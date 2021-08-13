import argparse
import os
import pickle

import dgl
import numpy as np
import torch

ap = argparse.ArgumentParser()
ap.add_argument("--dp", default="../data/", help="dataset path")
ap.add_argument("--dn", default="dataset", help="dataset name")
ap.add_argument("--dim", default=100, type=int, help="embedding dim (word/sentence)")
ap.add_argument("--ct", default='IR_', help='country name')
ap.add_argument("--hl", default=7, type=int, help="history_len (e.g., 7)")
args = ap.parse_args()


# 这个函数在1_get_digraphs.py中已经出现过了
def load_quadruples(inPath, fileName, fileName2=None, fileName3=None):
    with open(os.path.join(inPath, fileName), 'r') as fr:
        quadrupleList = []
        times = set()
        for line in fr:
            line_split = line.split()
            head = int(line_split[0])
            tail = int(line_split[2])
            rel = int(line_split[1])
            time = int(line_split[3])
            quadrupleList.append([head, rel, tail, time])
            times.add(time)
    if fileName2 is not None:
        with open(os.path.join(inPath, fileName2), 'r') as fr:
            for line in fr:
                line_split = line.split()
                head = int(line_split[0])
                tail = int(line_split[2])
                rel = int(line_split[1])
                time = int(line_split[3])
                quadrupleList.append([head, rel, tail, time])
                times.add(time)

    if fileName3 is not None:
        with open(os.path.join(inPath, fileName3), 'r') as fr:
            for line in fr:
                line_split = line.split()
                head = int(line_split[0])
                tail = int(line_split[2])
                rel = int(line_split[1])
                time = int(line_split[3])
                quadrupleList.append([head, rel, tail, time])
                times.add(time)
    times = list(times)
    times.sort()

    return np.asarray(quadrupleList), np.asarray(times)


# 这个函数在1_get_digraphs.py中已经出现过了
def get_total_number(inPath, fileName):
    with open(os.path.join(inPath, fileName), 'r') as fr:
        for line in fr:
            line_split = line.split()
            return int(line_split[0]), int(line_split[1])


# 这个函数在1_get_digraphs.py中已经出现过了
def get_data_with_t(data, tim):
    triples = [[quad[0], quad[1], quad[2]] for quad in data if quad[3] == tim]
    return np.array(triples)


def get_data_with_ts(data, t_min, t_max):
    triples = [[quad[0], quad[1], quad[2]] for quad in data if (quad[3] <= t_max) and (quad[3] >= t_min)]
    return np.array(triples)


# 这个函数在1_get_digraphs.py中已经出现过了
def comp_deg_norm(g):
    in_deg = g.in_degrees(range(g.number_of_nodes())).float()
    in_deg[torch.nonzero(in_deg == 0).view(-1)] = 1
    norm = 1.0 / in_deg
    return norm


def get_big_graph(data, num_rels):
    src, rel, dst = data.transpose()
    uniq_v, edges = np.unique((src, dst), return_inverse=True)
    src, dst = np.reshape(edges, (2, -1))
    g = dgl.DGLGraph()
    g.add_nodes(len(uniq_v))
    src, dst = np.concatenate((src, dst)), np.concatenate((dst, src))
    rel_o = np.concatenate((rel + num_rels, rel))
    rel_s = np.concatenate((rel, rel + num_rels))
    g.add_edges(src, dst)
    norm = comp_deg_norm(g)
    g.ndata.update({'id': torch.from_numpy(uniq_v).long().view(-1, 1), 'norm': norm.view(-1, 1)})
    g.edata['type_s'] = torch.LongTensor(rel_s)
    g.edata['type_o'] = torch.LongTensor(rel_o)
    g.ids = {}
    idx = 0
    for id in uniq_v:
        g.ids[id] = idx
        idx += 1
    return g


train_data, train_times = load_quadruples(args.dp + args.dn, args.ct + 'train.txt')
test_data, test_times = load_quadruples(args.dp + args.dn, args.ct + 'test.txt')
dev_data, dev_times = load_quadruples(args.dp + args.dn, args.ct + 'valid.txt')
total_data, total_times = load_quadruples(args.dp + args.dn, args.ct + 'train.txt', args.ct + 'valid.txt',
                                          args.ct + 'test.txt')

num_e, num_r = get_total_number(args.dp + args.dn, args.ct + 'stat.txt')

# '''
# rel
print('rel info...')
#################
r_his = [[] for _ in range(num_r)]
r_his_t = [[] for _ in range(num_r)]
r_history_data = [[] for _ in range(len(train_data))]
r_history_data_t = [[] for _ in range(len(train_data))]

