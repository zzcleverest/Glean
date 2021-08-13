# -*-coding:utf-8 -*-
# auhor:yangjing
import os

import pandas as pd

IR_dataset_path = '/home/user/data/t5/Glean/data/dataset/IR_dataset/IR_quadruple.txt'
TU_dataset_path = '/home/user/data/t5/Glean/data/dataset/TU_dataset/TU_quadruple.txt'
IZ_dataset_path = '/home/user/data/t5/Glean/data/dataset/IZ_dataset/IZ_quadruple.txt'

IR_text_path = '/home/user/data/t5/Glean/data/dataset/IR_dataset/IR_text.txt'
IZ_text_path = '/home/user/data/t5/Glean/data/dataset/IZ_dataset/IZ_text.txt'
TU_text_path = '/home/user/data/t5/Glean/data/dataset/TU_dataset/TU_text.txt'


def get_entity_relation_data(ct, tm):
    # return:
    #     date_node_rel = {'node':[{node1} , {node2} ] , 'relation':[{rel1 , rel2 2}]}
    # date_node_rel = {'node': [], 'relation': []}
    if ct == 'IR':
        path = os.path.join(IR_dataset_path)
        text_path = IR_text_path

    elif ct == 'TU':
        path = os.path.join(TU_dataset_path)
        text_path = TU_text_path
    elif ct == 'IZ':
        path = os.path.join(IZ_dataset_path)
        text_path = IZ_text_path
    else:
        raise Exception(" ct  only  'TU' , 'IZ' , 'IR' ")
    # f = open(path, 'r', encoding='utf-8')
    # des_file = open(text_path, 'r', encoding='utf-8')
    #
    #
    # count = 1
    # while 1:
    #     line = f.readline()
    #     if line == '':
    #         break
    #     # print(line)
    #     line = line.split()
    #     des = des_file.readline()
    #     if tm == line[-1]:
    #         des = des.split('.')[0]
    #         date_node_rel['node'].append({'name': line[0], 'des': '', 'symbolSize': 50, 'category': count})
    #         date_node_rel['node'].append({'name': line[2], 'des': '', 'symbolSize': 50, 'category': count})
    #         date_node_rel['relation'].append(
    #             {'source': line[0], 'target': line[2], 'name': ' '.join(line[1:len(line) - 2]), 'des': des})
    #         if count % 14 == 0:
    #             break
    #         count += 1
    #
    #     # if (count + 1) % 14 == 0:
    #     #     # date_node_rel.append({'node': node_data, 'relation': node_rel})
    #     #     date_node_rel['node'].append(node_data)
    #     #     date_node_rel['relation'].append(node_data)
    #     #     # break
    # print(date_node_rel)
    node_data = []
    relation_data = []
    print(path)
    qudruple = pd.read_csv(path, sep=' ', names=['s', 'r', 'o', 't'])
    des_file = open(text_path, 'r', encoding='utf-8')
    # add a set to record added node
    entity_set = set()
    count = 0
    for i in range(len(qudruple)):
        des = des_file.readline()
        if tm == qudruple['t'][i]:
            count += 1
            des = des.split('.')[0]
            if qudruple['s'][i] not in entity_set:
                node_data.append({'name': qudruple['s'][i], 'des': '', 'symbolSize': 50, 'category': count})
                entity_set.add(qudruple['s'][i])
            if qudruple['o'][i] not in entity_set:
                node_data.append({'name': qudruple['o'][i], 'des': '', 'symbolSize': 50, 'category': count})
                entity_set.add(qudruple['o'][i])
            relation_data.append(
                {'source': qudruple['s'][i], 'target': qudruple['o'][i], 'name': qudruple['r'][i], 'des': des})
        elif tm < qudruple['t'][i]:
            break
    entity_set.clear()
    return node_data, relation_data


# def get_entity_relation_data(ct, tm):
#     #  ct = 'TU' , 'IZ' , 'IR'
#     # tm = 2020-01-01 　格式
#     try:
#         date_node_rel = get_node(ct, tm)
#     except:
#         raise Exception("日期不符合格式或者超出范围")
#     return date_node_rel['node'], date_node_rel['relation']


if __name__ == '__main__':
    # get_node('IZ', '2019-01-01')
    get_entity_relation_data('IR', '2019-01-01')
