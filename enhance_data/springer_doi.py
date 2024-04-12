from habanero import Crossref
import pandas as pd
from bs4 import BeautifulSoup
import time
import requests
from glob import glob
import csv
import unicodedata
import re
from bs4.element import NavigableString,Tag,Script,ProcessingInstruction
import copy
import nltk
from nltk.corpus import wordnet
from pylatexenc.latex2text import LatexNodes2Text
import warnings
warnings.filterwarnings("ignore")
cr = Crossref()

#选出2000年后的发表的文献
def get_year(index):
    flag = 0
    try:
        doi = list1[i]
        article = cr.works(ids=doi)
        year = article['message']['issued']['date-parts'][0][0]
        print(year)
        list2.append(int(year))      #字符型转为整数型
    except:
        dic[index] = doi
        return 1

# df = pd.read_csv('count_publisher1134.csv', header=0)
# list1 = list(df['doi'])
# list2 = []
# dic = dict()
# for i in range(len(list1)):
#     flag = get_year(i)
#     with open('result.csv','w',newline="")as f:
#         writer = csv.writer(f)
#         for i, j in zip(list(dic.keys()), list(dic.values())):  # 为什么不是紧凑的数据格式
#             data = ','.join(j)
#             writer.writerow([i] + [j])
#         # #或者
#         # for i, j in dic:  # 为什么不是紧凑的数据格式
#         #     writer.writerow([i,j])
#     if flag == 1:
#         list2.append('10000')
#         continue
#
# print(len(list1))
# print(len(list2))
# print(list2)0
# df.insert(3, 'year', list2)
# df = df.loc[df['year'].astype(int)>2000]
# df.to_csv('count_year_publiser1134.csv', index=False)

def get_url(df):
    list_doi = df['doi']
    list_urls = ['https://link.springer.com/article/{doi}'.format(doi=list_doi[i]) for i in range(len(list_doi))]
    #list_urls = ['http://api.springernature.com/metadata/xml?q=doi:{doi}&api_key={apikey}'.format(doi=list_doi[i],apikey='fff1a02034ab463e11fa60f5fe9718d1') for i in range(len(list_doi))]
    #list_urls = ['http://api.springernature.com/meta/v2/pam?q=doi:{doi}&api_key={apikey}'.format(doi=list_doi[i],apikey='fff1a02034ab463e11fa60f5fe9718d1') for i in range(len(list_doi))]
    df.insert(4, 'url', list_urls)
    df.to_csv('count_year_url_publiser1134.csv', index=False)

#下载xml
# def download_xml(df):
#     list_urls, list_years, list_dois = df['url'] ,df['year'] ,df['doi']
#     #初始状态
#     list_flags = [0]*len(df['url'])
#     print(list_flags)
#
#     api_key = 'fff1a02034ab463e11fa60f5fe9718d1'
#     headers = {
#         "Accept": "text/html",
#         "X-ELS-APIKey": api_key
#     }
#     for i in range(len(list_urls)):   #len(list_urls)
#         try:
#             response = requests.get(list_urls[i], headers=headers)
#             soup = BeautifulSoup(response.text, 'html.parser')
#             # print(soup.prettify())
#
#             # 删除所有的figure
#             figure_tags = soup.find_all('figure')
#             for j in range(len(figure_tags)):
#                 figure_tags[j].extract()
#
#             # 删除所有参考文献上标
#             ref_tags = soup.select('sup a')
#             # print(ref_tags)
#             # print(len(ref_tags))
#             # exit()
#             for k in range(len(ref_tags)):
#                 ref_tags[k].extract()
#
#             main_text = soup.select('div .main-content section .c-article-section__content')  # 如果查找器找不到对应tag，可以尝试将get到的网页打印出来看看节点标签;    为什么写class="main-content"不行
#             #section = main_text[1].select('h3')
#             #print(len(main_text))
#
#             rename = 'DOI_10.1007_' + list_urls[i][list_urls[i].rfind('/') + 1:] + '_' + str(list_years[i])
#             # 改不下去了，不知道为什么原soup对象的tag和main_text不改变,即使改变也无用
#             for l in range(len(main_text)):
#                 # print(type(main_text[i]))
#                 # print(type(ptag_merge_h2tag(main_text[i])))
#                 new_tag = soup.new_tag(ptag_merge_h3tag(main_text[l]))
#                 main_text[l].replace_with(new_tag)  # 如何返回一个bs4.element.Tag类型       其实也可以不用再将修改后main_text[i]内容置入main_text[i],直接分部存入文档就行   继续打印main_text[i],其实其值是并未改变的，改变的是Beautifuisoup对象，oldtag会从Beautifulsoup对象中删除，newtag会被添加到oldtag位置上。
#                 # print(main_text[i].prettify())
#                 # print(ptag_merge_h2tag(main_text[i]).prettify())
#                 # print('.....')
#                 with open(rename + '.html', 'ab') as f:
#                     f.write(str(ptag_merge_h3tag(main_text[l])).encode())
#             list_flags[i] = 1
#             print(list_urls[i])
#             #print(list_flags)
#
#             # print(main_text[i].prettify())
#             # with open(rename + '.html', 'ab') as f:
#             #     f.write(str(main_text[i]).encode())
#         except:
#             print('download error')
#             list_flags[i] = 2
#             print(list_flags)
#     return list_flags

#将段落总结（h3tag）的内容嵌入段落内部（ptag）
def ptag_merge_h3tag(tag):
    soup = BeautifulSoup(str(tag),'html.parser')
    #print(soup.prettify())
    #注意顺序，认为五级标题和四级标题比三级标题更接近段落节点
    h5_tags = soup.find_all('h5')
    if h5_tags:
        print('有五级标题')
        for i in range(len(h5_tags)):
            p_tag = h5_tags[i].find_next_sibling()
            if p_tag:
                if p_tag.name == 'p':
                    if isinstance(h5_tags[i].contents[-1], NavigableString):
                        h5_tags[i].contents[-1].replace_with(h5_tags[i].contents[-1].string + '. ')   # 标题文本的字符串形式影响小
                    elif isinstance(h5_tags[i].contents[-1], Tag):
                        h5_tags[i].contents[-1].append('. ')
                    for content in reversed(list(h5_tags[i].contents)):
                        p_tag.contents[0].insert_before(content)
                    h5_tags[i].extract()
                else:
                    h5_tags[i].extract()
            else:
                h5_tags[i].extract()

    h4_tags = soup.find_all('h4')
    if h4_tags:
        print('有四级标题')
        for i in range(len(h4_tags)):
            p_tag = h4_tags[i].find_next_sibling()
            if p_tag:
                # print(p_tag.text)
                # print(h4_tags[i].text)
                if p_tag.name == 'p':
                    if isinstance(h4_tags[i].contents[-1], NavigableString):
                        h4_tags[i].contents[-1].replace_with(h4_tags[i].contents[-1].string + '. ')   # 标题文本的字符串形式影响小
                    elif isinstance(h4_tags[i].contents[-1], Tag):
                        h4_tags[i].contents[-1].append('. ')
                    for content in reversed(list(h4_tags[i].contents)):
                        p_tag.contents[0].insert_before(content)
                    h4_tags[i].extract()
                else:
                    h4_tags[i].extract()
            else:
                h4_tags[i].extract()


    # h3_tags = soup.find_all('h3')
    # for i in range(len(h3_tags)):
    #     p_tag = h3_tags[i].find_next_sibling()
    #     if p_tag.name == 'p':
    #         # print(type(p_tag.contents[0]))                      #也是<class 'bs4.element.NavigableString'>对象
    #         # print(h3_tags[i].find_next_sibling())
    #         # print(type(h3_tags[0]), type(p_tag))
    #         h3_content = h3_tags[i].text + '. '
    #         # h3_tags[i].string = ''                              #不能用.text方法，只能用.string方法才能表示NavigableString对象内存放的文本内容 ，这种方法只能清空h3标签的文本内容，不能真正删除h3标签
    #         h3_tags[i].extract()  # 删除、移除标签
    #         # p_tag.contents[0].string.replace_with(h3_content + '. ' + str(p_tag.contents[0]))            #p_tag.contents[0]是一个<class 'bs4.element.NavigableString'>对象
    #         # p_tag.contents[0] = h3_content + '.' + str(p_tag.contents[0])
    #         # print(type(p_tag.contents[0]),type(p_tag.contents[1]))
    #         # print(p_tag.prettify())
    #         # print('....................exit...................')
    #         p_tag.contents[0].insert_before(h3_content)
    #     else:
    #         h3_tags[i].extract

    h3_tags = soup.find_all('h3')
    for i in range(len(h3_tags)):
        p_tag = h3_tags[i].find_next_sibling()
        if p_tag:
            if p_tag.name == 'p':
                if isinstance(h3_tags[i].contents[-1], NavigableString):
                    h3_tags[i].contents[-1].replace_with(h3_tags[i].contents[-1].string + '. ')  # 标题文本的字符串形式影响小
                elif isinstance(h3_tags[i].contents[-1], Tag):
                    h3_tags[i].contents[-1].append('. ')
                for content in reversed(list(h3_tags[i].contents)):
                    p_tag.contents[0].insert_before(content)
                h3_tags[i].extract()
            else:
                h3_tags[i].extract()
        else:
            h3_tags[i].extract()

    if len(soup.contents) == 1:
        return soup.contents[0]


def test_download(url):
    api_key = 'fff1a02034ab463e11fa60f5fe9718d1'
    headers = {
        "Accept": "text/xml",
        'Authorization':f'Bearer{api_key}'
    }
    params = {'api_key': api_key}
    response = requests.get(url, params = params)
    soup = BeautifulSoup(response.text, 'html.parser')
    print(soup.prettify())
    main_text = soup.select('div .main-content')
    with open('flag_download.html', 'wb+') as f:
        f.write(soup.prettify().encode())
    print('...下载完成...')

