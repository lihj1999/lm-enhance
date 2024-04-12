import regex as re
import pandas as pd
import ast
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from transformers import BertTokenizer
from transformers import BertModel
from transformers import logging
logging.set_verbosity_error()


import matplotlib.pyplot as plt

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimSun']

# 年份列表
years = list(range(2013, 2024))

# 论文发表数量列表
paper_counts = [1105, 1441, 1834, 2420, 2851, 3798, 5050, 6099, 7883, 8883,9654]

# 创建折线图
#plt.figure(figsize=(8, 6))  # 调整图形大小
plt.plot(years, paper_counts, marker='o', color='skyblue', linestyle='-')

# 添加标题和标签
plt.xlabel('发表年份',fontsize = 12)
plt.ylabel('文献数量',fontsize = 12)
# 设置 x 轴刻度间隔
plt.xticks(years)
plt.legend(loc="upper right")
plt.legend(['web of science数据库'])

# 显示图形
plt.grid(axis="y")  # 显示网格线
plt.tight_layout()  # 调整布局以减少空白
plt.show()
exit()

df = pd.read_csv('final_dataset.csv', header=0)
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
print(labels.count(1))
print(labels.count(0))


data = []
for i in range(len(texts)):
    texts[i] = re.sub(r'第\d+段\s\:','',texts[i])
    data.append([texts[i],tags[i]])

#合成段落的文本集
syn_para = []
for i in range(len(texts)):
    if tags[i] == 1:
        syn_para.append(texts[i])

df_syn = pd.DataFrame(data,columns = ['text_para','tag'])
# df_distri = pd.DataFrame({
#     "name":['target para','Not target para'],
#     "number":[labels.count(1),labels.count(0)]
# })
# fig = make_subplots(
#     rows=1, cols=2,
#     specs=[[{"type": "pie"}, {"type": "bar"}]]
# )
#
# #合成段落与非合成段落在数据集中的分布
# # 创建饼图
# #fig1 = go.Figure(data=[go.Pie(labels=df_distri['name'], values=df_distri['number'])])
# fig1 = go.Pie(labels=list(df_distri['name']), values=list(df_distri['number']))
#
# # # 设置文本位置和信息
# # fig1.update_traces(
# #     textposition='inside',  # 文本显示在内部
# #     textinfo='percent+label',  # 显示百分比和标签
# #     insidetextorientation='horizontal'  # 文本方向
# # )
# # # 设置图形大小和 DPI
# # fig1.update_layout(
# #     width=800,  # 设置图形宽度(像素)
# #     height=600,  # 设置图形高度
# #     autosize=False,  # 禁用自动调整大小
# #     margin=dict(l=0, r=0, t=0, b=0),  # 设置图形边距
# #     paper_bgcolor='white',  # 设置背景颜色
# #     plot_bgcolor='white',  # 设置绘图区域背景颜色
# #     template='plotly',  # 使用 Plotly 默认模板
# # )
#
# # 创建柱状图
# bar_colors = ['turquoise','dodgerblue']
# #fig2 = go.Figure(data=[go.Bar(x=['synthetic para', 'Not synthetic para'], y=[tags.count(1),tags.count(0)])])
# fig2 = go.Bar(x=['Synthetic para (2076)', 'Not synthetic para (19629)'], y=[tags.count(1),tags.count(0)],marker_color=bar_colors,name='1')
#
# # # 设置图形布局
# # fig2.update_layout(
# #     title='Target paragraph count in dataset',  # 设置图形标题
# #     xaxis_title='target',  # 设置X轴标题
# #     #yaxis_title='count',  # 设置Y轴标题
# #     xaxis=dict(tickmode='array', ticktext=['synthetic para', 'Not synthetic para']),
# #     yaxis=dict(tickmode='linear'),  # 设置Y轴刻度模式为线性
# # )
#
# fig.add_trace(fig1, row=1, col=1)
# fig.add_trace(fig2, row=1, col=2)
# fig.update_traces(
#     textposition='inside',  # 文本显示在内部
#     textinfo='percent+label',  # 显示百分比和标签
#     insidetextorientation='horizontal',  # 文本方向,
#     hole=0.4,#空白区域
#     row=1, col=1
# )
# # 设置子图1的大小
# fig.update_xaxes(row=1, col=1, domain=[0, 0.4])  # 控制子图1的横向大小
# fig.update_yaxes(row=1, col=1, domain=[0, 1])  # 控制子图1的纵向大小
#
# # 设置子图2的大小
# fig.update_xaxes(row=1, col=2, domain=[0.5, 1])  # 控制子图2的横向大小
# fig.update_yaxes(row=1, col=2, domain=[0, 1])  # 控制子图2的纵向大小
#
# fig.update_xaxes(row=1, col=2,showline=True,linewidth=2,linecolor='black',mirror=True)
# fig.update_yaxes(title_text='count',showline=True,linewidth=2,linecolor='black',mirror=True, row=1, col=2)
#
# # 设置子图的标题
# fig.update_layout(
#     #paper_bgcolor='white',  # 设置绘图区域的背景颜色为白色
#     plot_bgcolor='white',  # 设置图形的背景颜色为白色
#     annotations=[
#         dict(
#             text="Target documennt distribution in dataset",  # 标题文本
#             x=0.11,  # 标题文本的X位置（相对于子图）
#             y=1.05,  # 标题文本的Y位置（相对于子图）
#             xref="paper",  # X位置的参考系（"paper"表示相对于图形的左侧边缘）
#             yref="paper",  # Y位置的参考系（"paper"表示相对于图形的顶部边缘）
#             showarrow=False,  # 不显示箭头
#             font=dict(size=17)  # 标题文本的字体大小
#         ),
#         dict(
#             text="Target para in dataset",  # 标题文本
#             x=0.82,  # 标题文本的X位置（相对于子图）
#             y=1.05,  # 标题文本的Y位置（相对于子图）
#             xref="paper",  # X位置的参考系（"paper"表示相对于图形的左侧边缘）
#             yref="paper",  # Y位置的参考系（"paper"表示相对于图形的顶部边缘）
#             showarrow=False,  # 不显示箭头
#             font=dict(size=17)  # 标题文本的字体大小
#         )
#     ]
# )
# # 设置图例名称
# fig.update_traces(showlegend=False, row=1, col=1)
# fig.update_traces(showlegend=False, row=1, col=2)
#
# # # 更新布局和更新布局
# # fig.update_layout(height=700, showlegend=False)
# # #fig.write_image('../pic/subplots_8.png', scale=10)
# fig.show()


