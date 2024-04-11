import torch
DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'    #self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')   # 设备

BERT_PAD_ID = 0
TEXT_LEN = 350          #统一的文本长度，限制；并不是随便取的，需要做一个简单的数据统计，挑选

model_name = 'bert-base-cased'    #使用deberta-v3安装sentencepiece：    deberta_v3_base
BERT_MODEL = '../huggingface_demo/{}/'.format(model_name)   #config.bert_path = './bert-base-chinese'
MODEL_DIR = './output/bert-base/'
LR = 1.5e-5                                                   #config.learning_rate = 5e-5   1e-4
EPOCH = 8
OPTIMIZER = 'Adam'   # else AdamW 优化器的选择
use_GPU = True

REQUIRE_BATCH = 750
EMBEDDING_DIM = 768   #large语言模型改为 1024   768
#hidden_size = 1024   #config.hidden_size
NUM_CLASSES = 2     #config.num_classes
BATCH_SIZE = 32    #32

# self.model_name = 'bert'
# self.train_path = dataset + '/data/train.txt'                                # 训练集
# self.dev_path = dataset + '/data/dev.txt'                                    # 验证集
# self.test_path = dataset + '/data/test.txt'                                  # 测试集
# self.save_path = dataset + '/saved_dict/' + self.model_name + '.ckpt'        # 模型训练结果
#
# self.require_improvement = 1000                                 # 若超过1000batch效果还没提升，则提前结束训练
# self.num_epochs = 3                                             # epoch数
# self.batch_size = 128                                           # mini-batch大小
# self.dropout = 1
# self.pad_size = 32                                              # 每句话处理成的长度(短填长切)

# from transformers import BertTokenizer,BertModel
# from transformers import DebertaTokenizer, DebertaModel
# from transformers import AutoModel, AutoTokenizer
# import torch
#
# # downloading the models
# # tokenizer = BertTokenizer.from_pretrained(BERT_MODEL)
# # model = BertModel.from_pretrained(BERT_MODEL)
# tokenizer = AutoTokenizer.from_pretrained(BERT_MODEL)
# model = AutoModel.from_pretrained(BERT_MODEL)
# # tokenizing the input text and converting it into pytorch tensors
# inputs = tokenizer(["The cat cought the mouse", "This is the second sentence"], return_tensors="pt", padding=True)
# # pass through the model
# outputs = model(**inputs)
# print(outputs)


