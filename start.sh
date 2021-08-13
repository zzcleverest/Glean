#!/bin/bash
root_path=$(pwd)
if [ ! -d '../sent2vec' ]; then
  cd ..
  git clone https://github.com/epfml/sent2vec.git
  cd sent2vec
  make
  pip install .
  cd ${root_path}
fi
if [ $# -ge 1 ]; then
  (rm -f ${root_path}/data/dataset/*.txt)
  (rm -f ${root_path}/data/dataset/*.w_emb)
  (rm -f ${root_path}/data/dataset/*.npy)
  (rm -f ${root_path}/src/models/dataset/*.pth)
  echo start data preprocessing...
  cd data/dataset
  dataset_path=$(pwd)
  python data-preprocessing.py

fi
cd ${root_path}/presrc
presrc_path=$(pwd)
for ct in 'IR_' 'IZ_' 'TU_'; do
  echo $ct 0/9
  python 0_build_raw_sets.py --ct $ct --dn dataset/${ct}dataset
  echo $ct 1/9
  python 1_get_digraphs.py --ct $ct --dn dataset/${ct}dataset
  echo $ct 2/9
  python 2_get_history.py --ct $ct --dn dataset/${ct}dataset
  echo $ct 3/9
  python 3_get_token_for_embedding_training.py --ct $ct --dn dataset/${ct}dataset
  if [ $# -ge 1 ]; then
    cd ${root_path}
    cd ../sent2vec
    sent2vec_path=$(pwd)
    echo pretraining word2vec vector
    ./fasttext sent2vec -input ${root_path}/data/dataset/${ct}dataset/${ct}text_token.txt -lr 0.2 -lrUpdateRate 100 -dim 100 -epoch 5 -minCount 8 -minCountLabel 0 -neg 10 -wordNgrams 3 -loss ns -bucket 2000000 -thread 2 -t 0.0001 -dropoutK 4 -verbose 2 -numCheckPoints 1 -output ${root_path}/data/dataset/${ct}dataset/${ct}s2v_100
    cd ${presrc_path}
  fi
  echo $ct 4/9
  python 4_get_word_embedding.py --ct $ct --dn dataset/${ct}dataset
  echo $ct 5/9
  python 5_build_word_graphs.pmi.py --ct $ct --dn dataset/${ct}dataset
  echo $ct 6/9
  python 6_get_word_entity_map.py --ct $ct  --dn dataset/${ct}dataset
  echo $ct 7/9
  python 7_get_sub_event_dg_from_entity_g.py --ct $ct --dn dataset/${ct}dataset
  echo $ct 8/9
  python 8_get_sub_word_g_from_entity_g.py --ct $ct --dn dataset/${ct}dataset
  echo $ct 9/9
  python 9_get_scaled_tr_dataset.py --ct $ct --dn dataset/${ct}dataset
  cd ../src
  echo train $ct event predictor models
  python train_event_predictor.py --ct $ct --runs 50 --batch-size 4 --dn dataset/${ct}dataset
  echo train $ct acotor predictor models
  python train_actor_predictor.py --ct $ct --runs 50 --dn dataset/${ct}dataset
  cd -
done
