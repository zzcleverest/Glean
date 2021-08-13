import argparse
import os
import pickle

import dgl
import numpy as np
import torch

print(os.getcwd())


# get direct graph
def get_total_number(inPath, fileName):
    with open(os.path.join(inPath, fileName), 'r') as fr:
        for line in fr:
            line_split = line.split()
            return int(line_split[0]), int(line_split[1])


def load_quadruples(inPath, fileName, fileName2=None, fileName3=None):
    # 从train.txt valid.txt test.txt三个文件中读取四元组
    # 其中，时间序列需要排序
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


def get_data_with_t(data, tim):
    triples = [[quad[0], quad[1], quad[2]] for quad in data if quad[3] == tim]
    return np.array(triples)


def get_indices_with_t(data, time):
    idx = [i for i in range(len(data)) if data[i][3] == time]
    return np.array(idx)


def comp_deg_norm(g):
    # 计算入度
    in_deg = g.in_degrees(range(g.number_of_nodes())).float()
    in_deg[torch.nonzero(in_deg == 0, as_tuple=False).view(-1)] = 1
    norm = 1.0 / in_deg
    return norm


def check_exist(outf):
    return os.path.isfile(outf)


def get_all_graph_dict(args):
    file = os.path.join(args.dp + args.dn, args.ct + 'dg_dict.txt')
    if not check_exist(file):
        # num_e是节点数，num_r是事件类型数
        num_e, num_r = get_total_number(args.dp + args.dn, args.ct + 'stat.txt')

        graph_dict = {}
        # 读取所有四元组和时间序列（有序）
        total_data, total_times = load_quadruples(args.dp + args.dn, args.ct + 'train.txt', args.ct + 'valid.txt',
                                                  args.ct + 'test.txt')
        print(total_data.shape, total_times.shape)

        for time in total_times:
            if time % 100 == 0:
                # 进度条？
                print(str(time) + '\tof ' + str(max(total_times)))
            # 获取t时刻的数据，构成三元组（s,r,o）
            data = get_data_with_t(total_data, time)
            # 获取t时刻的数据的索引 时间序列已经排序
            # search from total_data (unsplitted)
            edge_indices = get_indices_with_t(total_data, time)

            g = get_big_graph_w_idx(data, num_r, edge_indices)
            # 每个time对应一个事件图
            graph_dict[time] = g

        with open(file, 'wb') as fp:
            pickle.dump(graph_dict, fp)
        print(args.ct + 'dg_dict.txt saved! ')
    else:
        print(args.ct + 'dg_dict.txt exists! ')


def get_big_graph_w_idx(data, num_rels, edge_indices):
    # transpose()的作用是将矩阵转置，src，rel，dst刚好对应s，r，o
    src, rel, dst = data.transpose()
    # 去除重复的节点，uniq_v是所有不重复的实体集合
    # edges是旧列表（src，dst）元素在新列表（uniq_v）中的位置
    uniq_v, edges = np.unique((src, dst), return_inverse=True)
    # 用src，dst在新列表中的索引来表示src和dst
    src, dst = np.reshape(edges, (2, -1))
    g = dgl.DGLGraph()
    g.add_nodes(len(uniq_v))
    # array list
    # 'eid' 是指边的id
    g.add_edges(src, dst, {'eid': torch.from_numpy(edge_indices)})
    norm = comp_deg_norm(g)
    g.ndata.update({'id': torch.from_numpy(uniq_v).long().view(-1, 1), 'norm': norm.view(-1, 1)})
    g.edata['type'] = torch.LongTensor(rel)
    g.ids = {}
    idx = 0
    for id in uniq_v:
        g.ids[id] = idx
        idx += 1
    return g


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--dp", default="../data/", help="dataset path")
    ap.add_argument("--dn", default="dataset", help="dataset name")
    ap.add_argument("--ct", default='IR_', help='country name')

    args = ap.parse_args()
    print(args)

    if not os.path.exists(os.path.join(args.dp, args.dn)):
        print('Check if the dataset exists')
        exit()

    get_all_graph_dict(args)
