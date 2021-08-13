import datetime
import os
import pickle
import time
from array import array
import numpy
import pandas as pd
import torch
from flask import *
from torch.utils.data import DataLoader
from tqdm import tqdm
from data import *
from get_quadruple import get_entity_relation_data
from models import glean_event, glean_actor

app = Flask(__name__)


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


def get_total_number(inPath, fileName):
    with open(os.path.join(inPath, fileName), 'r') as fr:
        for line in fr:
            line_split = line.split()
            return int(line_split[0]), int(line_split[1])


def collate_4(batch):
    batch_data = [item[0] for item in batch]
    s_prob = [item[1] for item in batch]
    r_prob = [item[2] for item in batch]
    o_prob = [item[3] for item in batch]
    return [batch_data, s_prob, r_prob, o_prob]


def collate_6(batch):
    inp0 = [item[0] for item in batch]
    inp1 = [item[1] for item in batch]
    inp2 = [item[2] for item in batch]
    inp3 = [item[3] for item in batch]
    inp4 = [item[4] for item in batch]
    inp5 = [item[5] for item in batch]
    return [inp0, inp1, inp2, inp3, inp4, inp5]


@app.route('/t5/')
def index():
    return render_template("index.html")


# def get_entity_relation_data(ct, tm):
#     node_data = []
#     relation_data = []
#     for i in range(100):
#         node_data.append({'name': '%d' % i, 'des': 'node %d' % i, 'symbolSize': 50, 'category': i})
#         relation_data.append(
#             {'source': '%d' % random.randint(0, 100), 'target': '%d' % random.randint(0, 100),
#              'name': 'link %d' % i, 'des': 'link%ddes' % i})
#     return node_data, relation_data


def generate_data(ct, tm, rel):
    # f = open('../data/dataset/' + ct + '_dataset/' + ct + '_predict.txt', 'w', encoding='utf-8')
    t = int(calculate_time('2018-01-01', tm)) - 7
    r_data = []
    t_data = []
    record = None
    data = []
    t_set = set()
    with open('../data/dataset/' + ct + '_dataset/' + ct + '_quadruple_idx.txt', 'r', encoding='utf-8') as file:
        for line in file:
            s, r, o, t1 = [int(i) for i in line.split(' ')]
            if t <= t1 < t + 7:
                if r == rel:
                    if t1 not in t_set:
                        t_set.add(t1)
                        t_data.append(numpy.int64(t1))
                    if record is None or record == t1:
                        record = t1
                        data.append([numpy.int64(s), numpy.int64(o)])
                    else:
                        r_data.append(numpy.array(data))
                        data = [numpy.int64(s), numpy.int64(o)]
                        record = t1
            elif t1 >= t + 7:
                # r_data = [numpy.array(i, dtype=numpy.int64) for i in r_data]
                r_data.append(numpy.array(data))
                return [t_data], [r_data]
    return [], []


def get_relation_name(ct, data):
    relation = pd.read_csv('../data/dataset/' + ct + '_dataset/' + ct + '_relation2id.txt', sep=' ', names=['name', 'id'])
    relation_name = []
    for i in data:
        for j in range(len(relation)):
            if relation['id'][j] == i:
                relation_name.append(relation['name'][j])
    return relation_name


def get_actor_graph(ct, sub_prob, sub_id, ob_prob, ob_id, name):
    node_data = []
    relation_data = []
    entity_dict = {}
    entity_set = set()
    name = name.replace('+', ' ')
    actor = pd.read_csv('../data/dataset/' + ct + '_dataset/' + ct + '_entity2id.txt', sep=' ', names=['name', 'id'])
    for i in range(len(actor)):
        entity_dict[actor['id'][i]] = actor['name'][i]
    node_data.append({'name': name, 'des': '', 'symbolSize': 50, 'category': 0})
    for i in range(len(sub_id)):
        if sub_id[i] not in entity_set:
            entity_set.add(sub_id[i])
            node_data.append({'name': entity_dict[sub_id[i]], 'des': str(sub_prob[i]), 'symbolSize': 50, 'category': 1})
        if ob_id[i] not in entity_set:
            entity_set.add(ob_id[i])
            node_data.append({'name': entity_dict[ob_id[i]], 'des': str(ob_prob[i]), 'symbolSize': 50, 'category': 2})
        relation_data.append({'source': entity_dict[sub_id[i]], 'target': name, 'name': '%d' % i, 'des': ''})
        relation_data.append({'source': name, 'target': entity_dict[ob_id[i]], 'name': '%d' % i, 'des': ''})
    return node_data, relation_data


