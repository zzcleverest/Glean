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

fail_information = {'fail', 'page', 'found', 'displayed', 'error', 'contact', 'support'}

event_dict = {}
with open('EventCode.csv', 'r', encoding='utf-8') as file:
    file.readline()
    for line in file:
        line = line.strip()
        code, name = line.split('+')
        name = name.strip()
        event_dict[int(code)] = name


def calculate_time(date_begin, date_end):
    '''
    lculate the past days from date_begin to date_end
    :param date_begin: for example: 2018-01-01
    :param date_end: for example: 2018-01-02
    :return: for example: 1
    '''
    date_begin = time.strptime(date_begin, "%Y-%m-%d")
    date_end = time.strptime(date_end, "%Y-%m-%d")
    date_begin = datetime.datetime(date_begin[0], date_begin[1], date_begin[2])
    date_end = datetime.datetime(date_end[0], date_end[1], date_end[2])
    return (date_end - date_begin).days


def get_split_words(text):
    '''
    split a sentence to words, and remove stop words
    :param text: I love python
    :return: {love, python}
    '''
    words = word_tokenize(text)
    word_set = set()
    for w in words:
        w = w.lower()
        if w not in stopWords:
            word_set.add(w)
    return word_set


def words_in_set(words, word_set):
    '''
    whether the words in word_set
    :param words: [i, love, python]
    :param word_set: {love}
    :return: True
    '''
    for w in words:
        if w in word_set:
            return True
    return False


def get_files(dires):
    '''
    get the dateset files from a directory
    :param dires: ./IR
    :return: [./IR/IR_2018/IR_20180101.csv....]
    '''
    files = []
    for i in os.listdir(dires):
        sub_dires = os.listdir(dires + '/' + i)
        for j in sub_dires:
            files.append(dires + '/' + i + '/' + j)
    files.sort()
    # return ['./IR/IR_2018/IR_20180101.csv']
    return files


def is_failed_pull(summary_world_set):
    if len(summary_world_set & fail_information) > 4:
        return True
    return False


def is_dirty_data(summary, s, r, o):
    '''
    judge if the summary is a dirty data
    :param summary:
    :return: True or False
    '''
    words_set = get_split_words(summary)
    relation_set = get_split_words(event_dict[r])
    actor_set = get_split_words(s + '.' + o)
    if not words_in_set(words_set, relation_set | actor_set):
        return is_failed_pull(words_set)
    return False


def is_english_content(summary):
    illegalWords = 0
    for w in summary.split()[:3]:
        try:
            w.encode('ascii')
        except:
            illegalWords += 1
    if illegalWords == 3:
        return False
    return True


def save_csv(dire, file_name, data):
    frame = pd.DataFrame(data)
    frame.to_csv(os.path.join(dire, file_name), index=False, header=False, sep=' ')


def extract_summary(content, s, r, o):
    summary = ''
    content = re.sub(r'[^\x00-\x7F]+', '', content)
    sentence = content.split('.')
    for i in sentence:
        words_set = get_split_words(i)
        relation_set = get_split_words(event_dict[r])
        actor_set = get_split_words(s + '.' + o)
        if not words_in_set(words_set, relation_set | actor_set):
            continue
        summary += i + '.'
    if summary == '':
        summary = content
    return summary


def read_dateset(dire, files):
    # 实体集
    entities = set()
    # 事件类型集
    relations = set()
    # 四元组列表
    quadruple_list = []
    summary_list = []
    for i in tqdm(files):
        data = pd.read_csv(i)
        for j in range(len(data)):
            if pd.isnull(data['Actor1Name'][j]) or pd.isnull(data['Actor2Name'][j]) or pd.isnull(data['Content'][j]):
                continue
            else:
                s = data['Actor1Name'][j]
                r = data['EventCode'][j]
                o = data['Actor2Name'][j]
                t = str(data['SQLDATE'][j])
                t = t[:4] + '-' + t[4:6] + '-' + t[6:]
                if not is_english_content(data['Content'][j]):
                    continue
                if is_dirty_data(data['Content'][j], s, r, o):
                    continue
                entities.add(s)
                entities.add(o)
                relations.add(r)
                # 保存四元组序列，用于后续处理
                quadruple_list.append([s, r, o, t])
                summary_list.append(extract_summary(data['Content'][j], s, r, o))
    save_csv(dire + '_dataset', dire + '_text.txt', summary_list)
    save_csv(dire + '_dataset', dire + '_stat.txt', [[len(entities), len(relations), len(quadruple_list)]])
    return entities, relations, quadruple_list


def save_entity_file(dire, entities):
    entity_list = list(entities)
    entity_list.sort()
    entity_dict = {}
    data = []
    for i in range(len(entity_list)):
        data.append([entity_list[i], i])
        entity_dict[entity_list[i]] = i
    save_csv(dire + '_dataset', dire + '_entity2id.txt', data)
    return entity_dict


def save_relation_file(dire, relations):
    relation_dict = {}
    data = []
    count = 0
    for i in relations:
        data.append([event_dict[i], count])
        relation_dict[event_dict[i]] = count
        count += 1
    save_csv(dire + '_dataset', dire + '_relation2id.txt', data)
    return relation_dict


def save_quadruple_file(dire, quadruple_list, entity_dict, relation_dict):
    data = []
    for i in quadruple_list:
        data.append([i[0], event_dict[i[1]], i[2], i[3]])
    save_csv(dire + '_dataset', dire + '_quadruple.txt', data)
    data = []
    for i in quadruple_list:
        data.append(
            [entity_dict[i[0]], relation_dict[event_dict[i[1]]], entity_dict[i[2]], calculate_time('2018-01-01', i[3])])
    save_csv(dire + '_dataset', dire + '_quadruple_idx.txt', data)


if __name__ == "__main__":
    for i in ['IR', 'IZ', 'TU']:
        os.makedirs(i + '_dataset', exist_ok=True)
        entities, relations, quadruple_list = read_dateset(i, get_files(i))
        entity_dict = save_entity_file(i, entities)
        relation_dict = save_relation_file(i, relations)
        save_quadruple_file(i, quadruple_list, entity_dict, relation_dict)