def orignaltext_batch_process():
    list_html = glob('./1134-process/*.html')
    print(len(list_html))
    dois = [list_html[i][list_html[i].find('_')+1:list_html[i].rfind('_')] for i in range(len(list_html))]
    dois = [dois[i].replace('_','/') for i in range(len(dois))]
    years = [list_html[i][list_html[i].rfind('_')+1:list_html[i].rfind('.')] for i in range(len(list_html))]
    with open('Dataset_springer_1134.csv', 'a', newline="", encoding='utf-8') as f:  # 写改为追加的方式；‘ab+’以二进制的形式写入
        writer = csv.writer(f)
        header = 'doi', 'year', 'count', 'number', 'paras', 'label'
        writer.writerow(header)
    for j in range(len(list_html)):            #len(list_html)
        print(dois[j])
        number, paras = 0, []
        with open(list_html[j],'r',encoding = 'utf-8') as f:
            soup = BeautifulSoup(f.read(), features='lxml')

        #清理包含链接节点的段落
        for element in soup.find_all("p"):
            if element.find_all('a'):
                # print([i.string for i in element.find_all('a')])
                # print(len([i.string for i in element.find_all('a')]))
                for child in element.find_all('a'):                                  # find_next_sibling和next_sibling，前一个只找寻tag节点
                    #if str(child.previous_sibling.string)[-1]=='(' and str(child.next_sibling.string)[0]==')':
                    #try:
                    if child.previous_sibling and child.next_sibling:
                        if find_count(str(child.previous_sibling.string),'(')>find_count(str(child.previous_sibling.string),')') and find_count(str(child.next_sibling.string),'(')<find_count(str(child.next_sibling.string),')'):
                            child.previous_sibling.replace_with(str(child.previous_sibling.string)[:str(child.previous_sibling.string).rfind('(')])            #本来想用节点替换的方式，结果发现tag中包含的字符串（即Navigablestring对象）不能编辑,但是可以被替换成其它的字符串
                            #print(str(child.next_sibling.string)[str(child.next_sibling.string).find(')')+1:])
                            child.next_sibling.replace_with(str(child.next_sibling.string)[str(child.next_sibling.string).find(')')+1:])
                            child.extract()
                            continue

                        #换个思路，可能某一个方向能够欺骗代码的逻辑，那就加一层从两个方向来进行检查。对这种多个链接节点和混杂在一起的字符串节点的括号内，需要删除所有的字符串节点，并替换括号。链接节点是必定功能删除的; 最后会剩下一个（链接节点）的形式，因此不用删除括号
                        if find_count(str(child.previous_sibling.string), '(')>find_count(str(child.previous_sibling.string), ')'):
                            #两者顺序翻转逻辑也可以通，一种是前向一种是后向，现为前向
                            if str(child.next_sibling).find(')') >= 0:  # find返回的是列表索引位置
                                child.next_sibling.replace_with(str(child.next_sibling.string)[str(child.next_sibling.string).find(')') + 1:])
                                child.previous_sibling.replace_with(str(child.previous_sibling.string)[:str(child.previous_sibling.string).rfind('(')])
                                child.extract()
                                continue
                            if ')' not in str(child.text):
                                for target in list(child.next_siblings):
                                    # print(target)
                                    # print(str(target).find(')') >= 0)       #find的是字符串的位置，没找到返回-1         注意find函数是节点的find还是字符串的find
                                    if target.name == 'a' or str(target).find(')') >= 0:                 #就用target，反而解决了target是tag对象在调string方法时报错，反正html也是<>
                                        break
                                    target.extract()
                                child.extract()
                                continue
                            else:
                                child.previous_sibling.replace_with(str(child.previous_sibling.string)[:str(child.previous_sibling.string).rfind('(')])
                                child.extract()
                                continue

                        #有可能之前的链接节点都没处理，默认前兄弟节点的（）是相等的，或者链接节点有一个（
                        if find_count(str(child.next_sibling.string),'(') < find_count(str(child.next_sibling.string), ')'):
                            # print(22222)
                            # print(child.text)
                            # print(child.next_sibling)
                            # print(child.previous_sibling)
                            for target in list(child.previous_siblings):
                                if str(target).find('(') >= 0:  # find返回的是列表索引位置
                                    if isinstance(target, NavigableString):
                                        child.next_sibling.replace_with(str(child.next_sibling.string)[str(child.next_sibling.string).find(')') + 1:])
                                        target.replace_with(str(target.string)[:str(target.string).rfind('(')])
                                        child.extract()
                                        break
                                    elif target.name == 'a':
                                        child.next_sibling.replace_with(str(child.next_sibling.string)[str(child.next_sibling.string).find(')') + 1:])
                                        target.extract()
                                        child.extract()
                                        break
                                else:
                                    target.extract()
                            continue

                        if find_count(str(child.previous_sibling.string), '(') == find_count(str(child.previous_sibling.string), ')') or find_count(str(child.next_sibling.string),'(') == find_count(str(child.next_sibling.string), ')'):  # 判别条件方宽松一些
                            if re.match('[fF]ig', child.get_text()):
                                if isinstance(child.next_sibling, NavigableString):
                                    child.next_sibling.replace_with('Figure' + str(child.next_sibling.string))
                                    child.extract()
                                    continue
                                elif isinstance(child.previous_sibling, NavigableString):
                                    child.previous_sibling.replace_with(str(child.previous_sibling.string) + 'Figure')
                                    child.extract()
                                    continue
                            if re.match('[tT]ab', child.get_text()):
                                if isinstance(child.next_sibling, NavigableString):
                                    child.next_sibling.replace_with('Table' + str(child.next_sibling.string))
                                    child.extract()
                                    continue
                                elif isinstance(child.previous_sibling, NavigableString):
                                    child.previous_sibling.replace_with(str(child.previous_sibling.string) + 'Table')
                                    child.extract()
                                    continue
                    else:
                        print('段首节点' + child.text)
                        if re.match('[fF]ig', child.get_text()):
                            child.next_sibling.replace_with('Figure' + str(child.next_sibling.string))
                            child.extract()
                            continue
                        if re.match('[tT]ab', child.get_text()):
                            child.next_sibling.replace_with('Table' + str(child.next_sibling.string))
                            child.extract()
                            continue
                    child.extract()
                    # except Exception as e:
                    #     print(str(e))
                    #     print('>>>>>>>>>>>>修改错误<<<<<<<<<<')
                #print(element.get_text())
                print(element.get_text().replace("\n", " ").replace("\t",""))
                print('<<<<<<<<<<<<<>>>>>>>>>>>>>>>')

        number, paras = 0, []
        counts = len(soup.find_all('p'))
        print(counts)
        # 删除不包含字母和数字的中括号及其内容
        pattern = r'\[[^\w\d]*?\]'
        pattern1 = r'\[[\-\d\,\ ]*?\]'
        pattern2 = r'\b(and|or)\s+(\w+-\w+)'
        pattern3 = r'\b\w+-\w+\b'
        # 删除特殊字符
        pattern4 = r'\(ref. \)'
        pattern5 = r'\bFig.\s'
        pattern6 = r'\(\)' + '|' r'\[\s*[-,]+\s*\]'
        #10.1134/S1066362221040056
        for i,element in enumerate(soup.find_all("p")):
            '''只有参考文献的链接节点有中括号'''
            paragraph = re.sub(pattern1, '', re.sub(pattern, '', unicodedata.normalize('NFKC', element.text.replace("\n", " ").replace( "\t", ""))))
            if re.findall(pattern2, paragraph):             #or re.findall(pattern3, paragraph)
                #print(paragraph)
                paragraph = para_clean(paragraph)
                #处理A-B格式的符合词汇
                #print(paragraph)
                print('--------------')
            #paras.append('第{}段 :'.format(i+1) + paragraph)
            paras.append('第{}段 :'.format(i + 1) + re.sub(pattern6, '', re.sub(pattern5, ' ', re.sub(pattern4, '', unicodedata.normalize('NFKC',element.get_text().replace("\n"," ").replace( "\t", ""))))) + '.')
            #paras.append(unicodedata.normalize('NFKC',element.get_text()))
            number += 1
        if number != len(paras):
            print('{}分段错误'.format(url))
            # continue

        data = []
        data.append([dois[j], years[j], counts, len(paras), paras, number * [0]])
        with open('Dataset_springer_1134.csv', 'a', newline="", encoding='utf-8') as f:  # 写改为追加的方式；‘ab+’以二进制的形式写入
            writer = csv.writer(f)
            for line in data:
                writer.writerow(line)


# def find_count(str,chars):                 #因为有一部分文献链接节点外，圆括号和方括号
#     count0,count1 = 0,0
#     for element in str:
#         if element == chars[0]:
#             count0 += 1
#         if element == chars[1]:
#             count1 += 1
#     return count0,count1

def find_count(str,char):
    count = 0
    for element in str:
        if element == char:
            count += 1
    return count

