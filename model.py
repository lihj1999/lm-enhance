import torch.nn as nn
import torch.nn.functional as F
import torch
from config import *
from transformers import BertModel
from transformers import AutoModel, AutoTokenizer

from transformers import logging
logging.set_verbosity_error()


class MeanPooling(nn.Module):
    def __init__(self):
            super(MeanPooling, self).__init__()
    def forward(self, last_hidden_state, attention_mask):
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(last_hidden_state.size()).float()
        sum_embeddings = torch.sum(last_hidden_state * input_mask_expanded, 1)
        sum_mask = input_mask_expanded.sum(1)
        sum_mask = torch.clamp(sum_mask, min=1e-9)
        mean_embeddings = sum_embeddings / sum_mask
        return mean_embeddings


class Model(nn.Module):
    def __init__(self):
        super(Model, self).__init__()
        self.bert = AutoModel.from_pretrained(BERT_MODEL)
        self.pooler = MeanPooling()
        # self.bert = BertModel.from_pretrained(BERT_MODEL)
        for param in self.bert.parameters():
            param.requires_grad = False  #True
        self.fc = nn.Linear(EMBEDDING_DIM, NUM_CLASSES)

    def forward(self, input, mask):
        #DeBERTa 预训练模型的输出通常是一个包含一个元素的元组 (tuple)last_hidden_state：这是一个张量，包含了经过模型所有层处理后的文本表示。
        # output = self.bert(input,attention_mask=mask,token_type_ids=None,output_hidden_states=False)
        # pooled = self.pooler(output.last_hidden_state, mask)
        # out = self.fc(pooled)
        # return out

        _, pooled = self.bert(input, attention_mask=mask, token_type_ids=None, output_hidden_states=False,return_dict=False)         #mask对padding部分进行mask，和句子一个size，padding部分用0表示，如：[1, 1, 1, 1, 0, 0]
        out = self.fc(pooled)
        return out

class TextModel(nn.Module):
    def __init__(self, model_name):
        super(TextModel, self).__init__()
        self.model = AutoModel.from_pretrained(BERT_MODEL)
        self.drop = nn.Dropout(p=0.2)
        self.pooler = MeanPooling()
        self.fc = nn.Linear(EMBEDDING_DIM, NUM_CLASSES)
    def forward(self, ids, mask):
        #deberta的写法
        out = self.model(input_ids=ids,attention_mask=mask,
                         output_hidden_states=False)
        out = self.pooler(out.last_hidden_state, mask)

        out = self.drop(out)
        outputs = self.fc(out)
        return outputs

filter_sizes = (2, 3, 4)                                   # 卷积核尺寸
num_filters = 256                                          # 卷积核数量

class Model_cnn(nn.Module):
    def __init__(self):
        super(Model_cnn, self).__init__()
        self.bert = BertModel.from_pretrained(BERT_MODEL)
        for param in self.bert.parameters():
            param.requires_grad = False
        self.convs = nn.ModuleList(
            [nn.Conv2d(1, num_filters, (k, EMBEDDING_DIM)) for k in filter_sizes])
        self.dropout = nn.Dropout(p=0.1)

        self.fc_cnn = nn.Linear(num_filters * len(filter_sizes), NUM_CLASSES)

    def conv_and_pool(self, x, conv):
        x = F.relu(conv(x)).squeeze(3)
        x = F.max_pool1d(x, x.size(2)).squeeze(2)
        return x

    def forward(self, input, mask):
        encoder_out= self.bert(input, attention_mask=mask)[0]
        out = encoder_out.unsqueeze(1)
        out = torch.cat([self.conv_and_pool(out, conv) for conv in self.convs], 1)
        out = self.dropout(out)
        out = self.fc_cnn(out)
        return out


