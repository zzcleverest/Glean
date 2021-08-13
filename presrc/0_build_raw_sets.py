import argparse
import os

print(os.getcwd())


# build train/valid/test sets by time
# using full_events(with event sentence) the dates are fixed
# 切割数据集
def get_total_number(inPath, fileName):
    with open(os.path.join(inPath, fileName), 'r') as fr:
        for line in fr:
            line_split = line.split()
            return int(line_split[0]), int(line_split[1]), int(line_split[2])


def split(args):
    # num_nodes, num_rels = get_total_number(args.dp + args.dn, 'stat.txt')

    quadruple_idx_path = os.path.join(args.dp + args.dn, args.ct + 'quadruple_idx.txt')
    # ratio 80% 10% 10%（训练集，验证集，测试集）的比例
    # in total 2557 days (0-2556) 
    # 
    # cut_1和cut_2需要更改，以使得训练集，验证集，测试集的比例适应
    '''
    df = pd.read_csv(quadruple_idx_path, sep='\t',  lineterminator='\n', names=[
                     'source', 'relation', 'target', 'time'])
    print(df.head())
    cut_1 = 1795 #2044
    cut_2 = 2019 #2300
    train_df = df.loc[df['time'] <= cut_1]
    valid_df = df.loc[(df['time'] > cut_1) & (df['time'] <= cut_2)]
    test_df = df.loc[df['time'] > cut_2]

    train_df.to_csv(train_path, sep='\t', encoding='utf-8', header=None, index=False)
    valid_df.to_csv(valid_path, sep='\t', encoding='utf-8', header=None, index=False)
    test_df.to_csv(test_path, sep='\t', encoding='utf-8', header=None, index=False)
    '''
    train_path = os.path.join(args.dp + args.dn, args.ct + 'train.txt')
    valid_path = os.path.join(args.dp + args.dn, args.ct + 'valid.txt')
    test_path = os.path.join(args.dp + args.dn, args.ct + 'test.txt')
    total_count = get_total_number(args.dp + args.dn, args.ct + 'stat.txt')[2]
    df = open(quadruple_idx_path, 'r', encoding='utf-8')
    valid_beg = int(total_count * 0.8)
    test_beg = int(total_count * 0.9)
    # 总共有738286条数据，按比例来划分数据集
    with open(train_path, 'w', encoding='utf-8') as file:
        for _ in range(valid_beg):
            file.write(df.readline())
    with open(valid_path, 'w', encoding='utf-8') as file:
        for _ in range(test_beg - valid_beg):
            file.write(df.readline())
    with open(test_path, 'w', encoding='utf-8') as file:
        while True:
            tx = df.readline()
            if tx == '':
                break
            else:
                file.write(tx)
    print(train_path, 'saved')
    print(valid_path, 'saved')
    print(test_path, 'saved')


if __name__ == "__main__":
    ap = argparse.ArgumentParser()

    ap.add_argument("--dp", default="../data/", help="dataset path")
    ap.add_argument("--dn", default="dataset", help="dataset name (will create a folder)")
    ap.add_argument("--ct", default='IR_', help='country name')

    args = ap.parse_args()
    print(args)

    if not os.path.exists("{}{}".format(args.dp, args.dn)):
        print('Check if the dataset exists')
        exit()

    split(args)
