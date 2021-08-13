# -*- coding:utf-8 -*-
import datetime
import os
import re
import time

import pandas as pd
from nltk.tokenize import word_tokenize
from tqdm import tqdm

stopWords = {'very', 'ourselves', 'am', 'doesn', 'through', 'me', 'against', 'up', 'just', 'her', 'ours', 'couldn',
             'because', 'is', 'isn', 'it', 'only', 'in', 'such', 'too', 'mustn', 'under', 'their', 'if', 'to', 'my',
             'himself', 'after', 'why', 'while', 'can', 'each', 'itself', 'his', 'all', 'once', 'herself', 'more',
             'our', 'they', 'hasn', 'on', 'ma', 'them', 'its', 'where', 'did', 'll', 'you', 'didn', 'nor', 'as', 'now',
             'before', 'those', 'yours', 'from', 'who', 'was', 'm', 'been', 'will', 'into', 'same', 'how', 'some', 'of',
             'out', 'with', 's', 'being', 't', 'mightn', 'she', 'again', 'be', 'by', 'shan', 'have', 'yourselves',
             'needn', 'and', 'are', 'o', 'these', 'further', 'most', 'yourself', 'having', 'aren', 'here', 'he', 'were',
             'but', 'this', 'myself', 'own', 'we', 'so', 'i', 'does', 'both', 'when', 'between', 'd', 'had', 'the', 'y',
             'has', 'down', 'off', 'than', 'haven', 'whom', 'wouldn', 'should', 've', 'over', 'themselves', 'few',
             'then', 'hadn', 'what', 'until', 'won', 'no', 'about', 'any', 'that', 'for', 'shouldn', 'don', 'do',
             'there', 'doing', 'an', 'or', 'ain', 'hers', 'wasn', 'weren', 'above', 'a', 'at', 'your', 'theirs',
             'below', 'other', 'not', 're', 'him', 'during', 'which'}


def count_date(date1, date2):
    date1 = time.strptime(date1, "%Y%m%d")
    date2 = time.strptime(date2, "%Y%m%d")
    date1 = datetime.datetime(date1[0], date1[1], date1[2])
    date2 = datetime.datetime(date2[0], date2[1], date2[2])
    return (date1 - date2).days


def match_keywords(text, keywords):
    keyword = keywords.split()
    for i in keyword:
        if re.match(r'.*%s.*' % i, text, re.I):
            return True
    return False


def get_split_words(text):
    words = word_tokenize(text)
    word_set = set()
    for w in words:
        w = w.lower()
        if w not in stopWords:
            word_set.add(w)
    return word_set


def words_in_set(words, word_set):
    for w in words:
        if w in word_set:
            return True
    return False


def get_files(dires):
    files = []
    for i in os.listdir(dires):
        sub_dires = os.listdir(dires + '/' + i)
        for j in sub_dires:
            files.append(dires + '/' + i + '/' + j)
    files.sort()
    # return ['./IR/IR_2018/IR_20180101.csv']
    return files


for dire in ['./IR', './IZ', './TU']:
    # 实体集
    entities = set()
    # 事件类型集
    relations = set()
    # 四元组列表
    quadruple_list = []
    summary_list = []
    title_list = []
    print('reading %s files....' % dire)
    for i in tqdm(get_files(dire)):
        data = pd.read_csv(i)
        for j in range(len(data)):
            if pd.isnull(data['Actor1Name'][j]) or pd.isnull(data['Actor2Name'][j]) or pd.isnull(data['Content'][j]):
                continue
            else:
                s = data['Actor1Name'][j]
                r = data['EventCode'][j]
                o = data['Actor2Name'][j]
                t = data['SQLDATE'][j]
                illegalWords = 0
                for w in data['Content'][j].split()[:3]:
                    try:
                        w.encode('ascii')
                    except:
                        illegalWords += 1
                if illegalWords == 3:
                    continue
                entities.add(s)
                entities.add(o)
                relations.add(r)
                # 保存四元组序列，用于后续处理
                quadruple_list.append([s, r, o, t])
                summary = re.sub(r'[^\x00-\x7F]+', '', data['Content'][j])
                summary_list.append(summary)
                title_list.append(data['Title'][j])

    entity_file = open(dire + '_entity2id.txt', 'w', encoding='utf-8')

    relation_file = open(dire + '_relation2id.txt', 'w', encoding='utf-8')

    # 将实体集中元素保存到列表中，方便排序
    entity_list = list(entities)
    entity_list.sort()
    entities.clear()

    # entity_count作为entity的id，从0开始
    entity_count = 0
    # 用字典记录每个entity的id，方便将entity转换为id
    entity_dict = {}
    # 保存entity和id的映射
    for i in entity_list:
        entity_file.write(i + '	' + str(entity_count) + '\n')
        entity_dict[i] = entity_count
        entity_count += 1
    entity_file.close()
    entity_list = []
    # relation_count作为relation的id
    relation_count = 0
    # 如上
    relation_dict = {}
    relation_list = []
    # 将eventcode转换为EventCode.csv中的eventy type
    with open('EventCode.csv', 'r', encoding='utf-8') as file:
        file.readline()
        for line in file:
            line = line.strip()
            code, name = line.split('+')
            code = int(code)
            name = name.strip()
            if code in relations:
                relation_file.write(name + '	' + str(relation_count) + '\n')
                relation_dict[code] = relation_count
                relation_list.append(name)
                relation_count += 1
    relation_file.close()
    relations.clear()
    # 保存entity和relation的个数
    with open(dire + '_stat.txt', 'w', encoding='utf-8') as file:
        file.write(str(entity_count) + '	' + str(relation_count) + '	' + str(len(quadruple_list)) + '\n')
    # 保存(s,r,o,t) 四元组
    with open(dire + '_quadruple.txt', 'w', encoding='utf-8') as file:
        for i in quadruple_list:
            t = str(i[3])
            t = t[:4] + '-' + t[4:6] + '-' + t[6:]
            file.write(i[0] + '	' + relation_list[relation_dict[i[1]]] + '	' + i[2] + '	' + t + '\n')
    # 保存四元组的id值，即将s,r,o,t分别转换为其id
    with open(dire + '_quadruple_idx.txt', 'w', encoding='utf-8') as file:
        for i in quadruple_list:
            s = entity_dict[i[0]]
            r = relation_dict[i[1]]
            o = entity_dict[i[2]]
            # 时间的id就是将其减去20180101，即时间的起始点
            t = count_date(str(i[3]), '20180101')
            file.write(str(s) + '	' + str(r) + '	' + str(o) + '	' + str(t) + '\n')
    entity_dict = {}
    # 保存摘要，但现在只是简单地用s,r,o拼凑起来
    print('saving summaries...')
    with open(dire + '_text.txt', 'w', encoding='utf-8') as file:
        for i in tqdm(range(len(summary_list))):
            summary = ''
            sentence = summary_list[i].split('.')
            count = 0
            for j in sentence:
                words_set = get_split_words(j)
                relation_set = get_split_words(relation_list[relation_dict[int(quadruple_list[i][1])]])
                actors = get_split_words(quadruple_list[i][0] + ' ' + quadruple_list[i][2])
                if words_in_set(words_set, relation_set):
                    summary += j + '. '
                    continue
                if words_in_set(words_set, actors):
                    summary += j + '. '
                    continue
            if summary == '':
                summary = title_list[i]
            file.write(summary + '\n')
    print('done')
