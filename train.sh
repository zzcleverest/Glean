#!/bin/bash
root_path=$(pwd)

cd ${root_path}/src
for ct in 'IR_' 'IZ_' 'TU_'; do
  echo train $ct event predictor models
  python train_event_predictor.py --ct $ct --runs 5 --batch-size 4 --dn dataset/${ct}dataset
  echo train $ct acotor predictor models
  python train_actor_predictor.py --ct $ct --runs 5 --dn dataset/${ct}dataset
  cd -
done