import nltk
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS as sklearn_stopwords
from nltk.corpus import stopwords as nltk_stopwords
from nltk.corpus import wordnet
from nltk import pos_tag
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.probability import FreqDist
from wordcloud import WordCloud
nltk_stopwords = set(nltk_stopwords.words('english'))
merged_stopwords = set(sklearn_stopwords).union(nltk_stopwords)
stopwords = set(merged_stopwords)
more_stopwords = {'c', 'h', 'w', 'n', 'x', 'b', 'v', 'l','nm','oh','3d','2d','n.','In','fig','figure','As','IR','⋯'}  # 领域自身调整  'O','1','2','3','4','5','6'
stopwords = stopwords.union(more_stopwords)
#分词并词性还原
wnl = WordNetLemmatizer()
def get_wordnet_pos(tag):
    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return wordnet.ADV
    else:
        return None
def reback(sentence):
    tokens = nltk.word_tokenize(sentence)
    tagged_sent = nltk.pos_tag(tokens)
    lemmatized_words = []
    for tag in tagged_sent:
        wordnet_pos = get_wordnet_pos(tag[1]) or wordnet.NOUN
        lemmatized_words.append(wnl.lemmatize(tag[0].lower(), pos=wordnet_pos))
    return lemmatized_words
    #return " ".join(lemmatized_words)
text_example = "NLTK is a leading platform for building Python programs to work with human language data."
reback(text_example)
def is_english_word(sentence,index = 0):
    tokens = nltk.word_tokenize(sentence)
    # 将字符串转换为小写字母，以确保与WordNet中的词形匹配
    word = tokens[index]
    word = word.lower()
    # 使用NLTK的词形归并器将单词还原为基本形式
    lemmatizer = nltk.stem.WordNetLemmatizer()
    lemma = lemmatizer.lemmatize(word,pos = wordnet.ADV)
    # 判断还原后的单词是否在WordNet中存在
    if len(wordnet.synsets(lemma))>0:
        return True
    else:
        return False

allwords = []
for para in tqdm(texts, desc="Spliting Texts", unit="para"):
    lemmatized_words = reback(para)
    for w in lemmatized_words:
        if w not in stopwords:  #and is_english_word(w)
            allwords.append(w)
print(len(set(allwords)))
print(FreqDist(allwords).most_common(4000))
exit()

# synwords = []
# for para in tqdm(syn_para, desc="Spliting Texts", unit="para"):
#     lemmatized_words = reback(para)
#     for w in lemmatized_words:
#         if w not in stopwords and is_english_word(w) and not re.search('\d',w):
#             synwords.append(w)
# print(len(set(synwords)))
# print(FreqDist(synwords).most_common(200))

