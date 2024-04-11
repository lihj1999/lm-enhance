import pandas as pd
import ast
import regex as re
import numpy as np
import torch.utils.data as data
from config import *
from transformers import BertTokenizer
from transformers import DebertaTokenizer, DebertaModel
from sklearn.model_selection import train_test_split
from transformers import AutoModel, AutoTokenizer

df = pd.read_csv('./data/final_dataset.csv',header=0)
paras = list(df['paras'].values)
label = list(df['label'].values)
num = list(df['number'].values)
texts = []
tags = []
labels = []
for i in range(len(df)):
    texts += ast.literal_eval(paras[i])
    tags += ast.literal_eval(label[i])
    if '1' in label[i]:
        labels.append(1)
    else:
        labels.append(0)
    if num[i] != len(ast.literal_eval(paras[i])):
        print(i+2)
print(len(texts))
print(len(tags))
print(len(labels))
print(labels.count(1))       #存在合成段落
print(labels.count(0))       #不存在合成段落

paras = []
for i in range(len(texts)):
    texts[i] = re.sub(r'第\d+段\s\:','',texts[i])
    paras.append([texts[i],tags[i]])


def build_dataset(list):
    # 划分数据集为训练集、测试集和验证集
    train_ratio = 0.7
    test_ratio = 0.2
    val_ratio = 0.1

    # 先将数据集划分为训练集和临时集（包括测试集和验证集）
    train, temp = train_test_split(list, test_size=(1 - train_ratio))

    # 接着将临时集划分为测试集和验证集
    test, dev = train_test_split(temp, test_size=(val_ratio / (val_ratio + test_ratio)))
    return train, dev, test

class Dataset(data.Dataset):
    def __init__(self,list_para_label):
        super().__init__()
        self.data = list_para_label
        self.tokenizer = AutoTokenizer.from_pretrained(BERT_MODEL)
        #self.tokenizer = BertTokenizer.from_pretrained(BERT_MODEL)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        text, label = self.data[index][0], self.data[index][1]           #返回的是str类型
        tokened = self.tokenizer(text)

        input_ids = tokened['input_ids']
        mask = tokened['attention_mask']
        if len(input_ids) < TEXT_LEN:                     #负责填充
            pad_len = (TEXT_LEN - len(input_ids))
            input_ids += [BERT_PAD_ID] * pad_len          #列表形式
            mask += [0] * pad_len
        target = int(label)
        return torch.tensor(input_ids[:TEXT_LEN]), torch.tensor(mask[:TEXT_LEN]), torch.tensor(target)       #负责截取

def class_count(df):
    print(df.iloc[:,1].value_counts())
    print(df.iloc[:,1].value_counts(normalize = True))


def count_parameters(model):
    # 遍历模型的所有参数，并统计参数数量
    num_parameters = sum(p.numel() for p in model.parameters() if p.requires_grad)
    return f"{num_parameters / 1e6:.2f}M"

if __name__ == '__main__':
    # dataset = Dataset(list_para_label=paras)
    # loader = data.DataLoader(dataset, batch_size=BATCH_SIZE)
    # print(iter(loader).next())
    # print(iter(loader).next()[0].shape)

    # 设置随机种子 确保每次运行的条件(模型参数初始化、数据集的切分或打乱等)是一样的
    np.random.seed(1)
    torch.manual_seed(1)
    torch.cuda.manual_seed_all(1)
    torch.backends.cudnn.deterministic = True  # 保证每次结果一样
    train, dev, test = build_dataset(paras)
    number = 0
    for i in range(len(test)):
        if train[i][1] == 0:
            number += 1
    print(number)
    exit()
    train_data = data.DataLoader(Dataset(list_para_label=train), batch_size=BATCH_SIZE, shuffle=False)
    dev_data = data.DataLoader(Dataset(list_para_label=dev), batch_size=BATCH_SIZE, shuffle=False)
    test_data = data.DataLoader(Dataset(list_para_label=test), batch_size=BATCH_SIZE, shuffle=False)
    print(iter(train_data).next())

    # df = pd.DataFrame({'paras': texts, 'label': tags})
    # class_count(df)






# from transformers import BertTokenizer,BertModel
# from transformers import AutoModel, AutoTokenizer
# import torch
#
# # downloading the models
# # tokenizer = BertTokenizer.from_pretrained(BERT_MODEL)
# # model = BertModel.from_pretrained(BERT_MODEL)
# tokenizer = AutoTokenizer.from_pretrained('../huggingface_demo/chembert_cased/')
# model = AutoModel.from_pretrained('../huggingface_demo/chembert_cased/')
#
# # pass through the model
# print(inputs.input_ids)
# print(len(inputs.input_ids[0]))
# print(tokenizer.encode('([ce2(h2o)8(c4o4)2(c2o4)]·3h2o) (1)',add_special_tokens=True))
# print(tokenizer.decode([1162, 1477]))
# exit()