def get_event_predict_result(ct, tm):
    x_data = []
    y_data = []
    print("loading data...")
    num_nodes, num_rels = get_total_number('../data/dataset/', ct + '_dataset/' + ct + '_stat.txt')
    with open('{}{}/{}_100.w_emb'.format('../data/', 'dataset', ct + '_dataset/' + ct), 'rb') as f:
        word_embeds = pickle.load(f, encoding="latin1")
    word_embeds = torch.FloatTensor(word_embeds)

    with open('../data/dataset/' + ct + '_dataset/' + ct + '_dg_dict.txt', 'rb') as f:
        graph_dict = pickle.load(f)
    print('load dg_dict.txt')
    with open('../data/dataset/' + ct + '_dataset/' + ct + '_wg_dict_truncated.txt', 'rb') as f:
        word_graph_dict = pickle.load(f)
    print('load wg_dict_truncated.txt')
    with open('../data/dataset/' + ct + '_dataset/' + ct + '_word_relation_map.txt', 'rb') as f:
        rel_map = pickle.load(f)
    print('load word_relation_map.txt')
    with open('../data/dataset/' + ct + '_dataset/' + ct + '_word_entity_map.txt', 'rb') as f:
        ent_map = pickle.load(f)
    print('load word_entity_map.txt')

    model = glean_event(h_dim=100, num_ents=num_nodes,
                        num_rels=num_rels, dropout=0.5,
                        seq_len=7,
                        maxpool=1,
                        use_gru=1,
                        attn='')

    model_name = model.__class__.__name__
    print('Model:', model_name)
    token = '{}_{}_sl{}_max{}_gru{}_attn{}'.format(ct, model_name, 7, int(1),
                                                   int(1), str(''))
    print('Token:', token, 'dataset/')
    total_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print('#params:', total_params)
    model_state_file = '../src/models/{}/{}.pth'.format('dataset/' + ct + '_dataset', token)
    use_cuda = True
    if use_cuda:
        model.cuda()
        word_embeds = word_embeds.cuda()

    model.word_embeds = word_embeds
    model.graph_dict = graph_dict
    model.word_graph_dict = word_graph_dict
    model.ent_map = ent_map
    model.rel_map = rel_map
    try:
        checkpoint = torch.load(model_state_file, map_location=lambda storage, loc: storage)
        model.load_state_dict(checkpoint['state_dict'])
        print("start multi-event prediction...")
        checkpoint = torch.load(model_state_file, map_location=lambda storage, loc: storage)
        model.load_state_dict(checkpoint['state_dict'])
        # evaluate(data_loader)
        model.eval()
        batch_data = torch.tensor([int(calculate_time('2018-01-01', tm))])

        loss, pred, _ = model.predict(batch_data, None)
        prob_rel = model.out_func(pred.view(-1))
        sorted_prob_rel, prob_rel_idx = prob_rel.sort(0, descending=True)
        y_data = sorted_prob_rel.cpu().tolist()[:10]
        x_data = get_relation_name(ct, prob_rel_idx.cpu().tolist()[:10])
        print("multi-event prediction done")
    except KeyboardInterrupt:
        print('-' * 80)
        print('Exiting from predicting early')
    return x_data, y_data