latest_t = 0
r_his_cache = [[] for _ in range(num_r)]
r_his_cache_t = [None for _ in range(num_r)]

for i, train in enumerate(train_data):
    if i % 10000 == 0:
        print("train", i, len(train_data))
    # if i == 10000:
    #     break
    t = train[3]
    if latest_t != t:
        for rr in range(num_r):
            if len(r_his_cache[rr]) != 0:
                if len(r_his[rr]) >= args.hl:
                    r_his[rr].pop(0)
                    r_his_t[rr].pop(0)

                r_his[rr].append(r_his_cache[rr].copy())
                r_his_t[rr].append(r_his_cache_t[rr])
                r_his_cache[rr] = []
                r_his_cache_t[rr] = None
        latest_t = t
    s = train[0]
    r = train[1]
    o = train[2]
    r_history_data[i] = r_his[r].copy()
    r_history_data_t[i] = r_his_t[r].copy()
    if len(r_his_cache[r]) == 0:
        r_his_cache[r] = np.array([[s, o]])
    else:
        r_his_cache[r] = np.concatenate((r_his_cache[r], [[s, o]]), axis=0)
    r_his_cache_t[r] = t

print(len(r_history_data), len(r_history_data_t), args.ct + 'train_history_rel')
with open(os.path.join(args.dp + args.dn, args.ct + 'train_history_rel_{}.txt'.format(args.hl)), 'wb') as fp:
    pickle.dump([r_history_data, r_history_data_t], fp)

r_history_data_dev = [[] for _ in range(len(dev_data))]
r_history_data_dev_t = [[] for _ in range(len(dev_data))]

for i, dev in enumerate(dev_data):
    if i % 10000 == 0:
        print("valid", i, len(dev_data))
    t = dev[3]
    if latest_t != t:
        for rr in range(num_r):
            if len(r_his_cache[rr]) != 0:
                if len(r_his[rr]) >= args.hl:
                    r_his[rr].pop(0)
                    r_his_t[rr].pop(0)
                r_his_t[rr].append(r_his_cache_t[rr])
                r_his[rr].append(r_his_cache[rr].copy())
                r_his_cache[rr] = []
                r_his_cache_t[rr] = None

        latest_t = t
    s = dev[0]
    r = dev[1]
    o = dev[2]
    r_history_data_dev[i] = r_his[r].copy()
    r_history_data_dev_t[i] = r_his_t[r].copy()
    if len(r_his_cache[r]) == 0:
        r_his_cache[r] = np.array([[s, o]])
    else:
        r_his_cache[r] = np.concatenate((r_his_cache[r], [[s, o]]), axis=0)
    r_his_cache_t[r] = t

print(len(r_history_data_dev), len(r_history_data_dev_t), args.ct + 'valid_history_rel')
with open(os.path.join(args.dp + args.dn, args.ct + 'valid_history_rel_{}.txt'.format(args.hl)), 'wb') as fp:
    pickle.dump([r_history_data_dev, r_history_data_dev_t], fp)

r_history_data_test = [[] for _ in range(len(test_data))]
r_history_data_test_t = [[] for _ in range(len(test_data))]

for i, test in enumerate(test_data):
    if i % 10000 == 0:
        print("valid", i, len(test_data))
    t = test[3]
    if latest_t != t:
        for rr in range(num_r):
            if len(r_his_cache[rr]) != 0:
                if len(r_his[rr]) >= args.hl:
                    r_his[rr].pop(0)
                    r_his_t[rr].pop(0)
                r_his_t[rr].append(r_his_cache_t[rr])
                r_his[rr].append(r_his_cache[rr].copy())
                r_his_cache[rr] = []
                r_his_cache_t[rr] = None

        latest_t = t
    s = test[0]
    r = test[1]
    o = test[2]
    r_history_data_test[i] = r_his[r].copy()
    r_history_data_test_t[i] = r_his_t[r].copy()
    if len(r_his_cache[r]) == 0:
        r_his_cache[r] = np.array([[s, o]])
    else:
        r_his_cache[r] = np.concatenate((r_his_cache[r], [[s, o]]), axis=0)
    r_his_cache_t[r] = t

print(len(r_history_data_test), len(r_history_data_test_t), args.ct + 'test_history_rel')
with open(os.path.join(args.dp + args.dn, args.ct + 'test_history_rel_{}.txt'.format(args.hl)), 'wb') as fp:
    pickle.dump([r_history_data_test, r_history_data_test_t], fp)
    # print(train)
