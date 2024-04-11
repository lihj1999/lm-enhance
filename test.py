from config import *
from utils import *
from model import *

from sklearn import metrics
from sklearn.metrics import classification_report
from sklearn.metrics import f1_score
from sklearn.metrics import confusion_matrix

import matplotlib.pyplot as plt
import seaborn as sns

# 或者忽略所有警告
import warnings
warnings.filterwarnings("ignore")

# 设置随机种子 确保每次运行的条件(模型参数初始化、数据集的切分或打乱等)是一样的
import random
np.random.seed(1)
torch.manual_seed(1)
torch.cuda.manual_seed_all(1)
torch.backends.cudnn.deterministic = True  # 保证每次结果一样

def evaluate(pred, true, target_names=None, output_dict=False):     #sample_weight：1 维数组，不同数据点在评估结果中所占的权重digits：评估报告中小数点的保留位数，
    return classification_report(
        true,
        pred,
        target_names=target_names,          #类别名字
        output_dict=output_dict,
        zero_division=0,
        digits = 3
    )

if __name__ == '__main__':
    df = pd.read_csv('./data/final_dataset.csv', header=0)    #final_dataset   dataset_v2
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

    # '''train_loader存入数据对象'''
    train, dev, test = build_dataset(paras)

    train_loader = data.DataLoader(Dataset(list_para_label=train), batch_size=BATCH_SIZE, shuffle=False)
    dev_loader = data.DataLoader(Dataset(list_para_label=dev), batch_size=BATCH_SIZE, shuffle=False)
    test_loader = data.DataLoader(Dataset(list_para_label=test), batch_size=BATCH_SIZE, shuffle=False)


    model = torch.load(MODEL_DIR + 'model_5.pth', map_location=DEVICE)

    from sklearn.cluster import KMeans
    from sklearn.decomposition import PCA
    import matplotlib.pyplot as plt
    x = np.empty((0, 350), dtype=int)
    pca = PCA(n_components=2,whiten=True)
    print(len(test_loader))
    n =0
    for b, (input, mask, target) in enumerate(train_loader):
        input, mask, target = input.to(DEVICE), mask.to(DEVICE), target.to(DEVICE)
        x = np.vstack((x, input.cpu().numpy()))
        n += len(target)
    print(n)
    pca_vecs = pca.fit_transform(x)
    print(len(pca_vecs))
    label = []
    for i in range(len(train)):
        label.append(train[i][1])
    # 初始化K-Means模型，设置聚类簇数
    from sklearn.mixture import GaussianMixture
    # 使用高斯混合模型进行聚类
    gmm = GaussianMixture(n_components=3, random_state=42,covariance_type='tied', tol=1e-3, max_iter=100)
    labels = gmm.fit_predict(pca_vecs)
    #kmeans = KMeans(n_clusters=3,init='k-means++', n_init=20, max_iter=500, tol=1e-3, random_state=2)

    #对降维后的数据进行K-Means聚类


    # kmeans.fit(pca_vecs)
    # labels = kmeans.labels_


    # 设置图像宽度和高度（单位是英寸）
    #plt.figure(figsize=(3, 3))
    # 可视化聚类结果
    colors = ['r', 'g', 'b']
    for i in range(3):  # 假设有三个聚类簇
        cluster_points = pca_vecs[labels == i]  # 获取属于第 i 个聚类簇的数据点
        plt.scatter(cluster_points[:, 0], cluster_points[:, 1], c=colors[i], label=f'Cluster {i + 1}')

    # scatter = plt.scatter(pca_vecs[:, 0], pca_vecs[:, 1], c=labels, cmap='viridis', s=10)
    plt.legend()
    plt.tight_layout()
    plt.show()
    exit()
    # plt.title('PCA dimension reduction analysis',fontsize=6)
    # plt.xlabel('Principal Component 1',fontsize=6)
    # plt.ylabel('Principal Component 2',fontsize=6)

    # 添加图例，根据类别设置标签
    # legend_labels = ['Class 0', 'Class 1']  # 根据实际情况设置类别标签
    # plt.legend(handles=scatter.legend_elements()[0], labels=legend_labels,fontsize=24)
    # plt.tight_layout()
    # plt.show()
    # plt.close()
    # exit()

    # #计算模型参数量
    # count_parameters(model)
    # print(count_parameters(model))
    # exit()
    model.eval()

    y_pred = []
    y_true = []

    with torch.no_grad():
        for b, (input, mask, target) in enumerate(test_loader):
            input, mask, target = input.to(DEVICE), mask.to(DEVICE), target.to(DEVICE)
            test_pred = model(input, mask)

            test_pred_ = torch.argmax(test_pred, dim=1)

            y_pred += test_pred_.data.tolist()
            y_true += target.data.tolist()

    print(evaluate(y_true,y_pred))

    #混肴矩阵可视化
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(8, 6))
    sns.set(font_scale=1.2)
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", cbar=False)
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.title('Confusion Matrix')
    plt.show()
