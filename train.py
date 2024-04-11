from config import *
from utils import *
from model import *
from transformers import AdamW, get_linear_schedule_with_warmup
import torch
from sklearn import metrics
from sklearn.metrics import classification_report
from sklearn.metrics import f1_score
from sklearn.metrics import confusion_matrix
from tqdm import tqdm

import warnings
# 忽略特定类型的警告
warnings.filterwarnings("ignore", category=UserWarning)

# 设置随机种子 确保每次运行的条件(模型参数初始化、数据集的切分或打乱等)是一样的
import random
np.random.seed(1)
torch.manual_seed(1)
torch.cuda.manual_seed_all(1)
torch.backends.cudnn.deterministic = True  # 保证每次结果一样

epsilon = 1e-7

def f1_loss(y_true, y_pred):
    if type(y_true) != 'torch.Tensor':
        y_true = torch.tensor(y_true)
    if type(y_pred) != 'torch.Tensor':
        y_pred = torch.tensor(y_pred)
    #y_true:真实标签0或者1；y_pred:为正类的概率
    loss = 2*torch.sum(y_true*y_pred)/torch.sum(y_true+y_pred)+epsilon
    return -loss

#返回文本型报告或者字典型报告
def evaluate(pred, true, target_names=None, output_dict=False):     #sample_weight：1 维数组，不同数据点在评估结果中所占的权重digits：评估报告中小数点的保留位数，
    return classification_report(
        true,
        pred,
        target_names=target_names,          #类别名字
        output_dict=output_dict,
        zero_division=0,
        digits = 3
    )

def save_model_results(train_history):
    results = {
        'learning rate': LR,  # 保存模型的参数
        'optimizer_name': OPTIMIZER,
        'train_history': train_history,
    }
    with open('result.txt', 'a', encoding="utf-8") as f:
        f.write('模型训练：')
    with open('result.txt', 'a', encoding="utf-8") as f:
        f.write(str(results))

class f1_Loss(nn.Module):
    """
       tp = torch.sum(y_true * y_pred)
        fp = torch.sum((1 - y_true) * y_pred)
        fn = torch.sum(y_true * (1 - y_pred))
    """
    def __init__(self, epsilon=1e-7, reduction='elementwise_mean'):
        super().__init__()
        self.epsilon = epsilon
        self.reduction = reduction

    def forward(self, y_true, y_pred):
        loss = -2 * torch.sum(y_true * y_pred) / torch.sum(y_true + y_pred) + epsilon    #(1类的损失)
        if self.reduction == 'elementwise_mean':
            loss = torch.mean(loss)
        elif self.reduction == 'sum':
            loss = torch.sum(loss)
        return loss  # 返回平均损失

class BCEFocalLoss(torch.nn.Module):
    """
    二分类的Focalloss alpha 固定
    """
    def __init__(self, gamma=2, alpha=0.25, reduction='elementwise_mean'):
        super().__init__()
        self.gamma = gamma
        self.alpha = alpha
        self.reduction = reduction

    def forward(self, _input, target):
        pt = torch.sigmoid(_input)
        alpha = self.alpha
        loss = - alpha * (1 - pt) ** self.gamma * target * torch.log(pt) - \
               (1 - alpha) * pt ** self.gamma * (1 - target) * torch.log(1 - pt)
        if self.reduction == 'elementwise_mean':
            loss = torch.mean(loss)
        elif self.reduction == 'sum':
            loss = torch.sum(loss)
        return loss