def get_actor_predict_result(ct, tm, rel=None, relation_name=None):
    print('loading data...')
    num_nodes, num_rels = get_total_number('../data/dataset/', ct + '_dataset/' + ct + '_stat.txt')
    with open('{}{}/{}_100.w_emb'.format('../data/', 'dataset', ct + '_dataset/' + ct), 'rb') as f:
        word_embeds = pickle.load(f, encoding="latin1")
    word_embeds = torch.FloatTensor(word_embeds)
    r_hist_t, r_hist = generate_data(ct, tm, rel)
    # dataset_loader = EntDistGivenTRData(
    #     '../data/', 'dataset/' + ct + '_dataset/', num_nodes, num_rels, ct + '_predict', 7, num_r=20)
    # data_loader = DataLoader(dataset_loader, batch_size=1, shuffle=False, collate_fn=collate_6)

    with open('../data/' + 'dataset/' + ct + '_dataset/' + '/{}_wg_r_dict_sl{}_rand_{}.txt'.format(ct, 7, 20),
              'rb') as f:
        word_graph_dict = pickle.load(f)
    with open('../data/' + 'dataset/' + ct + '_dataset/' + '/{}_dg_r_dict_sl{}_rand_{}.txt'.format(ct, 7, 20),
              'rb') as f:
        graph_dict = pickle.load(f)

    # load word_relation_map.txt
    with open('../data/' + 'dataset/' + ct + '_dataset/' + '/' + ct + '_word_relation_map.txt', 'rb') as f:
        rel_map = pickle.load(f)
    # load word_entity_map.txt
    with open('../data/' + 'dataset/' + ct + '_dataset/' + '/' + ct + '_word_entity_map.txt', 'rb') as f:
        ent_map = pickle.load(f)
    print('initiating model...')
    # n_hidden就是d，默认为100
    model = glean_actor(h_dim=100, num_ents=num_nodes,
                        num_rels=num_rels, dropout=0.5,
                        seq_len=7,
                        maxpool=1,
                        use_gru=1,
                        attn='')

    model_name = model.__class__.__name__
    token = '{}_{}_sl{}_max{}_gru{}_attn{}'.format(ct, model_name, 7, 1, 1, '')

    print('Token:', token, 'dataset/' + ct + '_dataset/')

    total_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print('#params:', total_params)
    model_state_file = '../src/models/{}/{}.pth'.format('dataset/' + ct + '_dataset', token)
    model.cuda()
    word_embeds = word_embeds.cuda()

    model.word_embeds = word_embeds
    model.graph_dict = graph_dict
    model.word_graph_dict = word_graph_dict
    model.ent_map = ent_map
    model.rel_map = rel_map
    print("start multi-actor prediction...")
    checkpoint = torch.load(model_state_file, map_location=lambda storage, loc: storage)
    model.load_state_dict(checkpoint['state_dict'])
    model.eval()
    try:
        _, sub_pred, ob_pred = model.predict(torch.tensor([int(calculate_time('2018-01-01', tm))]), torch.tensor([int(rel)]), r_hist, r_hist_t, None, None)
        # print(sub_pred.cpu().tolist())
        # print(len(sub_pred.cpu().tolist()))
        # print(ob_pred.cpu().tolist())
        # print(len(ob_pred.cpu().tolist()))
        prob_sub = model.out_func(sub_pred.view(-1))
        prob_ob = model.out_func(ob_pred.view(-1))
        sort_prob_sub, prob_sub_idx = prob_sub.sort(0, descending=True)
        sort_prob_ob, prob_ob_idx = prob_ob.sort(0, descending=True)
        sub_prob = sort_prob_sub.cpu().tolist()[:10]
        sub_id = prob_sub_idx.cpu().tolist()[:10]
        ob_prob = sort_prob_ob.cpu().tolist()[:10]
        ob_id = prob_ob_idx.cpu().tolist()[:10]
        print('multi-actor prediction done')
        return get_actor_graph(ct, sub_prob, sub_id, ob_prob, ob_id, relation_name)
        # for i, batch in enumerate(tqdm(data_loader)):
        #     t_data, r_data, r_hist, r_hist_t, true_s, true_o = batch
        #     t_data = torch.stack(t_data, dim=0)
        #     r_data = torch.stack(r_data, dim=0)
        #     print(t_data)
        #     print(r_data)
        # _, sub_pred, ob_pred = model.predict()
    except KeyboardInterrupt:
        print('-' * 80)
        print('Exiting from training early')


@app.route('/t5/predict/<ct>', methods=['GET'])
def predict(ct):
    if ct == "IR":
        return render_template("predict.html", default="2019-01-01", min="2019-01-01", max="2020-01-01")
    elif ct == "IZ":
        return render_template("predict.html", default="2018-01-01", min="2018-01-01", max="2020-06-21")
    elif ct == "TU":
        return render_template("predict.html", default="2019-01-01", min="2019-01-01", max="2020-06-21")
    else:
        return render_template("error.html")


@app.route('/t5/api/<ct>/<type>', methods=['POST'])
def api(ct, type):
    rec_data = request.get_data().decode('utf-8')
    tm = rec_data.split('=')[1]
    tm = tm.split('&')[0]
    if type == 'graph':
        node_data, relation_data = get_entity_relation_data(ct, tm)
        return json.dumps({'node_data': node_data, 'relation_data': relation_data})
    elif type == 'event':
        event_x_data, event_y_data = get_event_predict_result(ct, tm)
        return json.dumps({'event_x_data': event_x_data, 'event_y_data': event_y_data})
    elif type == 'actor':
        relation = rec_data.split('=')[2].split('&')[0]
        relation_name = rec_data.split('=')[3]
        actor_x_data, actor_y_data = get_actor_predict_result(ct, tm, int(relation), relation_name)
        return json.dumps({'actor_node_data': actor_x_data, 'actor_relation_data': actor_y_data})
    else:
        return render_template("error.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