dp_cnn_num_filters = 250
class Model_dpcnn(nn.Module):
    def __init__(self, config):
        super(Model_dpcnn, self).__init__()
        self.bert = BertModel.from_pretrained(BERT_MODEL)
        for param in self.bert.parameters():
            param.requires_grad = False
        # self.fc = nn.Linear(config.hidden_size, config.num_classes)
        self.conv_region = nn.Conv2d(1, dp_cnn_num_filters, (3, EMBEDDING_DIM), stride=1)
        self.conv = nn.Conv2d(dp_cnn_num_filters, dp_cnn_num_filters, (3, 1), stride=1)
        self.max_pool = nn.MaxPool2d(kernel_size=(3, 1), stride=2)
        self.padding1 = nn.ZeroPad2d((0, 0, 1, 1))  # top bottom
        self.padding2 = nn.ZeroPad2d((0, 0, 0, 1))  # bottom
        self.relu = nn.ReLU()
        self.fc = nn.Linear(dp_cnn_num_filters, NUM_CLASSES)

    def forward(self, input, mask):
        encoder_out = self.bert(input, attention_mask=mask)[0]
        x = encoder_out.unsqueeze(1)  # [batch_size, 1, seq_len, embed]
        x = self.conv_region(x)  # [batch_size, 250, seq_len-3+1, 1]

        x = self.padding1(x)  # [batch_size, 250, seq_len, 1]
        x = self.relu(x)
        x = self.conv(x)  # [batch_size, 250, seq_len-3+1, 1]
        x = self.padding1(x)  # [batch_size, 250, seq_len, 1]
        x = self.relu(x)
        x = self.conv(x)  # [batch_size, 250, seq_len-3+1, 1]
        while x.size()[2] > 2:
            x = self._block(x)
        x = x.squeeze()  # [batch_size, num_filters(250)]
        x = self.fc(x)
        return x

    def _block(self, x):
        x = self.padding2(x)
        px = self.max_pool(x)
        x = self.padding1(px)
        x = F.relu(x)
        x = self.conv(x)
        x = self.padding1(x)
        x = F.relu(x)
        x = self.conv(x)
        x = x + px  # short cut
        return x


# class Model_rcnn(nn.Module):

lstm_hidden = 768
lstm_num_layers = 2
class Model_lstm(nn.Module):
    def __init__(self, config):
        super(Model_lstm, self).__init__()
        self.bert = BertModel.from_pretrained(BERT_MODEL)
        for param in self.bert.parameters():
            param.requires_grad = False
        self.lstm = nn.LSTM(EMBEDDING_DIM, lstm_hidden, lstm_num_layers,
                            bidirectional=True, batch_first=True, dropout=0.1)
        self.dropout = nn.Dropout(p=0.1)
        self.fc_rnn = nn.Linear(lstm_hidden * 2, NUM_CLASSES)

    def forward(self, input, mask):
        encoder_out = self.bert(context, attention_mask=mask, output_all_encoded_layers=False)
        out, _ = self.lstm(encoder_out)
        out = self.dropout(out)
        out = self.fc_rnn(out[:, -1, :])  # 句子最后时刻的 hidden state
        return out


if __name__ == '__main__':
    model = Model()
    input = torch.randint(0, 3000, (16, TEXT_LEN))
    mask = torch.ones_like(input)
    print(model(input, mask).shape)

#keras flatten the output and add Dropout with two Fully-Connected layers. The last layer has a softmax activation function.
# cls_out = keras.layers.Lambda(lambda seq: seq[:, 0, :])(bert_output)
#   cls_out = keras.layers.Dropout(0.5)(cls_out)
#   logits = keras.layers.Dense(units=768, activation="tanh")(cls_out)
#   logits = keras.layers.Dropout(0.5)(logits)
#   logits = keras.layers.Dense(
#     units=len(classes),
#     activation="softmax"
#   )(logits)


# if you changed the MLP architecture during training, change it also here:
# class MLP(pl.LightningModule):
#     def __init__(self, input_size, xcol='emb', ycol='avg_rating'):
#         super().__init__()
#         self.input_size = input_size
#         self.xcol = xcol
#         self.ycol = ycol
#         self.layers = nn.Sequential(
#             nn.Linear(self.input_size, 1024),
#             #nn.ReLU(),
#             nn.Dropout(0.2),
#             nn.Linear(1024, 128),
#             #nn.ReLU(),
#             nn.Dropout(0.2),
#             nn.Linear(128, 64),
#             #nn.ReLU(),
#             nn.Dropout(0.1),
#
#             nn.Linear(64, 16),
#             #nn.ReLU(),
#
#             nn.Linear(16, 1)
#         )
#
#     def forward(self, x):
#         return self.layers(x)