def objective(trial):
    # Generate the model.
    model = define_model(trial).to(DEVICE)

    # Generate the optimizers.
    optimizer_name = trial.suggest_categorical("optimizer", ["Adam", "RMSprop", "SGD"])
    lr = trial.suggest_float("lr", 1e-5, 1e-3, log=True)
    optimizer = getattr(optim, optimizer_name)(model.parameters(), lr=lr)

    # Get the FashionMNIST dataset.
    train_loader, valid_loader = get_mnist()

    # Training of the model.
    for epoch in range(8):
        model.train()
        for batch_idx, (data, target) in enumerate(train_loader):

            data, target = data.view(data.size(0), -1).to(DEVICE), target.to(DEVICE)

            optimizer.zero_grad()
            output = model(data)
            loss = F.nll_loss(output, target)
            loss.backward()
            optimizer.step()

        # Validation of the model.
        model.eval()
        correct = 0
        with torch.no_grad():
            for batch_idx, (data, target) in enumerate(valid_loader):
                data, target = data.view(data.size(0), -1).to(DEVICE), target.to(DEVICE)
                output = model(data)
                # Get the index of the max log-probability.
                pred = output.argmax(dim=1, keepdim=True)
                correct += pred.eq(target.view_as(pred)).sum().item()

        accuracy = correct / min(len(valid_loader.dataset), N_VALID_EXAMPLES)

        trial.report(accuracy, epoch)
        # Handle pruning based on the intermediate value.
        if trial.should_prune():
            raise optuna.exceptions.TrialPruned()

    return accuracy