def test(path):
    number, paras = 0, []
    with open(path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    # 清理包含链接节点的段落
    a = 0
    count_number = 0
    for element in soup.find_all("p"):
        number = 0
        a += len(element.find_all('a'))
        if element.find_all('a'):
            print('yes')
            # print([i.string for i in element.find_all('a')])
            # print(len([i.string for i in element.find_all('a')]))
            for child in element.find_all('a'):  # find_next_sibling和next_sibling，前一个只找寻tag节点
                try:
                    if find_count(str(child.previous_sibling.string), '(') > find_count(str(child.previous_sibling.string), ')') and find_count(str(child.next_sibling.string),'(') < find_count(str(child.next_sibling.string), ')'):
                        child.previous_sibling.replace_with(str(child.previous_sibling.string)[:str(child.previous_sibling.string).rfind('(')])  # 本来想用节点替换的方式，结果发现tag中包含的字符串（即Navigablestring对象）不能编辑,但是可以被替换成其它的字符串
                        # print(str(child.next_sibling.string)[str(child.next_sibling.string).find(')')+1:])
                        child.next_sibling.replace_with(str(child.next_sibling.string)[str(child.next_sibling.string).find(')')+1:])
                        child.extract()
                        print(1)
                        number += 1
                        continue
                    if find_count(str(child.previous_sibling.string), '(') == find_count(str(child.previous_sibling.string), ')') and find_count(str(child.next_sibling.string),'(') == find_count(str(child.next_sibling.string), ')'):
                        if re.match('[fF]ig', child.get_text()):
                            child.next_sibling.replace_with('Fig' + str(child.next_sibling.string))
                            child.extract()
                            print(2)
                            number += 1
                            continue
                        if re.match('[tT]ab', child.get_text()):
                            child.next_sibling.replace_with('Table' + str(child.next_sibling.string))
                            child.extract()
                            print(3)
                            number += 1
                            continue

                    # 换个思路，可能某一个方向能够欺骗代码的逻辑，那就加一层从两个方向来进行检查。对这种多个链接节点和混杂在一起的字符串节点的括号内，需要删除所有的字符串节点，并替换括号。链接节点是必定功能删除的; 最后会剩下一个（链接节点）的形式，因此不用删除括号
                    if find_count(str(child.previous_sibling.string), '(') > find_count(str(child.previous_sibling.string), ')'):
                        number += 1
                        print(4)
                        # print(str(child.next_sibling).find(')'))
                        # print(str(child.next_sibling))

                        '''如果有多个节点，则第一个节点的下一个兄弟节点绝不会包括括号'''
                        if str(child.next_sibling).find(')') >= 0:         #find返回的是列表索引位置
                            print(7)

                            child.next_sibling.replace_with(str(child.next_sibling.string)[str(child.next_sibling.string).find(')')+1:])
                            child.previous_sibling.replace_with(str(child.previous_sibling.string)[:str(child.previous_sibling.string).rfind('(')])

                            # print(str(child.previous_sibling))
                            # print(str(child.next_sibling))

                            child.extract()
                            #print(unicodedata.normalize('NFKC',element.text.replace("\n", " ").replace("\t","")))
                            continue

                        for target in list(child.next_siblings):
                            print(str(target).replace("\n", " ").replace("\t"," "))
                            '''print(target.find(')'))与print(target.find(')')>=0)的区别，一个是bs4节点的查找函数一个是字符串的查找函数'''
                            if target.name == 'a' or str(target).find(')')>=0:
                                break
                            target.extract()
                    if find_count(str(child.next_sibling.string), '(') < find_count(str(child.next_sibling.string),')'):
                        number += 1
                        print(5)

                        if str(child.next_sibling).find(')') >= 0:         #find返回的是列表索引位置
                            print(7)
                            child.next_sibling.replace_with(str(child.next_sibling.string)[str(child.next_sibling.string).find(')')+1:])
                            child.previous_sibling.replace_with(str(child.previous_sibling.string)[:str(child.previous_sibling.string).rfind('(')])
                            child.extract()
                            continue

                        for target in list(child.previous_siblings):
                            # print(target.string)
                            # print(str(target.string).find('('))            #find的是字符串的位置，没找到返回-1,后续判别条件也可写为！=-1         注意find函数是节点的find还是字符串的find
                            # if str(target.string).find('(') >= 0:           # 就用target不用反而解决了target是tag对象在调string方法时报错，反正html也是<>
                            #     break
                            if target.name == 'a' or str(target).rfind('(')>=0:
                                break
                            target.extract()
                except Exception as e:
                    print(str(e))
                    print('>>>>>>>>>>>>修改错误<<<<<<<<<<')
                child.extract()
                print(6)
                number += 1
        #print(element.get_text().replace("\n", ""))

        #删除不包含字母和数字的中括号及其内容
        pattern = r'\[[^\w\d]*?\]'
        pattern1 = r'\[[\-\d\,\ ]*?\]'

        '''只有参考文献的链接节点有中括号'''
        print(re.sub(pattern1,'',re.sub(pattern, '',unicodedata.normalize('NFKC',element.text.replace("\n", " ").replace("\t","")))))
        # print(unicodedata.normalize('NFKC',element.text.replace("\n", " ").replace("\t","")))
        # print(repr(element.get_text()))             #检验特殊字符,输出特殊字符
        count_number += number
        print('<<<<<<<<<<<<<{}>>>>>>>>>>>>>>>'.format(number))
    print(a)
    print(count_number)

    number, paras = 0, []
    counts = len(soup.find_all('p'))
    print(counts)
    for element in soup.find_all("p"):
        paras.append(unicodedata.normalize('NFKC',element.text.replace("\n", " ").replace("\t","")))
        number += 1
    if number != len(paras):
        print('{}分段错误'.format(url))
        # continue

def download_html(df):
    list_urls, list_years, list_dois = df['url'] ,df['year'] ,df['doi']
    #初始状态
    list_flags = [0]*len(df['url'])
    print(list_flags)

    api_key = 'fff1a02034ab463e11fa60f5fe9718d1'
    headers = {
        "Accept": "text/html",
        "X-ELS-APIKey": api_key
    }
    for i in range(len(list_urls)):   #len(list_urls)
        try:
            response = requests.get(list_urls[i], headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            rename = 'DOI_10.1007_' + list_urls[i][list_urls[i].rfind('/') + 1:] + '_' + str(list_years[i])
            if soup.select('div .main-content section .c-article-section__content'):
                with open(rename + '.html', 'wb') as f:
                    f.write(response.content)
                    #f.write(soup.prettify().encode())
                list_flags[i] = 1
                print(list_urls[i])
        except:
            print('download error')
            list_flags[i] = 2
            print(list_flags)
    return list_flags


def preprocess():        #10.1134/S0036023619090195复杂
    df = pd.read_csv('count_year_url_publiser1134.csv', header=0)
    df_doi = df['doi']
    vals = [{}]*len(df)
    df.insert(loc=len(df.columns),column='name_dicts', value=vals)   #loc=0
    df.insert(loc=len(df.columns), column='compound_dicts', value=vals)
    list_html = glob('./1134/*.html')
    print(len(list_html))

    dois = [list_html[i][list_html[i].find('_') + 1:list_html[i].rfind('_')] for i in range(len(list_html))]
    dois = [dois[i].replace('_', '/') for i in range(len(dois))]
    years = [list_html[i][list_html[i].rfind('_') + 1:list_html[i].rfind('.')] for i in range(len(list_html))]
    for j in range(len(list_html)):  # len(list_html)
        print(dois[j])
        index = df[df.doi == dois[j]].index.tolist()[0]
        # print(index)

        number, paras = 0, []
        #try:
        with open(list_html[j], 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), features='lxml')

        if soup.find_all('ol'):
            print('有列表项节点ol')
        if soup.find_all('ul'):
            print('有列表项节点ul')

        for link in soup.find_all(["br", "hr"]):
            link.extract()
        for link in soup.find_all(text="\n"):
            link.extract()

        #移除空白节点
        for element in soup(text=lambda text: isinstance(text, str) and text.strip() == ''):
            element.extract()

        # #适用于preprocess的文本
        #main_text = soup.select('.c-article-section__content')
        main_text = soup.select('div .main-content section .c-article-section__content')          #div .main-content section .c-article-section__content
        # for tag in main_text:
        #     # print(len(tag.contents))
        #     # print([content.name for content in tag.contents])
        #     if len(tag.contents) != [content.name for content in tag.contents].count('p'):
        #         print('并不是全p')

        # 删除所有的figure和table
        figure_tags = soup.select('div .main-content section .c-article-section__figure')       #属性不一定要全部取得，尤其是中间有空格
        for m in range(len(figure_tags)):
            figure_tags[m].extract()
        table_tags = soup.select('div .main-content section .c-article-table')
        for n in range(len(table_tags)):
            table_tags[n].extract()
        img_tags = soup.select('div .main-content section img')
        for g in range(len(img_tags)):
            img_tags[g].extract()
        table_container = soup.select('div .main-content section .c-article-table-container')
        for h in range(len(table_container)):
            table_container[h].extract()

        # 删除所有参考文献上标
        ref_tags = soup.select('sup a')
        for k in range(len(ref_tags)):
            ref_tags[k].extract()
        equ_tags = soup.select('.c-article-equation')
        for l in range(len(equ_tags)):
            print('有等式')
            equ_tags[l].extract()

        #网页会自动渲染临近的节点，给他们之间加上空格。本地的没有    只处理b节点这种极为特殊的节点
        b_tags = [tag for tag in list(soup.select('.c-article-section__content b')) if tag.parent.name == 'p']   #div .main-content section 因为要包括摘要部分
        for i in range(len(b_tags)-1):
            #print(soup.select('div .c-article-section__content')[0].prettify())
            if b_tags[i].next_sibling and b_tags[i].text == 'L':
                # print(b_tags[i].previous_sibling)
                # print(b_tags[i].next_sibling)
                # print((b_tags[i].next_sibling.name == 'sup' and b_tags[i].next_sibling.contents[0].name == 'b'))
                if b_tags[i].next_sibling == b_tags[i+1]:
                    if is_english_word(b_tags[i].text,-1) and is_english_word(b_tags[i+1].text):
                        b_tags[i].append(' ' + b_tags[i+1].text)
                        b_tags[i+1].extract()          #extract()和clear()的差别
                    else:
                        b_tags[i].append(b_tags[i + 1].text)
                        b_tags[i+1].extract()
                #b标签在前，sup或sub标签在后，且sup和sub标签有直接子节点b节点
                elif b_tags[i].next_sibling.name == 'sup' and b_tags[i].next_sibling.contents[0].name == 'b' and len(b_tags[i].next_sibling.contents) == 1:
                    # # 创建一个新的字符串节点
                    # string_node = soup.new_string(b_tags[i].next_sibling.text)
                    # # 替换<b>标签节点为字符串节点
                    # b_tags[i].next_sibling.contents[0].replace_with(string_node)
                    # sup_tag = b_tags[i].next_sibling
                    # b_tags[i].next_sibling.extract()
                    # b_tags[i].contents[-1].insert_after(sup_tag)
                    # #print(soup.select('div .c-article-section__content')[0].find_all('b')[1].prettify())
                    # #print(b_tags[i].next_sibling)
                    b_tags[i].string.replace_with(b_tags[i].string+b_tags[i].next_sibling.text)
                    b_tags[i].next_sibling.extract()
                elif b_tags[i].next_sibling.name == 'sub' and b_tags[i].next_sibling.contents[0].name == 'b':
                    # string_node = soup.new_string(b_tags[i].next_sibling.text)
                    # b_tags[i].next_sibling.contents[0].replace_with(string_node)
                    # sub_tag = b_tags[i].next_sibling
                    # b_tags[i].next_sibling.extract()
                    # b_tags[i].contents[-1].insert_after(sub_tag)
                    b_tags[i].string.replace_with(b_tags[i].string + b_tags[i].next_sibling.text)
                    b_tags[i].next_sibling.extract()
                #print(soup.select('div .c-article-section__content')[0].prettify())

        # 处理ol-li-ul-li列表形式的文章，非p节点             顺序问题，若是放于div节点之前则报错
        for tag in main_text:
            if [content.name for content in tag.contents].count('ol') or [content.name for content in tag.contents].count('ul'):  # ['p']*len(tag.contents)
                diff_p = [content for content in tag.contents if content.name == 'ol' or content.name == 'ul']  # and  content.name != 'p'   否定用and，肯定用or
                for diff in diff_p:
                    tag = diff              #ol节点或者ul节点,应将p节点顺序添加至此节点之后
                    print(diff.name)
                    for children_li in reversed(diff.contents):
                        if len(children_li.find_all('p')) == 1:
                            parent_tag = tag
                            child_tag = children_li.find_all('p')[0]
                            parent_tag.insert_after(child_tag)
                        elif len(children_li.find_all('p')) > 1:
                            li_list = children_li.find_all('p')
                            new_tag = li_list[0]
                            '''for content in list(old_tag.contents)：
                                这段代码首先使用list()函数将old_tag.contents转换为列表类型，生成一个包含所有子节点的列表。然后，使用for循环遍历列表中的每个元素。这种方式可以在循环中修改节点的结构，例如添加、删除或替换节点。
                                for content in old_tag.contents：
                                这段代码直接遍历old_tag.contents，它返回一个可迭代的对象，每次迭代返回一个子节点。在循环中，你可以访问子节点的属性或执行其他操作，但不能直接修改节点的结构。如果在循环中修改节点的结构，例如添加、删除或替换节点，可能会导致迭代过程中的错误或意外结果。'''
                            for p_index in range(1, len(li_list)):
                                old_tag = li_list[p_index]
                                for content in list(old_tag.contents):
                                    children_li.find_all('p')[0].contents[-1].insert_after(content)
                            parent_tag = tag
                            child_tag = new_tag
                            parent_tag.insert_after(child_tag)
                    tag.extract()

                        # 经典错误，因为在循环内部每次都使用了children_li.find_all('p')，导致每次循环结束后都会重新查询一次li内部的p节点，且append形式导致会新增p节点的数量     因此需要习惯使用变量
                        # for p_index in range(len(children_li.find_all('p')) - 1, 0, -1):
                        #     print(children_li.find_all('p')[p_index].text)
                        #     new_tag.append(children_li.find_all('p')[p_index])

                        # #将p节点插入父节点的兄弟节点的位置
                        # for child2 in child1.contents:
                        #     parent_tag = child1  # 存储父标签
                        #     tag = child2
                        #     parent_tag.insert_after(tag)  # 将子节点插入到父标签后
                        #     parent_tag.extract()
                        # #合并同名子节点
                        # indexs = [index for index, value in enumerate(child1.contents) if value.name == 'p']
                        # p = child1.contents[indexs[0]]
                        # print(len(indexs))
                        # for i in range(1,len(indexs),-1):
                        #     p.insert_after(child1.contents[i])


        #处理指代消解的问题  进行替换  即使是紧密相连的两个b节点，也不认为其是一个变量（代词）,         要在合并h4,h3这样的节点前施行     应在原文删减实行之前执行
        # l_tag = soup.select('.c-article-section__content b')       #text = 'L'
        # l = soup.find(text = 'L')          #soup.find用text搜寻，返回的也是字符串
        # print(l_tag[174])
        # print(l_tag[174].previous_sibling)
        # print(l)
        # print(l.previous_sibling)
        # print(type(l))
        # print(type(l.parent))

        #print(soup.find_all(id = 'Abs1-content'))


        metals = ['Si', 'K', 'Ce', 'La', 'Mo', 'Fe', 'Ru', 'W', 'Ba', 'Ga', 'Sm', 'Ho', 'Zr', 'Be', 'Y', 'Cd', 'As', 'Yb', 'V', 'Er', 'Ca', 'Ag', 'Cu', 'Na', 'Dy', 'U', 'Tb', 'Mg', 'Co', 'Zn', 'Li', 'Mn', 'In', 'Ni', 'Sr', 'Eu', 'Nd', 'Sc', 'Th', 'Gd', 'Bi', 'Cs', 'Pr', 'Al', 'Pb', 'Hg']


        pattern_item = r'[A-Za-z\)\[\]\·\-\{](\d|\∞|}n|]n|\)n|\·){1}((\.\d+)|[A-Za-z\(\)\[\]|\{|\}])+'    #r'[A-Za-z\(\)\[\]\·]+(\d|\∞|}n|]n|\)n){1}[A-Za-z\(\)\[\]\·]*' 避免(2017).这样的错误指代词 10.1007/s10876-020-01848-x  结尾部分该不该加*
        pattern_metal = r'(?:{})'.format('|'.join(metals))
        pattern_1 = r'\(\S+\)'  #[Sc(HCOO)(bdc)]
        patt_equ = r'\s*=\s*(\S+)\s+'
        patt_equ_split = r'([\S|*]+)\s*=\s*(\S+)'
        patt_compounds = r'[\d|N](,[\d|N](′)*)*-[A-Za-z]{2,}'

        #避免b节点和字符串节点紧贴，且无空格
        string_b_tags = [tag for tag in soup.find_all('b',text=lambda text: text is not None) if isinstance(tag.previous_sibling, NavigableString)]
        for tag in string_b_tags:
            if tag.previous_sibling.string[-1] == '(':
                pass
            elif tag.previous_sibling.string[-1] != ' ':
                if not tag.next_sibling:
                    tag.previous_sibling.string.replace_with(tag.previous_sibling.string + ' ')
                elif tag.next_sibling.string[0]==',' or tag.next_sibling.string[0]=='.' or (tag.next_sibling.string[0] == ' ' and is_english_word(tag.next_sibling.string,0)):
                    tag.previous_sibling.string.replace_with(tag.previous_sibling.string + ' ')
                else:     #此b节点在化学式之后作为一个代词
                    pass

        # 避免sub节点和字符串节点紧贴，且无空格
        string_b_tags = [tag for tag in soup.find_all('sub', text=lambda text: text is not None) if isinstance(tag.previous_sibling, NavigableString)]
        for tag in string_b_tags:
            if tag.previous_sibling.string[-1] == ' ':
                tag.previous_sibling.string.replace_with(tag.previous_sibling.string[:len(tag.previous_sibling.string)-1])

        # 避免sup节点和字符串节点紧贴，且无空格
        string_b_tags = [tag for tag in soup.find_all('sup', text='′') if isinstance(tag.previous_sibling, NavigableString)]
        for tag in string_b_tags:
            if tag.previous_sibling.string[-1] == ' ':
                tag.previous_sibling.string.replace_with(
                    tag.previous_sibling.string[:len(tag.previous_sibling.string) - 1])


        #配合物的一些错误描述，(2, 2'-bipy)(H2O)] 多了一个空格
        compounds_excess = [tag for tag in soup.find_all(text=lambda text: text is not None and re.search(patt_compounds, text)) if tag.string]
        #print(len(compounds_excess))
        for tag in compounds_excess:
            tag.string.replace_with(re.sub(r'(N|\d),(\s+)(N|\d)',r'\1,\3',tag.string))


        #解码latex文本
        math_tags = [tag for tag in soup.find_all('span',class_="mathjax-tex") if tag.next_sibling and tag.previous_sibling]
        patt_latex = r'[\s|_]+'
        for tag in math_tags:
            latex_expr = tag.text
            # 使用 pylatexenc 进行 LaTeX 表达式的解析
            unicode_text = LatexNodes2Text().latex_to_text(latex_expr)
            # print(unicode_text)
            # print(re.sub(patt_latex,'',unicode_text))
            tag.insert_after(re.sub(patt_latex,'',unicode_text))
            tag.extract()

        # abs = soup.select('#Abs1-content')
        # print(len(abs))
        # print(abs[0].text)


        #sub节点后面直接跟b节点，这样可能会造成prerocess处理失误，也有可能造成切分句子误切
        sub_b_tags = [tag for tag in soup.find_all('sub') if tag.next_sibling and tag.previous_sibling]      #已经保证了sub节点不是b节点的子节点
        for tag in sub_b_tags:
            if isinstance(tag.next_sibling, Tag) and tag.next_sibling.name == 'b' :  #sub节点内不是b节点，如果是b节点那么相当于两者是一个整体
                # print(tag.previous_sibling)
                # print(tag.previous_sibling.previous_sibling)
                # print(tag.previous_sibling.previous_sibling.previous_sibling)
                # print(list(tag.next_siblings))
                if tag.find_all():
                    if isinstance(tag.find_all()[0], Tag) and tag.find_all()[0].name == 'b':
                        continue
                else:
                    tag.insert_after(' ')
            elif isinstance(tag.next_sibling.next_sibling, Tag) and tag.next_sibling.next_sibling.name == 'b' and tag.next_sibling.string == '(':
                tag.next_sibling.string.replace_with(' (')

        #sup和sub节点的处理 10.1007/s12039-015-0966-z
        sup_sub_tags = [tag for tag in soup.find_all('sup') if tag.next_sibling and tag.previous_sibling]
        for tag in sup_sub_tags:
            if tag.previous_sibling.string:
                if tag.previous_sibling.string[-1].isspace() and not tag.previous_sibling.string[-2].isdigit():
                    tag.previous_sibling.string.replace_with(tag.previous_sibling.string[:-1])

        #sub节点后的字符串节点莫名出现多余的空格
        sub_blank_tags = [tag for tag in soup.find_all('sub') if tag.next_sibling and tag.previous_sibling]
        for tag in sub_blank_tags:
            if tag.next_sibling.string:
                if tag.next_sibling.string[0] == ' ':
                    next_string = ''
                    for pre_next in (list(tag.next_siblings)):
                        if isinstance(pre_next, NavigableString):
                            next_string = next_string + re.sub(r'\s+[∙·⋅]\s+', '·', re.sub(r'\s+', ' ',pre_next.string))  # 不能用+=,因为存入字符串的顺序要使得线存入的字符串压入最末尾
                        elif isinstance(pre_next, Tag) and pre_next.name == 'sub':
                            next_string = next_string + re.sub(r'\s+[∙·⋅]\s+', '·', re.sub(r'\s+', ' ', pre_next.text))
                        elif isinstance(pre_next, Tag) and pre_next.name == 'sup':
                            next_string = next_string + re.sub(r'\s+[∙·⋅]\s+', '·', re.sub(r'\s+', ' ', pre_next.text))
                        elif isinstance(pre_next, Tag) and pre_next.name == 'i':
                            next_string = next_string + re.sub(r'\s+[∙·⋅]\s+', '·', re.sub(r'\s+', ' ', pre_next.text))
                        elif isinstance(pre_next, Tag) and pre_next.name == 'b':
                            next_string = next_string + re.sub(r'\s+[∙·⋅]\s+', '·', re.sub(r'\s+', ' ', pre_next.text))
                        elif isinstance(pre_next, Tag) and pre_next.name == 'span' and pre_next['class'][0] == 'c-stack':
                            next_string = next_string + re.sub(r'\s+[∙·⋅]\s+', '·', re.sub(r'\s+', ' ', pre_next.text))
                        else:
                            break
                    if re.search(pattern_item,next_string[1:next_string[1:].find(' ')+1]):
                        tag.next_sibling.string.replace_with(tag.next_sibling.string[1:])

        #字符串节点的一些空格处理
        patt_string_spacing = r'\d(,\d)*-\s+'   #r'\d(,\d)*- [A-Za-z]+'
        text_spacing = [tag for tag in soup.find_all(text=lambda text: text is not None and re.search(patt_string_spacing, text)) if tag.string]
        for tag in text_spacing:
            string = re.search(patt_string_spacing, tag.string)[0]
            new_string = string.replace(' ','')
            tag.string.replace_with(tag.string.replace(string, new_string))

        # 字符串节点的一些大括号{处理
        patt_string_brace = r'[A-Za-z]*\{\s+'
        text_brace = [tag for tag in soup.find_all(text=lambda text: text is not None and re.match(patt_string_brace, text)) if tag.string]
        for tag in text_brace:
            text = re.match(patt_string_brace, tag.string).group(0).strip()
            tag.string.replace_with(tag.string.replace(re.match(patt_string_brace, tag.string).group(0),text))

        #namely{[Hg(3-pmpmd)I2]·H2O)}n   10.1007/s11243-019-00369-5
        patt_str_brace = r'namely\{'
        txt_brace = [tag for tag in soup.find_all(text=lambda text: text is not None and re.search(patt_str_brace, text)) if tag.string]
        for tag in txt_brace:
            tag.string.replace_with(tag.string.replace('namely','namely '))


        #b节点中的and文本进行切分
        patt_text_and = r'\s+(and)\s+'  # .在此种情况下只能是句号不可能是逗号
        spilt_text_and = [tag for tag in soup.find_all('b', text=lambda text: text is not None and re.search(patt_text_and, text)) if tag.string]
        #print(len(spilt_text_and))
        for tag in spilt_text_and:
            # print(tag.string)
            # print(re.search(patt_text_and, tag.string).span())
            # print(tag.string[:re.search(patt_text_and, tag.string).span()[0]])
            # print(tag.string[re.search(patt_text_and, tag.string).span()[0]:re.search(patt_text_and, tag.string).span()[1]])
            # print(tag.string[re.search(patt_text_and, tag.string).span()[1]:])
            text = tag.string[re.search(patt_text_and, tag.string).span()[0]:re.search(patt_text_and, tag.string).span()[1]]
            b_next_node = soup.new_tag('b')
            b_next_node.string = tag.string[re.search(patt_text_and, tag.string).span()[1]:]
            tag.string.replace_with(tag.string[:re.search(patt_text_and, tag.string).span()[0]])
            tag.insert_after(b_next_node)
            tag.insert_after(text)

        #清理不合理的节点文本
        IUPAC_tags = [tag for tag in list(soup.find_all(text = lambda text: text is not None and 'hydrate' in text)) if tag.string]
        patt1 = r'(\d+)\s+(hydrate)\b'
        for i in IUPAC_tags:
            text = i.string
            strs = re.sub(patt1,r'\1\2', text)
            if i.parent:
                i.string.replace_with(strs)
        patt2 = r'\s+[∙·⋅]\s+'
        point_tags = [tag for tag in list(soup.find_all(text = lambda text: text is not None and re.search(patt2,text))) if tag.string]
        for i in point_tags:
            i.string.replace_with(re.sub(patt2, '·',i.string))
        # patt3 = r'\S+\s+[–-]'
        # line_tag = [tag for tag in list(soup.find_all(text=lambda text: text is not None and re.search(patt3,text))) if tag.string]
        # for i in line_tag:
        #     i.string.replace_with(re.sub(patt3,'–', i.string))
        patt3_supp = r'\s+[–-−]\s+'  # 将search修改一下
        line_tag = [tag for tag in list(soup.find_all(text=lambda text: text is not None and re.search(patt3_supp, text))) if tag.string]
        for i in line_tag:
            i.string.replace_with(re.sub(patt3_supp, '–', i.string))
        #与patt3的不一样的处理   #10.1007/s12039-015-0966-z
        patt4 = r'[–-]\s+'
        line_tags = [tag for tag in list(soup.find_all(text=lambda text: text is not None and re.match(patt4, text))) if tag.string]
        for i in line_tags:
            text = i.string[0] + i.string[2:-1]
            i.string.replace_with(text)
        patt4_supp = r'\(\S+[–-]\s+'
        line_tags_supp = [tag for tag in list(soup.find_all(text=lambda text: text is not None and re.match(patt4_supp, text))) if tag.string]
        for i in line_tags_supp:
            text = i.string.replace(' ','',1)
            i.string.replace_with(text)

        patt5 = r'[∙·⋅]\s+'       #r'^[∙·⋅]\s+'
        kpoint_tags1 = [tag for tag in list(soup.find_all(text=lambda text: text is not None and re.search(patt5, text)))if tag.string]
        for i in kpoint_tags1:
            i.string.replace_with(re.sub(patt5, '·', i.string))

        patt6 = r'\s+[∙·⋅]'
        kpoint_tags2 = [tag for tag in list(soup.find_all(text=lambda text: text is not None and re.search(patt6, text))) if tag.string]
        for i in kpoint_tags2:
            i.string.replace_with(re.sub(patt6, '·', i.string))

        iupac_tags = [tag for tag in list(soup.find_all('sub',text = '2')) if tag.next_sibling and tag.previous_sibling]
        for tag in iupac_tags:
            string = ''
            wd =''
            # if not tag.next_sibling.string or not tag.previous_sibling.string:
            #     continue
            if tag.next_sibling.string[0] == 'O' and tag.previous_sibling.string[-1] == 'H':
                for i in tag.previous_siblings:
                    if isinstance(i, NavigableString):
                        string = re.sub(r'\s+', ' ', i.string) + string      #不能用+=,因为存入字符串的顺序要使得新存入的字符串压入最末尾
                    elif isinstance(i, Tag) and i.name == 'sub':
                        string = re.sub(r'\s+', ' ', i.text) + string
                    elif isinstance(i, Tag) and i.name == 'sup':
                        string = re.sub(r'\s+', ' ', i.text) + string
                    elif isinstance(i, Tag) and i.name == 'i':
                        string = re.sub(r'\s+', ' ', i.text) + string
                    elif isinstance(i, Tag) and i.name == 'b':
                        string = re.sub(r'\s+', ' ', i.text) + string
                    else:
                        break
                index1 = string.rfind(' ')
                index2 = string[:string.rfind(' ')].rfind(' ')
                if index1 > index2:
                    wd = string[index2 + 1:index1]
                if re.search(pattern_item, wd):
                    if tag.previous_sibling.string.rfind(' ') > -1:
                        #[{Cupz)4SO4}{Cu(pz)4SO4(H2O)}]. H2O  这种情况
                        if tag.previous_sibling.string[tag.previous_sibling.string.rfind(' ')-1] == '.':
                            continue
                        else:
                            tag.previous_sibling.string.replace_with(tag.previous_sibling.string[0:tag.previous_sibling.string.rfind(' ')] + tag.previous_sibling.string[tag.previous_sibling.string.rfind(' ')+1:])
                    #10.1007/s10847-007-9293-4
                    elif tag.previous_sibling.previous_sibling.string:
                        if tag.previous_sibling.previous_sibling.string.rfind(' ') > -1:
                            tag.previous_sibling.previous_sibling.string.replace_with(tag.previous_sibling.previous_sibling.string[0:tag.previous_sibling.previous_sibling.string.rfind(' ')] + tag.previous_sibling.previous_sibling.string[tag.previous_sibling.previous_sibling.string.rfind(' ') + 1:])

        patt_text = r'\(\S+\)\.'  # .在此种情况下只能是句号不可能是逗号
        excess = [tag for tag in soup.find_all('b', text=lambda text: text is not None and re.search(patt_text, text)) if tag.string and isinstance(tag.next_sibling, NavigableString)]
        for tag in list(excess):
            target_text = ''
            target_text = tag.string[re.search(patt_text, tag.string).span()[0]+1:re.search(patt_text, tag.string).span()[1]-2]
            tag.string.replace_with(tag.text[:re.search(patt_text, tag.string).span()[0]])
            b_node = soup.new_tag('b')
            b_node.string = target_text
            tag.insert_after('). ')
            tag.insert_after(b_node)
            tag.insert_after('(')

        # test = [tag for tag in list(soup.find_all('b', text='3'))]   #text=lambda text: text is not None and 'Etypy' in text
        # txt = ''
        # print(list(test[0].previous_siblings))
        # for tag in test[0].previous_siblings:
        #     txt = tag.string + txt
        # print(txt)
        # exit()

        patt_text_b = r'\s+\((\S+)\)'  # .在此种情况下只能是句号不可能是逗号
        excess_b = [tag for tag in soup.find_all('b', text=lambda text: text is not None and re.search(patt_text_b, text)) if tag.string and isinstance(tag.next_sibling, NavigableString)]
        # print(re.search(patt_text_b, excess_b[0].string))
        # print(re.search(patt_text_b, excess_b[0].string).group(1))
        for tag in list(excess_b):
            string = ''
            target_text = ''
            for i in tag.previous_siblings:
                if isinstance(i, NavigableString):
                    string = re.sub(r'\s+', ' ', i.string) + string  # 不能用+=,因为存入字符串的顺序要使得新存入的字符串压入最末尾
                elif isinstance(i, Tag) and i.name == 'sub':
                    string = re.sub(r'\s+', ' ', i.text) + string
                elif isinstance(i, Tag) and i.name == 'sup':
                    string = re.sub(r'\s+', ' ', i.text) + string
                elif isinstance(i, Tag) and i.name == 'i':
                    string = re.sub(r'\s+', ' ', i.text) + string
                elif isinstance(i, Tag) and i.name == 'b':
                    string = re.sub(r'\s+', ' ', i.text) + string
                elif isinstance(i, Tag) and i.name == 'span' and i['class'][0] == 'c-stack':
                    string = re.sub(r'\s+', ' ', i.text) + string
                else:
                    break
            string = string + tag.string[0:tag.string.find(' ')]
            index1 = string.rfind(' ')
            if index1 > -1:
                wd = string[index1:]
            if re.search(pattern_item, wd):
                target_text = re.search(patt_text_b, tag.string).group(1)
                #re.search() 方法返回的匹配对象（match object）拥有类似span()方法的start()和end()方法来获得分组的索引范围
                # print(re.search(patt_text_b, tag.string).group(1))
                # print(re.search(patt_text_b, tag.string).start(1))
                # print(re.search(patt_text_b, tag.string).end(1))
                # print(tag.string[:re.search(patt_text_b, tag.string).start(1)])
                # print(tag.string[re.search(patt_text_b, tag.string).start(1):re.search(patt_text_b, tag.string).end(1)])

                b_node = soup.new_tag('b')
                b_node.string = tag.string[re.search(patt_text_b, tag.string).start(1):re.search(patt_text_b, tag.string).end(1)]
                b_next_node = soup.new_tag('b')
                b_next_node.string = tag.string[re.search(patt_text_b, tag.string).end(1):]
                tag.string.replace_with(tag.string[:re.search(patt_text_b, tag.string).start(1)])
                tag.insert_after(b_next_node)
                tag.insert_after(b_node)
                # print(tag.string)
                # print(tag.next_sibling)
                # print(tag.next_sibling.next_sibling)

        patt_text_single_b = r'\((\S+)\)'  # .在此种情况下只能是句号不可能是逗号
        excess_single_b = [tag for tag in soup.find_all('b', text=lambda text: text is not None and re.search(patt_text_single_b, text)) if tag.string and tag.next_sibling is None]
        for tag in excess_single_b:
            string = ''
            next_string = ''
            for i in tag.previous_siblings:
                if isinstance(i, NavigableString):
                    string = re.sub(r'\s+', ' ', i.string) + string  # 不能用+=,因为存入字符串的顺序要使得新存入的字符串压入最末尾
                elif isinstance(i, Tag) and i.name == 'sub':
                    string = re.sub(r'\s+', ' ', i.text) + string
                elif isinstance(i, Tag) and i.name == 'sup':
                    string = re.sub(r'\s+', ' ', i.text) + string
                elif isinstance(i, Tag) and i.name == 'i':
                    string = re.sub(r'\s+', ' ', i.text) + string
                elif isinstance(i, Tag) and i.name == 'b':
                    string = re.sub(r'\s+', ' ', i.text) + string
                elif isinstance(i, Tag) and i.name == 'span' and i['class'][0] == 'c-stack':
                    string = re.sub(r'\s+', ' ', i.text) + string
                else:
                    break
            string = string + tag.string[0:tag.string.find(' ')]
            index1 = string.rfind(' ')
            if index1 > -1:
                wd = string[index1:]
            if re.search(pattern_item, wd):
                tag.string.replace_with(tag.string[1:-1])


        patt5 = r'\S+[\)|\]]\s+\('  # r'^[∙·⋅]\s+'      #与下文不太一样，这里直接找的是空格，所以索引应该重新设计    因为已经有加入判断是不是wd，可认为字符串节点也可以使用此规则
        patt5_2version = r'\]\s+\('           #Na2(OAc)2[12-MCMnIII(N)shi-4] (DMF)6   ,10.1007/s10870-020-00843-4
        formula_tags = [tag for tag in list(soup.find_all(text=lambda text: text is not None and re.search(patt5, text))) if tag.string]
        for tag in formula_tags:
            string = ''
            next_string = ''
            for i in tag.previous_siblings:
                if isinstance(i, NavigableString):
                    string = re.sub(r'\s+', ' ', i.string) + string  # 不能用+=,因为存入字符串的顺序要使得新存入的字符串压入最末尾
                elif isinstance(i, Tag) and i.name == 'sub':
                    string = re.sub(r'\s+', ' ', i.text) + string
                elif isinstance(i, Tag) and i.name == 'sup':
                    string = re.sub(r'\s+', ' ', i.text) + string
                elif isinstance(i, Tag) and i.name == 'i':
                    string = re.sub(r'\s+', ' ', i.text) + string
                elif isinstance(i, Tag) and i.name == 'b':
                    string = re.sub(r'\s+', ' ', i.text) + string
                elif isinstance(i, Tag) and i.name == 'span' and i['class'][0] == 'c-stack':
                    string = re.sub(r'\s+', ' ', i.text) + string
                else:
                    break
            string = string + tag.string[0:re.search(patt5, tag.string).start(0)]
            index1 = string.rfind(' ')
            if index1 > -1:
                wd = string[index1:]
            for pre_next in (list(tag.next_siblings)):
                if isinstance(pre_next, NavigableString):
                    next_string = next_string + re.sub(r'\s+[∙·⋅]\s+', '·', re.sub(r'\s+', ' ',pre_next.string))  # 不能用+=,因为存入字符串的顺序要使得线存入的字符串压入最末尾
                elif isinstance(pre_next, Tag) and pre_next.name == 'sub':
                    next_string = next_string + re.sub(r'\s+[∙·⋅]\s+', '·', re.sub(r'\s+', ' ', pre_next.text))
                elif isinstance(pre_next, Tag) and pre_next.name == 'sup':
                    next_string = next_string + re.sub(r'\s+[∙·⋅]\s+', '·', re.sub(r'\s+', ' ', pre_next.text))
                elif isinstance(pre_next, Tag) and pre_next.name == 'i':
                    next_string = next_string + re.sub(r'\s+[∙·⋅]\s+', '·', re.sub(r'\s+', ' ', pre_next.text))
                elif isinstance(pre_next, Tag) and pre_next.name == 'b':
                    next_string = next_string + re.sub(r'\s+[∙·⋅]\s+', '·', re.sub(r'\s+', ' ', pre_next.text))
                elif isinstance(pre_next, Tag) and pre_next.name == 'span' and pre_next['class'][0] == 'c-stack':
                    next_string = next_string + re.sub(r'\s+[∙·⋅]\s+', '·', re.sub(r'\s+', ' ', pre_next.text))
                else:
                    break
            next_string = tag.string[re.search(patt5, tag.string).end(0):] + next_string
            index2 = next_string.find(' ')
            if index2 > -1:
                seq_wd = next_string[0:index2]
            else:
                seq_wd = next_string
            if re.search(pattern_item, seq_wd) and isinstance(tag.next_sibling,NavigableString):   #re.search(pattern_item, wd) and加上此条件约束太大了 但是光用后又比光用前要可靠
                if re.search(patt5_2version, tag.string):
                    tag.string.replace_with(re.sub(patt5_2version, '](', tag.string))
                else:
                    tag.string.replace_with(re.sub(patt5, ')(', tag.string))

        pronoun_tags = [tag for tag in list(soup.find_all('b')) if isinstance(tag.parent, Tag)]
        for tag in pronoun_tags:
            if tag.parent.name == 'sup' or tag.parent.name == 'sub':
                if isinstance(tag.parent.previous_sibling, Tag):
                    if tag.parent.previous_sibling.name == 'b':
                        if tag.parent.previous_sibling.text[-1] != ' ':
                            new_tag = tag.parent
                            tag.parent.previous_sibling.append(new_tag)
                            tag.parent.extract()


        pronoun_tag = [tag for tag in list(soup.find_all('i')) if isinstance(tag.parent, Tag) and tag.parent.previous_sibling]
        for tag in pronoun_tag:
            if tag.parent.name == 'b':
                if isinstance(tag.parent.previous_sibling, Tag):
                    if tag.parent.previous_sibling.name == 'b' and tag.previous_sibling:
                        if tag.parent.previous_sibling.text[-1] != ' ':
                            new_tag = tag          #同名标签的append插入有问题
                            tag.parent.previous_sibling.append(new_tag)
                            if isinstance(tag.parent.next_sibling, Tag):
                                tag.parent.next_sibling.extract()


        dct = {}
        compound_dct = {}
        b_tags = [tag for tag in list(soup.select('.c-article-section__content b'))]    #[tag for tag in list(soup.select('.c-article-section__content b')) if tag.parent.name == 'p']
        b_tags = [tag for tag in b_tags if tag.text != '·']
        #print(len(b_tags))
        #print(len(set(b_tags)))
        for b_tag in b_tags:
            #正常情况，以及表格中p节点的情况  此段代码的功能是取出之前字符串的最后一个单词
            string = ''
            next_string = ''
            wd = ''
            #判别等号后的字符串
            seq_wd = ''
            key = ''
            text = ''
            if b_tag.previous_siblings:
                for pre_str in b_tag.previous_siblings:
                    if isinstance(pre_str, NavigableString):
                        string = re.sub(r'\s+[∙·⋅]\s+', '·',re.sub(r'\s+', ' ', pre_str.string)) + string      #不能用+=,因为存入字符串的顺序要使得新存入的字符串压入最末尾
                    elif isinstance(pre_str, Tag) and pre_str.name == 'sub':
                        string = re.sub(r'\s+[∙·⋅]\s+', '·',re.sub(r'\s+', ' ', pre_str.text)) + string
                    elif isinstance(pre_str, Tag) and pre_str.name == 'sup':
                        string = re.sub(r'\s+[∙·⋅]\s+', '·',re.sub(r'\s+', ' ', pre_str.text)) + string
                    elif isinstance(pre_str, Tag) and pre_str.name == 'i':
                        string = re.sub(r'\s+[∙·⋅]\s+', '·',re.sub(r'\s+', ' ', pre_str.text)) + string
                    elif isinstance(pre_str, Tag) and pre_str.name == 'b':
                        string = re.sub(r'\s+[∙·⋅]\s+', '·',re.sub(r'\s+', ' ', pre_str.text)) + string
                    elif isinstance(pre_str, Tag) and pre_str.name == 'span' and pre_str['class'][0] == 'c-stack':
                        string = re.sub(r'\s+', ' ', pre_str.text) + string
                    else:
                        break
                # print(len(string))
                # print(b_tag.text)
                # print(string)
                if string.find('\\') != -1:
                    print('出现异常字符')
                    print(repr(string[index2+1:index1]))
                index1 = string.rfind(' ')
                index2 = string[:string.rfind(' ')].rfind(' ')
                if index1 > index2:
                    wd = string[index2+1:index1]
                elif index1==index2:
                    pass
                # else:         #-,<b>的情况
                #     wd = string
                #print(repr(wd))
            else:
                # 列表中的黑体
                for parent in b_tag.find_parents():  # table>thead>tr>th table>tbody>tr>td th和td内部可能也有节点
                    if parent.name == 'th':
                        position = list(parent.parent.children).index(parent)
                        for tr in list(parent.parent.next_sibling.children):
                            string = tr.contents[position].get_text()  # td节点
                            # 与下文的单词定位不同，下文的单词与强调文本的单词连接一起
                            index = string.rfind(' ')
                            if index > -1:
                                wd = string[index:]
                            else:
                                wd = string
                    # elif parent.name == 'td':    #认为是少数现象，不管了
            if b_tag.next_siblings:
                if b_tag.next_sibling and b_tag.next_sibling.string:
                    if b_tag.next_sibling.string[0]=='′':
                        continue
                for pre_next in (list(b_tag.next_siblings)):
                    if isinstance(pre_next, NavigableString):
                        next_string = next_string + re.sub(r'\s+[∙·⋅]\s+', '·',re.sub(r'\s+', ' ', pre_next.string))      #不能用+=,因为存入字符串的顺序要使得线存入的字符串压入最末尾
                    elif isinstance(pre_next, Tag) and pre_next.name == 'sub':
                        next_string = next_string + re.sub(r'\s+[∙·⋅]\s+', '·',re.sub(r'\s+', ' ', pre_next.text))
                    elif isinstance(pre_next, Tag) and pre_next.name == 'sup':
                        next_string = next_string + re.sub(r'\s+[∙·⋅]\s+', '·',re.sub(r'\s+', ' ', pre_next.text))
                    elif isinstance(pre_next, Tag) and pre_next.name == 'i':
                        next_string = next_string + re.sub(r'\s+[∙·⋅]\s+', '·',re.sub(r'\s+', ' ', pre_next.text))
                    elif isinstance(pre_next, Tag) and pre_next.name == 'b':
                        next_string = next_string + re.sub(r'\s+[∙·⋅]\s+', '·',re.sub(r'\s+', ' ', pre_next.text))
                    elif isinstance(pre_next, Tag) and pre_next.name == 'span' and pre_next['class'][0] == 'c-stack':
                        next_string = next_string + re.sub(r'\s+', ' ', pre_next.text)
                    else:
                        break
                if -1<next_string.find(' = ')<2 :
                    index1 = next_string.find(' ')
                    index2 = next_string.find('=')
                    index3 = next_string[index1+1:].find(' ')+index1+1
                    index4 = next_string[index3+1:].find(' ')+index3+1
                    #print(index1, index2, index3, index4)
                    # print(next_string[index3])
                    if index2 == index1+1 and index4 > index3:
                        # print(b_tag.text)
                        # print(next_string)
                        # print('<<<<>>>>>')
                        seq_wd = next_string[index3 + 1:index4]
                        if re.search(pattern_item, wd):
                            pass
                        elif re.search(pattern_item,seq_wd):
                            wd = seq_wd
                            if wd[-1] == '.'or wd[-1] == ',':
                                wd = wd[:len(wd) - 1]
                            if wd.find('. ') > -1:
                                wd = wd[:wd.find('. ') - 1]
                            if wd[0] == '(' and wd[-1] == ')':
                                wd = wd[1:len(wd)-1]
                else:
                    if next_string.find(' ') == 0:
                        seq_wd = next_string[1:next_string[1:].find(' ')+1]
                        if re.search(pattern_item, wd):
                            pass
                        elif re.search(pattern_item,seq_wd):
                            wd = seq_wd
                            if wd[-1] == '.'or wd[-1] == ',':
                                wd = wd[:len(wd) - 1]
                            if wd.find('. ') > -1:
                                wd = wd[:wd.find('. ') - 1]
                            if wd[0] == '(' and wd[-1] == ')':
                                wd = wd[1:len(wd)-1]
                    elif next_string.find(' ') == 1:
                        seq_wd = next_string[2:next_string[2:].find(' ') + 2]
                        if re.search(pattern_item, wd):
                            pass
                        elif re.search(pattern_item, seq_wd):
                            wd = seq_wd
                            if wd[-1] == '.' or wd[-1] == ',':
                                wd = wd[:len(wd) - 1]
                            if wd.find('. ') > -1:
                                wd = wd[:wd.find('. ') - 1]
                            if wd[0] == '(' and wd[-1] == ')':
                                wd = wd[1:len(wd)-1]
                # print(next_string)
                # print(b_tag.text)
                # print(seq_wd)
                # print(wd)

            #创建以及更新,字典的更新以及文本冗余的指代词的删除,同时进行
            if (re.search(pattern_item,wd) or (re.search(pattern_metal,wd) and len(re.findall(pattern_1, wd))>0)) and ' ' not in b_tag.text and '·' not in b_tag.text and '⋅' not in b_tag.text and ']' not in b_tag.text and '[' not in b_tag.text and ')' not in b_tag.text and '(' not in b_tag.text:
                # print(b_tag.text)
                # print(wd)
                # print(string)
                # print(next_string)
                # print(b_tag.parent.text)
                # print(b_tag.parent.prettify())

                # if re.search(patt_compounds,wd) and re.search(pattern_metal,wd) is None:
                #     b_tag.extract()
                #     continue

                #10.1134/S0036023619090195   ((Ph4SbOC(O)C6H4(OH-3)
                if wd.count('(') != wd.count(')'):
                    wd1 = wd
                    wd = wd.strip(')').strip('(')
                    if wd.count('(') == wd.count(')') + 1:
                        wd = wd +')'
                    elif wd.count('(') + 1 == wd.count(')'):
                        wd = '(' + wd
                    if wd.count('(') != wd.count(')'):
                        wd = wd1
                if wd[-1] == ';'  or wd[-1] == ':' or wd[-1] == '.' or wd[-1] == ',' :
                    wd = wd[:len(wd) - 1]
                if wd.find(':')>-1:
                    wd = wd[wd.find(':')+1:]
                if wd.find('—')>-1 or (wd.count('[') != wd.count (']')) or (wd.count('{') != wd.count ('}')) or (wd.count('(') != wd.count (')')):   #中文版的长破折号
                    continue
                if b_tag.text in dct :
                    if len(wd)>=len(dct[b_tag.text]):    #and b_tag.text.find('.')!=-1
                        if wd == next_string[1:next_string[1:].find(' ')+1]:
                            continue
                        dct[b_tag.text] = wd
                        #print('true')
                        b_tag.extract()
                    # elif len(wd) == len(dct[b_tag.text]):
                    #     b_tag.extract()
                    else:
                        pass
                else:
                    # print(b_tag.text)
                    # print(b_tag.next_sibling)
                    #print(wd)
                    #10.1134/S0022476621010133,
                    if b_tag.text and (b_tag.text[-1] == ')' or b_tag.text[0] == '(') or b_tag.text.find('−')>-1:
                        continue
                    dct[b_tag.text] = wd
                    b_tag.extract()                  #之后剩余即是无化学式前文的b标签节点
            if re.search(patt_compounds,wd):
                # print(b_tag.text)
                # print(wd)
                key = b_tag.text
                text = wd
                if wd.find('—')>-1:
                    continue
                if wd[-1] == ';' or wd[-1] == ':' or wd[-1] == '.' or wd[-1] == ',':
                    wd = wd[:len(wd) - 1]
                if wd.find(':')>-1:
                    wd = wd[wd.find(':')+1:]
                if key in compound_dct:
                    if wd in compound_dct[key]:
                        pass
                    else:
                        compound_dct[key].append(text)
                else:
                    if not key or key.find(' ')>-1 or (text.count(')') != text.count ('(')) or (text.count('{') != text.count ('}')) or (text.count('[') != text.count (']')):
                        continue
                    compound_dct[key] = [text]
        #print(len(dct))
        print(dct)
        #print(list(dct.keys()))

        # 若是字典中出现两个相同的值，保留后一个键值对
        keys, values = list(dct.keys()), list(dct.values())
        repeat_values = []
        for value in values:
            if values.count(value) > 1 and value not in repeat_values:
                repeat_values.append(value)
        for v in repeat_values:
            key = keys[values.index(v)]
            del dct[key]


        # t1 = soup.find_all('b',text ='1')
        # print(len(t1))
        # for b_tag in t1:
        #     string = ''
        #     if b_tag.previous_siblings:
        #         print('>>>>>>><<<<<<<')
        #         for pre_str in b_tag.previous_siblings:
        #             if isinstance(pre_str, NavigableString):      #<font _mstmutation="1">解析后被判断为字符串格式
        #                 string = pre_str.string + string  # 不能用+=,因为存入字符串的顺序要使得线存入的字符串压入最末尾
        #                 print(pre_str.string)
        #                 print(1)
        #             elif isinstance(pre_str, Tag) and pre_str.name == 'sub':
        #                 string = pre_str.text + string
        #                 print(pre_str.text)
        #                 print(2)
        #             elif isinstance(pre_str, Tag) and pre_str.name == 'sup':
        #                 string = pre_str.text + string
        #                 print(pre_str.text)
        #                 print(3)
        #             else:
        #                 break
        #         print(string)
        #         print(string)

        for key in list(dct.keys()):
            pattern = r'\s+{}$'.format(key)
            tags = [tag for tag in list(soup.find_all('b',text = lambda text: text is not None and re.match(pattern,text))) if tag.string and tag.previous_sibling]
            for tag in tags:
                if isinstance(tag.previous_sibling,NavigableString):
                    tag.previous_sibling.string.replace_with(tag.previous_sibling.string + ' ')
                    tag.string.replace_with(key)
                elif isinstance(tag.previous_sibling,Tag):
                    tag.insert_before(' ')
                    tag.string.replace_with(key)

        # for key in list(dct.keys()):
        #     target_text = '('+key+')'
        #     excess = soup.find_all('b',text = lambda text: text is not None and target_text in text)
        #     print(len(excess))
        #     for tag in list(excess):
        #         string = tag.string
        #         new_string = string.replace(target_text, "")
        #         tag.string.replace_with(new_string)

        brackets2 = [f"({x}" for x in list(dct.keys())]
        brackets1 = [f"{x})" for x in list(dct.keys())]
        #print(adds)
        #print(len(dashs))
        #处理括号，应该在，-符号之前，因为这些符号在括号内部
        b_strong_tags = [tag for tag in list(soup.find_all('b') + soup.find_all('strong')) if tag.parent.name == 'p']
        for tag in b_strong_tags:
            for brac in brackets1:
                if tag.text.endswith(brac) and tag.string:
                    tag.insert_after(')')
                    tag.string.replace_with(tag.string[:len(tag.string)-1])

        b_strong_tags = [tag for tag in list(soup.find_all('b') + soup.find_all('strong')) if tag.parent.name == 'p']
        for tag in b_strong_tags:
            for brac in brackets2:
                if tag.text.find(brac) == 0 and tag.string:
                    tag.insert_before('(')
                    tag.string.replace_with(tag.string[1:])

        b_strong_tags = [tag for tag in list(soup.find_all('b') + soup.find_all('strong')) if tag.parent.name == 'p']
        combinations = [f"{x}, {y}" for x in list(dct.keys()) for y in list(dct.keys()) if x != y]
        dashs = [f"{x}-{y}" for x in list(dct.keys()) for y in list(dct.keys()) if x != y]
        adds = [f"{x}," for x in list(dct.keys())] + [f"{x}." for x in list(dct.keys())]
        for tag in b_strong_tags:
            for opt in combinations:
                str_copy = tag.text
                if tag.text.find(opt)>-1 and tag.string and len(tag.text)>=len(opt):                                    #tag.string而不是tag.text是为了使b节点内只有一个子节点
                    if tag.text.find(opt) == 0:
                        tag.string.replace_with(str_copy[:str_copy.find(', ')])
                        b_node = soup.new_tag('b')
                        b_node.string = opt[opt.find(', ')+2:]
                        tag.insert_after(b_node)
                        tag.insert_after(', ')
                    else:
                        tag.string.replace_with(str_copy[:str_copy.find(opt)])
                        b_node1 = soup.new_tag('b')
                        b_node1.string = opt[:opt.find(',')]
                        b_node2 = soup.new_tag('b')
                        b_node2.string = opt[opt.find(' '):]
                        tag.insert_after(str_copy[str_copy.find(opt)+len(opt):])
                        tag.insert_after(b_node2)
                        tag.insert_after(', ')
                        tag.insert_after(b_node1)
                    break
            for connect in dashs:
                str_copy = tag.text
                if tag.text == connect and tag.string:
                    tag.string.replace_with(str_copy[:str_copy.find('-')])
                    b_node = soup.new_tag('b')
                    b_node.string = connect[connect.find('-')+1:]
                    tag.insert_after(b_node)
                    tag.insert_after('-')
                    # print(tag.string)
                    # print(tag.next_sibling.string)
                    # print(tag.next_sibling.next_sibling.string)
                    break
            for add in adds:
                str_copy = tag.text
                if tag.text.find(add) == 0 and tag.string:
                    if str_copy.find(',')>-1:
                        tag.string.replace_with(str_copy[:str_copy.find(',')])
                        tag.insert_after(str_copy[str_copy.find(','):])
                    elif str_copy.find('.')>-1:
                        tag.string.replace_with(str_copy[:str_copy.find('.')])
                        tag.insert_after(str_copy[str_copy.find('.'):])


        # 将各处包含-转为，
        for key in list(dct.keys()):
            b_strong_tags = soup.find_all('b', string=key) + soup.find_all('strong', string=key)
            b_strong_tags = [tag for tag in b_strong_tags if tag.parent.name == 'p']
            # print(len(b_strong_tags))
            for b_strong in b_strong_tags:
                if isinstance(b_strong.next_sibling, NavigableString):
                    if b_strong.next_sibling.string == '–' or b_strong.next_sibling.string == '-':
                        b_strong.next_sibling.extract()
                        if isinstance(b_strong.next_sibling, Tag) and b_strong.next_sibling.name == 'b' and b_strong.next_sibling.text in list(dct.keys()):
                            if b_strong.text.isdigit() and b_strong.next_sibling.text.isdigit():
                                for dig in reversed(range(int(b_strong.text) + 1, int(b_strong.next_sibling.text))):
                                    b_strong.insert_after(', ')
                                    new_b_tag = soup.new_tag('b')  # 创建新的<b>标签节点
                                    new_b_tag.string = str(dig)  # 设置<b>标签节点的文本内容
                                    b_strong.insert_after(new_b_tag)
                                b_strong.insert_after(', ')
                            elif list(dct.keys()).index(b_strong.text)>-1 and list(dct.keys()).index(b_strong.next_sibling.text)>-1:
                                for i in range(list(dct.keys()).index(b_strong.text) + 1,list(dct.keys()).index(b_strong.next_sibling.text)):
                                    b_strong.insert_after(', ')
                                    new_b_tag = soup.new_tag('b')  # 创建新的<b>标签节点
                                    new_b_tag.string = str(dct[list(dct.keys())[i]])  # 设置<b>标签节点的文本内容
                                    b_strong.insert_after(new_b_tag)
                                b_strong.insert_after(', ')
                        elif isinstance(b_strong.next_sibling, Tag) and b_strong.next_sibling.name == 'strong':
                            if b_strong.text.isdigit() and b_strong.next_sibling.text.isdigit():
                                for dig in reversed(range(int(b_strong.text) + 1, int(b_strong.next_sibling.text))):
                                    b_strong.insert_after(', ')
                                    new_b_tag = soup.new_tag('b')  # 创建新的<b>标签节点
                                    new_b_tag.string = str(dig)  # 设置<b>标签节点的文本内容
                                    b_strong.insert_after(new_b_tag)
                                b_strong.insert_after(', ')
                            elif list(dct.keys()).index(b_strong.text)>-1 and list(dct.keys()).index(b_strong.next_sibling.text)>-1:
                                for i in range(list(dct.keys()).index(b_strong.text)+1,list(dct.keys()).index(b_strong.next_sibling.text)):
                                    b_strong.insert_after(', ')
                                    new_b_tag = soup.new_tag('b')  # 创建新的<b>标签节点
                                    new_b_tag.string = str(dct[list(dct.keys())[i]])  # 设置<b>标签节点的文本内容
                                    b_strong.insert_after(new_b_tag)
                                b_strong.insert_after(', ')

        #将各处的指示代词替换为原形
        for key in list(dct.keys()):
            # b_strong_tags = soup.find_all('b',text= key) + soup.find_all('strong',text= key)
            b_strong_tags = [tag for tag in soup.find_all('b') + soup.find_all('strong') if tag.text == key]
            b_tags = [tag for tag in b_strong_tags if tag.parent.name == 'p']
            for i in range(len(b_tags)):
                # 不好观察具体怎么替换的
                # string_node = soup.new_string(dct[key])
                # b_tags[i].replace_with(string_node)
                string = ''
                wd = ''
                for pre in b_tags[i].previous_siblings:
                    if isinstance(pre, NavigableString):
                        string = re.sub(r'\s+', ' ', pre.string) + string  # 不能用+=,因为存入字符串的顺序要使得新存入的字符串压入最末尾
                    elif isinstance(pre, Tag) and pre.name == 'sub':
                        string = re.sub(r'\s+', ' ', pre.text) + string
                    elif isinstance(pre, Tag) and pre.name == 'sup':
                        string = re.sub(r'\s+', ' ', pre.text) + string
                    elif isinstance(pre, Tag) and pre.name == 'i':
                        string = re.sub(r'\s+', ' ', pre.text) + string
                    elif isinstance(pre, Tag) and pre.name == 'b':
                        string = re.sub(r'\s+', ' ', pre.text) + string
                    elif isinstance(pre, Tag) and pre.name == 'span' and pre['class'][0] == 'c-stack':
                        string = re.sub(r'\s+', ' ', pre.text) + string
                    else:
                        break
                index1 = string.rfind(' ')
                index2 = string[:string.rfind(' ')].rfind(' ')
                if index1 > index2:
                    wd = string[index2 + 1:index1]
                elif index1 == index2:
                    pass
                if wd:
                    if wd[-1] == ',':
                        wd = wd[:len(wd) - 1]
                if wd != dct[key]:
                    if b_tags[i].string is None:
                        new_b_tag = soup.new_tag('b')
                        new_b_tag.string = str(dct[key])
                        b_tags[i].insert_after(new_b_tag)
                        b_tags[i].extract()
                    else:
                        b_tags[i].string.replace_with(dct[key])
                else:
                    b_tags[i].extract()
                    if isinstance(b_tags[i].previous_sibling, NavigableString):
                        if b_tags[i].previous_sibling.string == ', ':
                            b_tags[i].previous_sibling.extract()

        #化合物 + 等号，配体
        compounud_tags = [tag for tag in soup.find_all(text=lambda text: text is not None and re.search(patt_equ, text)) if tag.parent.name == 'p']
        for tag in compounud_tags:
            text=''
            pre_string = tag.string
            for pre_str in tag.previous_siblings:
                if isinstance(pre_str, NavigableString):
                    if pre_str.string.find(']') > -1:
                        pre_string = re.sub(r'\s+', ' ', pre_str.string) + pre_string
                        break
                    pre_string = re.sub(r'\s+[∙·⋅]\s+', '·',re.sub(r'\s+', ' ', pre_str.string)) + pre_string  # 不能用+=,因为存入字符串的顺序要使得新存入的字符串压入最末尾
                elif isinstance(pre_str, Tag) and pre_str.name == 'sub' :
                    if pre_str.text.find(']') > -1:
                        pre_string = re.sub(r'\s+', ' ', pre_str.text) + pre_string
                        break
                    pre_string = re.sub(r'\s+[∙·⋅]\s+', '·', re.sub(r'\s+', ' ', pre_str.text)) + pre_string
                elif isinstance(pre_str, Tag) and pre_str.name == 'sup':
                    if pre_str.text.find(']') > -1:
                        pre_string = re.sub(r'\s+', ' ', pre_str.text) + pre_string
                        break
                    pre_string = re.sub(r'\s+[∙·⋅]\s+', '·', re.sub(r'\s+', ' ', pre_str.text)) + pre_string
                elif isinstance(pre_str, Tag) and pre_str.name == 'i':
                    if pre_str.text.find(']') > -1:
                        pre_string = re.sub(r'\s+', ' ', pre_str.text) + pre_string
                        break
                    pre_string = re.sub(r'\s+[∙·⋅]\s+', '·', re.sub(r'\s+', ' ', pre_str.text)) + pre_string
                elif isinstance(pre_str, Tag) and pre_str.name == 'b':
                    if pre_str.text.find(']') > -1:
                        pre_string = re.sub(r'\s+', ' ', pre_str.text) + pre_string
                        break
                    pre_string = re.sub(r'\s+[∙·⋅]\s+', '·', re.sub(r'\s+', ' ', pre_str.text)) + pre_string
                elif isinstance(pre_str, Tag) and pre_str.name == 'span' and pre_str['class'][0] == 'c-stack':
                    if pre_str.text.find(']') > -1:
                        pre_string = re.sub(r'\s+', ' ', pre_str.text) + pre_string
                        break
                    pre_string = re.sub(r'\s+', ' ', pre_str.text) + pre_string
                else:
                    break
            for pre_str in tag.next_siblings:
                if isinstance(pre_str, NavigableString):
                    if pre_str.string.find(' ') > -1:
                        pre_string = pre_string + re.sub(r'\s+', ' ', pre_str.string)
                        break
                    pre_string = pre_string + re.sub(r'\s+[∙·⋅]\s+', '·', re.sub(r'\s+', ' ',
                                                                                 pre_str.string))  # 不能用+=,因为存入字符串的顺序要使得新存入的字符串压入最末尾
                elif isinstance(pre_str, Tag) and pre_str.name == 'sub':
                    if pre_str.text.find(' ') > -1:
                        pre_string = pre_string + re.sub(r'\s+', ' ', pre_str.text)
                        break
                    pre_string = pre_string + re.sub(r'\s+[∙·⋅]\s+', '·', re.sub(r'\s+', ' ', pre_str.text))
                elif isinstance(pre_str, Tag) and pre_str.name == 'sup':
                    if pre_str.text.find(' ') > -1:
                        pre_string = pre_string + re.sub(r'\s+', ' ', pre_str.text) + pre_string
                        break
                    pre_string = pre_string + re.sub(r'\s+[∙·⋅]\s+', '·', re.sub(r'\s+', ' ', pre_str.text))
                elif isinstance(pre_str, Tag) and pre_str.name == 'i':
                    if pre_str.text.find(' ') > -1:
                        pre_string = pre_string + re.sub(r'\s+', ' ', pre_str.text)
                        break
                    pre_string = pre_string + re.sub(r'\s+[∙·⋅]\s+', '·', re.sub(r'\s+', ' ', pre_str.text))
                elif isinstance(pre_str, Tag) and pre_str.name == 'strong':
                    if pre_str.text.find(' ') > -1:
                        pre_string = pre_string + re.sub(r'\s+', ' ', pre_str.text)
                        break
                    pre_string = pre_string + re.sub(r'\s+[∙·⋅]\s+', '·', re.sub(r'\s+', ' ', pre_str.text))
                elif isinstance(pre_str, Tag) and pre_str.name == 'span' and ('class' in pre_str.attrs):
                    if pre_str['class'][0] == 'c-stack' and pre_str.text.find(' ') > -1:
                        pre_string = pre_string + re.sub(r'\s+', ' ', pre_str.text) + pre_string
                        break
                    pre_string = pre_string + re.sub(r'\s+', ' ', pre_str.text)
                else:
                    break
            # print(pre_string)
            # print(re.findall(patt_equ_split, pre_string))
            for i in range(len(re.findall(patt_equ_split, pre_string))):
                string = re.findall(patt_equ_split, pre_string)[i]
                # re.search(patt_equ, string).group(1) = string[0]
                # re.search(patt_equ, string).group(2) = string[1]
                if re.search(patt_compounds, string[1]):
                    # print(re.search(patt_compounds, string[1]))
                    # print(string[0].split('(')[-1].split('[')[-1] and string[0].split('(')[-1].split('[')[-1].find('http') == -1 and string[1].find('/') == -1)
                    if string[0].split('(')[-1].split('[')[-1] and string[0].split('(')[-1].split('[')[-1].find(
                            'http') == -1 and string[1].find('/') == -1:
                        text = string[1]
                        key = string[0].split('(')[-1].split('[')[-1]
                        if key.rfind('{') > -1:
                            key = key[key.rfind('{') + 1:]
                        if string[0].split('(')[-1].split('[')[-1].rfind('(') > -1:
                            key = key[key.rfind('(') + 1:]
                        if text.count('[') < text.count(']'):
                            text = text[:text.rfind(']')]
                        if text.count('{') < text.count('}'):
                            text = text[:text.rfind('}')]
                        if text.count('(') < text.count(')'):
                            text = text[:text.rfind(')')]
                        if text.count('[') > text.count(']'):
                            text = text[text.find('[') + 1:]
                        if text.count('{') > text.count('}'):
                            text = text[text.find('{') + 1:]
                        if text.count('(') > text.count(')'):
                            text = text[text.find('(') + 1:]
                        if text:
                            if text[-1] == ';':
                                text = text[:len(text) - 1]
                            if text[-1] == ',':
                                text = text[:len(text) - 1]
                            if text[-1] == '.':
                                text = text[:len(text) - 1]
                        if key in compound_dct:
                            if text in compound_dct[key]:
                                pass
                            else:
                                compound_dct[key].append(text)
                        else:
                            compound_dct[key] = [text]
        print(compound_dct)


        #单一的查找
        # if re.search(patt_compounds, re.search(patt_equ, string).group(2)):
        #     if re.search(patt_equ, string).group(1).split('(')[-1].split('[')[-1] and \
        #             re.search(patt_equ, string).group(1).split('(')[-1].split('[')[-1].find('http') == -1:
        #         text = re.search(patt_equ, string).group(2)
        #         print(text)
        #         key = re.search(patt_equ, string).group(1).split('(')[-1].split('[')[-1]
        #         if key.rfind('{') > -1:
        #             key = key[key.rfind('{') + 1:]
        #         if re.search(patt_equ, string).group(1).split('(')[-1].split('[')[-1].rfind('(') > -1:
        #             key = key[key.rfind('(') + 1:]
        #         if text.count('[') < text.count(']'):
        #             text = text[:text.rfind(']')]
        #         if text.count('{') < text.count('}'):
        #             text = text[:text.rfind('}')]
        #         if text.count('(') < text.count(')'):
        #             text = text[:text.rfind(')')]
        #         if text.count('[') > text.count(']'):
        #             text = text[:text.rfind('[')]
        #         if text.count('{') > text.count('}'):
        #             text = text[:text.rfind('{')]
        #         if text.count('(') > text.count(')'):
        #             text = text[:text.rfind('(')]
        #         if text[-1] == ';':
        #             text = text[:len(text) - 1]
        #         if text[-1] == ',':
        #             text = text[:len(text) - 1]
        #         if text[-1] == '.':
        #             text = text[:len(text) - 1]
        #         if key in compound_dct:
        #             compound_dct[key].append(text)
        #         else:
        #             compound_dct[key] = [text]

        # with open('test.html', 'wb') as f:
        #     f.write(str(soup.prettify()).encode())             #f.write(str(soup.prettify()).encode()),文件会出现多余的缩进符变成空格
        # exit()

        #10.1134/S1066362221040056  append和insert_after的差异      合并段落，部分段落以，结尾
        for l in range(len(main_text)):
            for content in [p_tag for p_tag in main_text[l].contents if p_tag.name=='p']:
                #print(content.text)
                if content.next_sibling:
                    if content.next_sibling.name == 'p' and content.text[-1]==',':
                        children = content.next_sibling.contents
                        print('>>>>>>>>processing<<<<<<<<<')
                        #用for child in children：只能在字符串节点中循环？？？
                        for i in range(len(children)):           #直接使用content.append(content.next_sibling)的效果差
                            # print(type(children[i]))
                            # print(children)
                            child = copy.copy(children[i])                   #必须要copy，哪怕是赋值给新变量，原始存储地址的值仍会随着insert变化
                            content.contents[-1].insert_after(child)         #content.append(child)
                        content.next_sibling.extract()

        #exit()
        df.at[index, 'name_dicts'] = dct
        df.at[index, 'compound_dicts'] = compound_dct

        #清空在以追加模式存入，无法以追加模式覆盖
        # with open(list_html[j], 'w') as f:
        #     pass
        # for l in range(len(main_text)):
        #     new_tag = ptag_merge_h3tag(main_text[l])
        #     main_text[l].replace_with(new_tag)  # 如何返回一个bs4.element.Tag类型       其实也可以不用再将修改后main_text[i]内容置入main_text[i],直接分部存入文档就行   继续打印main_text[i],其实其值是并未改变的，改变的是Beautifuisoup对象，oldtag会从Beautifulsoup对象中删除，newtag会被添加到oldtag位置上。
        #     #print('<<<<<<<<>>>>>>>>>')
        #     with open(list_html[j], 'ab') as f:
        #         f.write(str(ptag_merge_h3tag(main_text[l])).encode())

    if 'flags' in list(df.columns):
        df = df.drop(df[df['flags'] == 2].index, axis=0)
    df.to_csv('count_year_url_publiser_dict1134.csv', index=False)

        # except Exception as e:
        #     print(str(e))
        #     print('Data preprocess error')

def is_english_word(sentence,index = 0):
    tokens = nltk.word_tokenize(sentence)
    # 将字符串转换为小写字母，以确保与WordNet中的词形匹配
    word = tokens[index]
    word = word.lower()

    # 使用NLTK的词形归并器将单词还原为基本形式
    lemmatizer = nltk.stem.WordNetLemmatizer()
    lemma = lemmatizer.lemmatize(word)

    # 判断还原后的单词是否在WordNet中存在
    if len(wordnet.synsets(lemma))>0:
        return True
    else:
        return False


def para_clean(paragraph):
    pattern = r'\b(and|or)\s+(\w+-\w+)'
    pattern4 = r','
    str = re.findall(pattern, paragraph)  # 最好不能重复
    #print(str)
    if re.findall(pattern, paragraph):
        para = copy.copy(paragraph)
        para= re.sub(pattern4, '', para)
        head = 0
        text = ''
        for words in re.finditer(pattern, paragraph):        #注意para和paragraph的区别
            word = words.group()
            print(word)
            tail = words.end()
            tag_words = words.group(2).split('-')
            pattern3 = rf'((?:\b\w+-[\s]*){{0,5}})\b{re.escape(word)}\b'
            if not re.findall(pattern3, para):
                continue
            if not re.findall(pattern3, para)[0]:           #是一个包含空字符串的列表而不是一个空列表，匹配式中使用了零宽度匹配，例如*
                txt = paragraph[head:tail]
                print(txt)
            string = re.findall(pattern3, para)[0]
            print(re.findall(pattern3, para))
            for i in range(len(string.split())):
                if i < 1:
                    txt = paragraph[head:tail].replace(string.split()[i], string.split()[i] + tag_words[1])
                else:
                    txt = txt.replace(string.split()[i], string.split()[i] + tag_words[1], 1)
                print(txt)
            text += txt
            print('>>>>>>>>><<<<<<<<<')
            head = tail

        text += paragraph[tail:]
        # print(text)
        # print(paragraph)
        return text
    else:
        return paragraph

if __name__ == '__main__':
    # url = 'https://link.springer.com/article/10.1023/A:1008118524148'
    #url = 'https://link.springer.com/article/10.1007/s10876-020-01817-4'
    url = 'https://link.springer.com/article/10.1134/S002247662012015X'
    # doi_1 = '10.1134/S1070363221020183'
    # url = 'http://api.springernature.com/metadata/json?q=doi:{doi}&api_key={apikey}'.format(doi=doi_1,apikey='fff1a02034ab463e11fa60f5fe9718d1')
    # url = 'http://api.springernature.com/metadata/pam/doi/{doi}?api_key={apikey}'.format(doi=doi_1,apikey='fff1a02034ab463e11fa60f5fe9718d1')
    # url = 'http://api.springernature.com/meta/v2/jats?q=doi:{doi}&api_key={apikey}'.format(doi=doi_1,apikey='fff1a02034ab463e11fa60f5fe9718d1')
    # url = 'http://api.springernature.com/metadata/pam?q=doi:{doi}&api_key={apikey}'.format(doi=doi_1,apikey='fff1a02034ab463e11fa60f5fe9718d1')
    # url = 'https://api.springernature.com/openaccess/jats/doi/{doi}'.format(doi=doi_1)
    # url = 'http://api.springernature.com/openaccess/jats?s=1&p=1&q=doi：{doi}&api_key={apikey}'.format(doi=doi_1,apikey='fff1a02034ab463e11fa60f5fe9718d1')
    # #url = 'http://api.springernature.com/meta/v2/json?q=doi:{doi}&api_key={apikey}'.format(doi=doi_1,apikey='fff1a02034ab463e11fa60f5fe9718d1')
    # print(url)
    #test_download(url)
    # exit()

    # df = pd.read_csv('count_year_publiser1134.csv', header=0)
    # get_url(df)
    # exit()

    # df = pd.read_csv('count_year_url_publiser1007.csv', header=0)
    # list_flags = download_html(df)
    # print(list_flags)

    #preprocess()

    # df = pd.read_csv('count_year_url_publiser1007.csv', header=0)
    # list_flags = download_xml(df)
    #df.insert(5, 'flags', list_flags)
    #df.to_csv('count_year_url_publiser1134.csv', index=False)
    #'http://api.springernature.com/meta/v2/pam?q=doi:10.1007/s11276-008-0131-4&api_key=yourKeyHere'          #https://dev.springernature.com/表述的网页格式
    #'http://api.springernature.com/meta/v2/json?q=doi:10.1007/BF00627098&api_key=yourKeyHere'
    # list_flags = download_xml(df)
    # df.insert(6, 'flags', list_flags)
    # df.to_csv('count_year_url_publiser1007.csv', index=False)
    orignaltext_batch_process()
    #test('DOI_10.1134_S002247662008017X_2020.html')
    #test('DOI_10.1134_S1070363221020183_2021.html')







#与test函数中处理顺序不同
# if find_count(str(child.previous_sibling.string), '(') > find_count(str(child.previous_sibling.string),')') and find_count(str(child.next_sibling.string),'(') < find_count(str(child.next_sibling.string), ')'):
#     child.previous_sibling.replace_with(str(child.previous_sibling.string)[:str(child.previous_sibling.string).rfind('(')])  # 本来想用节点替换的方式，结果发现tag中包含的字符串（即Navigablestring对象）不能编辑,但是可以被替换成其它的字符串
#     # print(str(child.next_sibling.string)[str(child.next_sibling.string).find(')')+1:])
#     child.next_sibling.replace_with(str(child.next_sibling.string)[str(child.next_sibling.string).find(')') + 1:])
#     child.extract()
#     continue
#
# # 处理圆括号内含多个链接结点的情况
# # 换个思路，可能某一个方向能够欺骗代码的逻辑，那就加一层从两个方向来进行检查。对这种多个链接节点和混杂在一起的字符串节点的括号内，需要删除所有的字符串节点，并替换括号。链接节点是必定功能删除的; 最后会剩下一个（链接节点）的形式，因此不用删除括号
# # 主要目的是清楚夹杂在链接节点中间的文本节点
# if find_count(str(child.previous_sibling.string), '(') > find_count(str(child.previous_sibling.string), ')'):
#     '''如果有多个节点，则第一个节点的下一个兄弟节点绝不会包括括号'''
#     if str(child.next_sibling).find(')') >= 0:  # find返回的是列表索引位置
#         child.next_sibling.replace_with(str(child.next_sibling.string)[str(child.next_sibling.string).find(')') + 1:])
#         child.previous_sibling.replace_with(str(child.previous_sibling.string)[:str(child.previous_sibling.string).rfind('(')])
#         child.extract()
#         continue
#
#     for target in list(child.next_siblings):
#         print(str(target).replace("\n", "").replace("\t", ""))
#         '''print(target.find(')'))与print(target.find(')')>=0)的区别，一个是bs4节点的查找函数一个是字符串的查找函数'''
#         if target.name == 'a' or str(target).find(')') >= 0:
#             break
#         target.extract()
#     child.extract()
#     continue
# # if find_count(str(child.previous_sibling.string), '(')>find_count(str(child.previous_sibling.string), ')'):
# #     for target in list(child.next_siblings):
# #         if target.name != 'a' and target.find(')'):
# #             break
# #         target.extract()
# if find_count(str(child.next_sibling.string), '(') < find_count(str(child.next_sibling.string), ')'):
#     if str(child.previous_sibling).find('(') >= 0:  # find返回的是列表索引位置
#         child.next_sibling.replace_with(str(child.next_sibling.string)[str(child.next_sibling.string).find(')') + 1:])
#         child.previous_sibling.replace_with(str(child.previous_sibling.string)[:str(child.previous_sibling.string).rfind('(')])
#         child.extract()
#         continue
#     for target in list(child.previous_siblings):
#         if target.name == 'a' or str(target).rfind('(') >= 0:
#             break
#         target.extract()
# if find_count(str(child.previous_sibling.string), '(') == find_count(str(child.previous_sibling.string),')') or find_count(str(child.next_sibling.string),'(') == find_count(str(child.next_sibling.string), ')'):  # 判别条件方宽松一些
#     print(2)
#     if re.match('[fF]ig', child.get_text()):
#         if isinstance(child.next_sibling, NavigableString):
#             child.next_sibling.replace_with('Figure ' + str(child.next_sibling.string))
#             child.extract()
#             continue
#         elif isinstance(child.previous_sibling, NavigableString):
#             child.previous_sibling.replace_with(str(child.previous_sibling.string) + ' Fig')
#             child.extract()
#             continue
#     if re.match('[tT]ab', child.get_text()):
#         if isinstance(child.next_sibling, NavigableString):
#             child.next_sibling.replace_with('Table' + str(child.next_sibling.string))
#             child.extract()
#             continue
#         elif isinstance(child.previous_sibling, NavigableString):
#             child.previous_sibling.replace_with(str(child.previous_sibling.string) + ' Table')
#             child.extract()
#             continue
# # if find_count(str(child.next_sibling.string),'(') < find_count(str(child.next_sibling.string), ')'):
# #     for target in list(child.previous_siblings):
# #         #print(target.string)
# #         #print(str(target.string).find('('))    #find的是字符串的位置，没找到返回-1         注意find函数是节点的find还是字符串的find
# #         if str(target.string).find('(')>=0:                           #就用target不用反而解决了target是tag对象在调string方法时报错，反正html也是<>
# #             break
# #         target.extract()

#特殊例子
'10.1134_S1070328420050012'
'10.1007/s11243-020-00400-0'
'10.1007/s11243-016-0079-7'
'10.1007/s11243-009-9293-x'
'10.1007_s10904-010-9406-1' #给化学元素赋值
'10.1007/s11243-009-9195-y'
'[Cu2(bpp)(μ-CH3COO)4]·2H2O'
'1,3-bis(4-pyridyl)propane]'
'10.1007/s11224-010-9684-9'
{'1': '{M(Hnico)3M′}n', '2': 'Ni2+', '3': 'Co2+'}
'10.1007/s10876-011-0416-0'
{'1': 'Gd3+', '2': 'Tb3+', '3': 'Ho3+'}
'10.1007/s10876-010-0327-5'
{'1': '[Er2(pyba)3(μ3-OH)2(μ2-OH)(H2O)]n', '3': 'Y(2)'}
'10.1007_s11224-009-9447-7'
'相似段落'
'10.1007/s10904-010-9439-5'
'相似段落'
'10.1007_s11243-017-0118-z'
'相似段落'
'10.1007/s11224-007-9205-7'
'10.1007/s10904-019-01136-w'
'错误解读'
'10.1007/s11224-011-9888-7'
'相似段落 and'
'10.1007/s12039-016-1179-9'
'[Cu II(pdz)X 2], X: Cl, 1 and Br, 2.'
