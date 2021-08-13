# log 
## 1119[yangjing] 
- 已经clone 源代码   ： https://github.com/amy-deng/glean
- 已经配置好pyenv + virtualenv 
- 已经下载好了python == 3.7.7 ,并且建立了 task4的虚拟环境名称 ,使用 pyenv local task4 进入(尽量别用global)
    - pyenv local task4
- 已经添加pip3 清华源 ， 在task4的环境安装好了 除pytorch之外依赖环境
    - pip3 install xxx
    - pytorch 等看看服务器的gpu怎么说吧

## 1130[yangjing]
- 下载google drive 数据，并且上传到服务器

- 配置好pytorch（ cpu/gpu)版本
    - '1.7.0+cpu'
    - 使用python3 [版本：3.6.9] ,不用python

----------

## 1204[chenjian]
- 将下载好的google drive数据上传到了 glean/data/AFG/ 目录下  
- 将项目所需的新闻数据上传到了 glean/data/dataset/ 目录下，同时上传了数据预处理代码文件，生成`stat.txt`等文件  
- 安装nltk，以及下载`punkt`包，放在` ~/nltk_data/tokenizers/`目录下，注意，下载下来的压缩包必须放在`tokenizers`目录下解压  
----------

## [1206yangjing]   AFG-example as the example.
事件预测，时间大约：
- epoch 每三分钟训练一轮，但是保存模型需要6分钟左右
```
python3 train_event_predictor.py --runs 1 --dp ../data/   -d AFG-example --seq-len 7
```
result 
```

```

参与者预测，时间大约：
- 一个epoch,一个半小时？
```

(task4) t5@VM-0-16-ubuntu:~/glean/src$ python3 train_actor_predictor.py --runs 1 --dp ../data/   -d AFG-example --num-r 20 --seq-len 7

```

```
Using backend: pytorch
Namespace(attn='', batch_size=1, dataset='AFG-example', dp='../data/', dropout=0.5, gpu=0, grad_norm=1.0, lr=0.001, max_epochs=10, maxpool=1, n_hidden=100, num_r=20, patience=5, rnn_layers=1, runs=1, seed=42, seq_len=7, use_gru=1, weight_decay=1e-05)
/home/t5/.pyenv/versions/3.7.7/envs/task4/lib/python3.7/site-packages/torch/cuda/__init__.py:52: UserWarning: CUDA initialization: Found no NVIDIA driver on your system. Please check that you have an NVIDIA GPU and installed a driver from http://www.nvidia.com/Download/index.aspx (Triggered internally at  /pytorch/c10/cuda/CUDAFunctions.cpp:100.)
  return torch._C._cuda_getDeviceCount() > 0
cuda False
-------------- iterations  1
load tr_data ... AFG-example train
load tr_data ... AFG-example valid
load tr_data ... AFG-example test
Token: glean_actor_sl7_max1_gru1_attn AFG-example
#params: 639903
 15%|████████████▍                                                                     | 416/2732 [16:22<1:11:30,  1.85s/it]

```

----------
## 1211[chenjian]  
- 代码迁移到`user@106.52.65.202:~/data/t5/Glean`目录下，多事件预测模型和多参与者预测模型已经可以训练了。