if __name__ == '__main__':
    # storage_name = "sqlite:///my_optuna.db"
    # study = optuna.create_study(
    #     pruner=optuna.pruners.MedianPruner(n_warmup_steps=10), direction="maximize",
    #     study_name="para-cl", storage=storage_name, load_if_exists=True
    # )
    # study.optimize(objective, n_trials=200)
    # exit()
    #
    # best_params = study.best_params
    # best_value = study.best_value
    # print("\n\nbest_value = " + str(best_value))
    # print("best_params:")
    # print(best_params)
    # exit()


    df = pd.read_csv('./data/dataset_v2.csv', header=0)
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
            print(i + 2)
    paras = []
    for i in range(len(texts)):
        texts[i] = re.sub(r'第\d+段\s\:', '', texts[i])
        paras.append([texts[i], tags[i]])

    #'''train_loader存入数据对象'''
    train, dev, test = build_dataset(paras)
    train_loader = data.DataLoader(Dataset(list_para_label=train), batch_size=BATCH_SIZE,shuffle=False)
    dev_loader = data.DataLoader(Dataset(list_para_label=dev), batch_size=BATCH_SIZE, shuffle=False)
    test_loader = data.DataLoader(Dataset(list_para_label=test), batch_size=BATCH_SIZE, shuffle=False)

    model = Model().to(DEVICE)          # Model_cnn  ，Model_dpcnn，Model_rcnn ，Model_rnn，Model
    if OPTIMIZER == 'Adam':
        #optimizer = torch.optim.Adam(model.parameters(), lr=LR)
        # optimizer = torch.optim.Adam([{'params': model.bert.parameters(),'lr': LR},
        #                              {'params': model.fc.parameters()}],lr = 2e-4)

        optimizer = torch.optim.Adam([{'params': model.bert.parameters(), 'lr': LR}],lr=5e-5)  #model_cnn

    elif OPTIMIZER == 'AdamW':
        param_optimizer = list(model.named_parameters())
        no_decay = ['bias', 'LayerNorm.bias', 'LayerNorm.weight']             #一些偏置项和层归一化层的参数并不需要进行权重衰减
        optimizer_grouped_parameters = [
            {'params': [p for n, p in param_optimizer if not any(nd in n for nd in no_decay)], 'weight_decay': 0.01},
            {'params': [p for n, p in param_optimizer if any(nd in n for nd in no_decay)], 'weight_decay': 0.0}]

        optimizer = AdamW(optimizer_grouped_parameters, lr=LR)

        total_step = len(train_iter) * config.num_epochs
        num_warmup_steps = round(total_step * 0.1)
        scheduler = get_linear_schedule_with_warmup(optimizer, num_warmup_steps=num_warmup_steps,
                                                    num_training_steps=total_step)     #get_cosine_with_hard_restarts_schedule_with_warmup    get_cosine_schedule_with_warmup
    loss_fn = nn.CrossEntropyLoss()  #初始化
    #loss_fn = BCEFocalLoss()

    best_metric = float('0')   #float('inf')
    total_batch = 0

    model.train()
    train_history = []
    flag = False      #记录模型训练是否还能提升效果
    last_improve = 0
    with tqdm(total=EPOCH*len(train_loader)) as pbar:
        for e in range(EPOCH):

            y_true = []
            y_pred = []
            total_loss = 0

            for b, (input, mask, target) in enumerate(train_loader):
                input, mask, target = input.to(DEVICE), mask.to(DEVICE), target.to(DEVICE)

                pred = model(input, mask)
                loss = loss_fn(pred, target)

                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
                # scheduler.step(

                y_pred += torch.argmax(pred, dim=1).data.tolist()
                y_true += target.data.tolist()

                total_loss += loss.item()

                '''新增进度条'''
                pbar.set_description('processing')
                pbar.update(1)
                ''''''

                dev_y_true = []
                dev_y_pred = []
                total_batch += 1

                if total_batch % 25 == 0:
                    with torch.no_grad():
                        for _, (dev_input, dev_mask, dev_target) in enumerate(dev_loader):
                            dev_input, dev_mask, dev_target = dev_input.to(DEVICE), dev_mask.to(DEVICE), dev_target.to(DEVICE)
                            dev_pred = model(dev_input, dev_mask)
                            dev_pred_ = torch.argmax(dev_pred, dim=1)

                            dev_y_pred += dev_pred_.data.tolist()
                            dev_y_true += dev_target.data.tolist()
                            # print(dev_pred_.cpu().data.numpy())
                            # print(dev_target.cpu().data.numpy())
                        print(confusion_matrix(dev_y_true, dev_y_pred))
                        print(f1_score(dev_y_true, dev_y_pred, average='macro'))
                        macro_f1 = f1_score(dev_y_true, dev_y_pred, average='macro')
                        # print(f1_score(dev_y_true, dev_y_pred, average='micro'))
                        # print(f1_score(dev_y_true, dev_y_pred, average='weighted'))
                        dev_report = evaluate(dev_y_true, dev_y_pred, output_dict=True)

                    print(
                        '>> epoch:', e,
                        'loss:', round(loss.item(), 5),
                        'dev_acc:', dev_report['accuracy'],
                    )

                    # 每多少轮输出在训练集和验证集上的效果
                    train_acc = metrics.accuracy_score(y_true, y_pred)
                    if macro_f1 > best_metric:
                        print('>> epoch:', e, 'best_metric:', best_metric,'now_metric:', macro_f1)
                        best_metric = macro_f1
                        torch.save(model, MODEL_DIR + f'model_{e}.pth')
                        num_params = sum(p.numel() for p in model.parameters())
                        last_improve = total_batch
                    # msg = 'Iter: {0:>4},  Train Loss: {1:>5.2},  Train Acc: {2:>6.2%}'  # round(loss.item(), 5)
                    # print(msg.format(total_batch, loss.item(), train_acc))

                # if total_batch - last_improve > REQUIRE_BATCH:
                #     print('有无作用')
                #     flag = True

            train_history.append({
                'epoch': e,
                #'train_loss': train_loss,
                'model_name':model_name,
                'model Parameters':f"{num_params/1e6:.1f} M",
                'train_accuracy': metrics.accuracy_score(y_true, y_pred),
                'dev_macro_f1': f1_score(dev_y_true, dev_y_pred, average='macro'),
                'dev_accuracy': dev_report['accuracy'],
                'dev_confusion_matrix': confusion_matrix(dev_y_true, dev_y_pred)
            })

            print('>> total_data_acc:',metrics.accuracy_score(y_true, y_pred),'total_loss:', total_loss)

            if flag:
                break

    save_model_results(train_history=train_history)