mostcommon = FreqDist(allwords).most_common(100)
print(FreqDist(allwords).most_common(200))
data = " ".join(allwords[:100])
wordcloud = WordCloud(width=1600, height=800, background_color='white', stopwords=stopwords).generate(str(data))
fig = plt.figure(figsize=(30,10), facecolor='white')
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis('off')
plt.title('Top 100 Most Common Words in texts', fontsize=50)
plt.tight_layout(pad=0)
plt.show()

mostcommon_small = FreqDist(allwords).most_common(30)
x, y = zip(*mostcommon_small)
#plt.figure(figsize=(30,12))
plt.margins(0.01)
plt.bar(x, y)
plt.xlabel('Words', fontsize=16)
plt.ylabel('Frequency of Words', fontsize=16)
plt.yticks(fontsize=14)
plt.xticks(rotation=20, fontsize=11)
plt.tight_layout(pad=0)
plt.title('Freq of 30 Most Common Words in synthetic texts', fontsize=16)
plt.tight_layout()
plt.show()
exit()

#普通绘制词云，未进行小写转换和词性还原
def plot_wordcloud(text, mask=None, max_words=80, max_font_size=100, figure_size=(30.0, 10.0),
                   title=None, title_size=50, image_color=False):
    stopwords = set(merged_stopwords)
    more_stopwords = {'C','H','W','N','X','B','nm','ii'}  #领域自身调整
    stopwords = stopwords.union(more_stopwords)
    wordcloud = WordCloud(background_color='white',
                          stopwords=stopwords,
                          max_words=max_words,
                          max_font_size=max_font_size,
                          random_state=42,
                          width = 1600,
                          height = 800,
                          mask=mask)
    wordcloud.generate(str(text))
    plt.figure(figsize=figure_size)
    if image_color:
        image_colors = ImageColorGenerator(mask)
        plt.imshow(wordcloud.recolor(color_func=image_colors), interpolation="bilinear")
        plt.title('Top 100 Most Common Words in texts', fontdict={'size': title_size,
                                   'verticalalignment': 'bottom'})
    else:
        plt.imshow(wordcloud)
        plt.title('Top 100 Most Common Words in texts', fontdict={'size': title_size, 'color': 'black',
                                   'verticalalignment': 'bottom'})
    plt.axis('off')
    plt.tight_layout(pad=0)
    plt.show()
text_data = "\n".join(texts)
#plot_wordcloud(text_data)
syn_data = "\n".join(syn_para)
plot_wordcloud(syn_data)


#bert分词
# def count_token_lengths(texts):
#     tokenizer = BertTokenizer.from_pretrained('../Huggingface_demo/huggingface/matscibert')
#     token_lengths = []
#     for text in tqdm(texts, desc="Processing Texts", unit="para"):   #tqdm(texts, desc="Processing Texts", unit="text")
#         # 对文本进行分词并添加特殊标记
#         tokens = tokenizer.tokenize(tokenizer.decode(tokenizer.encode(text)))
#         num_tokens = len(tokens)
#         token_lengths.append(num_tokens)
#     return token_lengths

# result = count_token_lengths(texts)
# print(result)
# print(len(result))
# median = np.median(result)
# print(max(result))
# print(median)
# hist, bins, _ = plt.hist(result,bins=40,rwidth = 0.8,color = 'skyblue')
#
# # 添加频数标签
# for i in range(len(hist)):
#     plt.text(bins[i] + 50, hist[i], f"{int(hist[i])}", ha='center', va='bottom')
#
# plt.xticks(np.arange(0,4000,100))
# plt.xlim(20, 4200)
# plt.xlabel("Value")
# plt.ylabel("Frequency")
# plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用中文字体，替换成你电脑上支持的字体
# plt.title("文本段落长度统计直方图 (21705)")
# plt.show()


# print(len(syn_para))
# result = count_token_lengths(syn_para)
# print(result)
# print(len(result))
# median = np.median(result)
# print(max(result))
# print(median)
# hist, bins, _ = plt.hist(result,bins=np.arange(0,500,50),rwidth= 0.8,color = 'skyblue')   # edgecolor='black'
# for i in range(len(hist)):
#     plt.text(bins[i]+25, hist[i], f"{int(hist[i])}", ha='center', va='bottom')
# plt.xticks(np.arange(0,500,50))
# plt.xlim(0, 500)
# plt.xlabel("Value")
# plt.ylabel("Frequency")
# plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用中文字体，替换成你电脑上支持的字体
# plt.title("合成文本段落长度统计直方图 (2076)")
# plt.show()
exit()

