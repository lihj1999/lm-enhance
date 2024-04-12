# from habanero import Crossref
# import pandas as pd
# import csv
# cr = Crossref()
# #选出2000年后的发表的文献
# def get_year(index):
#     flag = 0
#     try:
#         doi = list1[i]
#         article = cr.works(ids=doi)
#         year = article['message']['issued']['date-parts'][0][0]
#         print(year)
#         list2.append(int(year))      #字符型转为整数型
#     except:
#         dic[index] = doi
#         return 1
#
# df = pd.read_csv('count_publisher1016.csv', header=0)
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
# print(list2)
# df.insert(3, 'year', list2)
# df = df.loc[df['year'].astype(int)>2000]
# df.to_csv('count_year_publiser1016.csv', index=False)
# exit()

# import sys
# sys.path.append("..")
# from elsapy_master.elsapy.elsclient import ElsClient
# from elsapy_master.elsapy.elsprofile import ElsAuthor, ElsAffil
# from elsapy_master.elsapy.elsdoc import FullDoc, AbsDoc
# from elsapy_master.elsapy.elssearch import ElsSearch
import json,requests,re
import pandas as pd
from bs4 import BeautifulSoup
import xml.etree.ElementTree as et
import regex
from glob import glob
import csv
from bs4.element import NavigableString
import unicodedata
import unicodedata
import regex as  re
from bs4.element import NavigableString,Tag,Script,ProcessingInstruction
import copy
import nltk
from nltk.corpus import wordnet
from pylatexenc.latex2text import LatexNodes2Text
import warnings
warnings.filterwarnings("ignore")

'''
    flag = 0表示当前文献未下载
    flag = 1表示当前文献能正常的完整下载文献正文的xml文档
    flag = 2表示当前文献不能正常下载，或者下载报警告
'''

#查询elsevier中文献对应p||标识符
def query_p2(list_article_doi):
    list = []
    header = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36 Edg/110.0.1587.57',
        "Cookie": 'utt=0351a4ff5e9a1818c1f8f0563f7794d9d62020b; OptanonAlertBoxClosed=2023-02-19T07:12:16.094Z; appRetURL=https%3A%2F%2Fwww.sciencedirect.com%2Fuser%2Frouter%2Fshib%3FtargetURL%3Dhttps%253A%252F%252Fwww.sciencedirect.com%252Fuser%252Frouter%252Flogin%253FtargetURL%253Dhttp%25253A%25252F%25252Fwww.sciencedirect.com%25252F%7Chttps%253A%252F%252Fpassport.escience.cn%252Fidp%252Fshibboleth%7C.sciencedirect.com%7CWAYFLESS; at_check=true; AWSELB=D343415516251A3F54556BE7FECC9D3D1C564FABC227474855E1850C96F7B599DC2160491488F63E6F25015D23CECB8DD9F01904CDE5835762433F4A2CB295033A3D136BC0; AWSELBCORS=D343415516251A3F54556BE7FECC9D3D1C564FABC227474855E1850C96F7B599DC2160491488F63E6F25015D23CECB8DD9F01904CDE5835762433F4A2CB295033A3D136BC0; JSESSIONID=DD57D87631D627D1AD6270CDAB720201; soStatus="{\"statusChecked\":true}"; AA_INFOv2="{\"visitor\":{\"accessType\":\"ae:REG:U_P:GUEST:\",\"accountId\":\"ae:333931\",\"accountName\":\"ae:Elsevier APIs Guest Account\",\"ipAddress\":\"172.104.101.151\",\"userId\":\"ae:151823085\"}}"; OptanonConsent=isGpcEnabled=0&datestamp=Wed+Mar+01+2023+09%3A49%3A49+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=202301.2.0&isIABGlobal=false&hosts=&consentId=52ff910d-b014-4bc0-aa88-8da84f5b6c66&interactionCount=1&landingPath=NotLandingPage&groups=1%3A1%2C3%3A1%2C2%3A1%2C4%3A1&geolocation=CN%3B&AwaitingReconsent=false; correlationId=_m8PWhQJAjRykiXsE4jYAqSMhJW6S2H5; s_sess=%20s_cpc%3D0%3B%20e41%3D1%3B%20s_cc%3Dtrue%3B%20s_ppvl%3Did%25253Acontinue_to_client_screen_session_jsoff%252C100%252C100%252C961%252C1873%252C961%252C1920%252C1080%252C1%252CP%3B%20s_ppv%3Dec%25253Aauthors%25253Apolicies-and-guidelines%25253Axml-in-science-publishing%252C83%252C43%252C1681.7500610351562%252C1873%252C961%252C1920%252C1080%252C1%252CP%3B; OptanonAlertBoxClosed=2023-03-01T02:36:22.258Z; OptanonConsent=isGpcEnabled=0&datestamp=Wed+Mar+01+2023+10%3A36%3A23+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=202301.2.0&isIABGlobal=false&hosts=&consentId=52ff910d-b014-4bc0-aa88-8da84f5b6c66&interactionCount=1&landingPath=NotLandingPage&groups=1%3A1%2C3%3A1%2C2%3A1%2C4%3A1&geolocation=CN%3B&AwaitingReconsent=false; s_pers=%20v8%3D1677638192525%7C1772246192525%3B%20v8_s%3DLess%2520than%25201%2520day%7C1677639992525%3B'}
    for i in range(len(list_article_doi)):
        article_doi = list_article_doi[i]
        url = 'https://api.elsevier.com/content/article/doi/{doi}'.format(doi=article_doi)
        try:
            response = requests.get(url, headers=header)
            soup = BeautifulSoup(response.text, 'lxml')
            soup.select('link[rel=scidir]')[0].attrs['href']
            url = soup.select('link[rel=scidir]')[0].attrs['href']
            print(url)
            list.append(url)
        except:
            list.append('error')
    return list
    # df = pd.read_csv('count_year_publiser1016.csv', header=0)
    # list_doi = df['doi']
    # list_url = query_p2(list_doi)
    # df.insert(4, 'url', list_url)
    # df.to_csv('count_year_url_publiser1016.csv', index=False)

def save_xml(response,path):
    with open(path + '.html', 'wb') as f:
        #f.write(str(response).encode())
        f.write(response.content)

#下载xml
def download_xml(df):
    list_urls, list_years, list_dois = df['urls'] ,df['year'] ,df['doi']
    #初始状态
    #list_flags = [0]*len(df['urls'])
    list_flags = df['flags']
    con_file = open("config.json")
    config = json.load(con_file)
    api_key = config['apikey']
    headers = {
        "Accept": "text/xml",
        "X-ELS-APIKey": api_key
    }
    for i in range(len(list_urls)):
        try:
            url = list_urls[i]
            response = requests.get(url, headers=headers)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'lxml-xml')
            #article_text = soup.find('ce:sections')
            article_text = soup.find_all('ce:sections')
            #将bs4.element.ResultSet类型转换为bs4.BeautifulSoup类型，便于使用find函数进行精确定位
            new_soup = BeautifulSoup(str(article_text[0]),'lxml-xml')                          #str(article_text[0])意外的做了一个报错提示
            # print(new_soup)
            orginal_text = new_soup.find_all('para')
            #print(article_text.contents)
            rename = 'DOI_10.1016_' + list_dois[i][list_dois[i].find('/') + 1:] + '_' + str(list_years[i])
            for j in range(len(orginal_text)):                                                #不要在两个循环内同用一个i变量
                with open(rename + '.html', 'ab+') as f:
                    f.write(str(orginal_text[j]).encode())
                    f.write('<br>'.encode())
                #print(orginal_text[j].text)
            print(list_dois[i])
            list_flags[i] = 1
            #print(article_text[2].contents)
            #save_xml(article_text,rename)
        except:
            print('download error')
            list_flags[i] = 2
    return list_flags


def contact(df):
    base_domain = 'https://api.elsevier.com/content/article/pii/'
    list_urls = df['url']
    list_urls = [base_domain + list_urls[i][list_urls[i].rfind('/')+1:] for i in range(len(list_urls))]
    df.insert(4, 'urls', list_urls)
    df.to_csv('count_year_url_publiser1016.csv', index=False)

def orignaltext_batch_process():
    df = pd.read_csv('count_year_url_publiser1016.csv', header=0)
    print(len(df))
    list_html = glob('./1016-process/*.html')
    print(len(list_html))
    dois = [list_html[i][list_html[i].find('_')+1:list_html[i].rfind('_')] for i in range(len(list_html))]
    dois = [dois[i].replace('_','/') for i in range(len(dois))]
    years = [list_html[i][list_html[i].rfind('_')+1:list_html[i].rfind('.')] for i in range(len(list_html))]
    pattern_excess_text = r'\(\)' + '|' r'\[\s*([-,]+\s*)*\s*\]'
    with open('Dataset.csv', 'a', newline="", encoding='utf-8') as f:                     # 写改为追加的方式；‘ab+’以二进制的形式写入
        writer = csv.writer(f)
        header = 'doi', 'year', 'count', 'number', 'paras', 'label'
        writer.writerow(header)
    for j in range(len(list_html)):            #len(list_html)
        print(dois[j])
        with open(list_html[j],'r',encoding = 'utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')    #features='lxml'
            orginal_text = soup.find_all('sections')
            # para子节点的个数
            counts = len(orginal_text[0].find_all('para'))
            print(counts)
            #print([tag['id'] for tag in orginal_text[0].find_all('para')])

            number, paras = 0, []
            if 'section' not in [tag.name for tag in orginal_text[0].contents]:
                number_result, paras_result = titletag_merge_paratag(orginal_text[0])
                number += number_result
                lp = len(paras)
                for i, para in enumerate(paras_result):
                    paras_result[i] = '第{}段 :'.format(i + lp + 1) + re.sub(r'\s+',' ',re.sub(pattern_excess_text, '', para).replace('\n', ''))
                paras += paras_result
                print('>>>>>>>>>><<<<<<<<<<<<<<')
            if 'section' in [tag.name for tag in orginal_text[0].contents] and 'para' in [tag.name for tag in orginal_text[0].contents]:
                indexs = [index for index, value in enumerate(orginal_text[0].contents) if value.name == 'para']
                lp = len(paras)
                for i,index in enumerate(indexs):
                    paras += ['第{}段 :'.format(i+ lp +1) + unicodedata.normalize('NFKC',re.sub(r'\s+',' ',re.sub(pattern_excess_text, '',orginal_text[0].contents[index].get_text()).replace('\n','')))]
                number += len(indexs)
            #print([i['id'] for i in orginal_text[0].find_all("section")])           #虽是同名节点，但是按照父节点在子节点之前的顺序排列
            for element in orginal_text[0].find_all("section"):                              #此处不是对某一节点而是所有的section节点
                #print(element.name)
                if 'section' in [tag.name for tag in del_n(element.contents)] and 'para' in [tag.name for tag in del_n(element.contents)]:
                    print(1)
                    if 'section-title' in [tag.name for tag in del_n(element.contents)]:
                        index = [tag.name for tag in del_n(element.contents)].index('section-title')
                        if del_n(element.contents)[index + 1].name == 'para':
                            if len(del_n(element.contents)[index + 1].contents) > 1:
                                local = del_n(element.contents)[index + 1].contents[0]
                                for child in del_n(element.contents)[index].contents:
                                    local.insert_before(child)
                                local.insert_before('. ')
                    indexs = [index for index, value in enumerate(del_n(element.contents)) if value.name == 'para' or value.name == 'span']               #找出列表中的特定元素，甚至section——title的合并
                    lp = len(paras)
                    for i,index in enumerate(indexs):
                        paras += ['第{}段 :'.format(i+ lp + 1) + unicodedata.normalize('NFKC', re.sub(r'\s+',' ',re.sub(pattern_excess_text, '',del_n(element.contents)[index].get_text()).replace('\n', '')))]             #将unicode字符串unistr进行规范化
                    number += len(indexs)

                if 'section' not in [tag.name for tag in del_n(element.contents)]:
                    number_result, paras_result = titletag_merge_paratag(element)
                    number += number_result
                    lp = len(paras)
                    for i,para in enumerate(paras_result):
                        paras_result[i] = '第{}段 :'.format(i + lp + 1) + re.sub(r'\s+',' ',re.sub(pattern_excess_text, '', para).replace('\n', ''))
                    paras += paras_result
                    print('>>>>>>>>>><<<<<<<<<<<<<<')


            # print(list(set(paras)))
            # print(len(list(set(paras))))
                #else:                                                       #sections节点里有section和para子节点

            # # 对两种不同的构造进行循环，因为最多是三级标题故只需两个循环即可     测试过程中有四级标题出现
            # number, paras = 0, []                                    # 段落数量需要相加，段落文本需要列表拓展
            # if 'section' not in [tag.name for tag in orginal_text[0].contents]:
            #     number_result, paras_result = titletag_merge_paratag(orginal_text[0])
            #     number += number_result
            #     paras += paras_result
            #     print('>>>>>>>>>><<<<<<<<<<<<<<')
            # else:
            #     for i, content in enumerate(orginal_text[0].contents()):  # sections     tag属性
            #         if 'section' == content.name:
            #             number_result, paras_result = titletag_merge_paratag(content)
            #             number += number_result
            #             paras += paras_result
            #         else:
            #             for i, content in enumerate(orginal_text[0].find_all('section')):  # sections     tag属性
            #                 if 'section' not in [tag.name for tag in del_n(content.contents)]:
            #                     number_result, paras_result = titletag_merge_paratag(content)
            #                     number += number_result
            #                     paras += paras_result
            #     print('>>>>>>>>>><<<<<<<<<')

            # for i, content in enumerate(orginal_text[0].contents):  # sections
            #     # print(len(content.contents))                               #contents内的元素是tag类型
            #     if 'section' not in [tag.name for tag in del_n(content.contents)]:
            #         number_result, paras_result = titletag_merge_paratag(content)
            #         number += number_result
            #         paras += paras_result
            #         print('>>>>>>>>>><<<<<<<<<<<<<<')
            #     else:
            #         for child in content.find_all('section'):  # section
            #             if 'section' not in [tag.name for tag in del_n(child.contents)]:
            #                 number_result, paras_result = titletag_merge_paratag(child)
            #                 number += number_result
            #                 paras += paras_result
            #         #print('>>>>>>>>>><<<<<<<<<')
            if number != len(paras):
                print('{}分段错误'.format(url))
                # continue
            # print(paras)
            # exit()
            data = []
            data.append([dois[j],years[j],counts,len(paras), paras, number * [0]])
            with open('Dataset.csv', 'a', newline="", encoding='utf-8') as f:                    # 写改为追加的方式；‘ab+’以二进制的形式写入
                writer = csv.writer(f)
                for line in data:
                    writer.writerow(line)

'''有一种情况是二级标题直接后面加文本内容，不经过三级标题'''

def test_download(url):
    # con_file = open("config.json")
    # config = json.load(con_file)
    # api_key = config['apikey']
    # headers = {
    #     "Accept": "text/xml",
    #     "X-ELS-APIKey": api_key
    # }
    # response = requests.get(url, headers=headers)
    # soup = BeautifulSoup(response.text, 'lxml-xml')
    # # print(soup.prettify())
    # # article_text = soup.find('ce:sections')
    # # exit()
    # article_text = soup.find_all('ce:sections')
    # #article_text = regex.sub(r"(?<=<.+?>)\n(?=<.+?>)", "", str(article_text[0]))                   #另外一种解决xml转html后换行符也成为节点的问题
    #
    # # 将bs4.element.ResultSet类型转换为bs4.BeautifulSoup类型，便于使用find函数进行精确定位
    # new_soup = BeautifulSoup(str(article_text[0]), 'lxml-xml')              #str(article_text[0])意外的做了一个报错提示   此时已不再是xml结构了，无ce命名空间
    #print(new_soup.prettify())

    # with open('gai1.html', 'w',encoding='utf-8') as f:
    #     f.write(str(new_soup))                                              #易错点f.write(new_soup.text.encode())中的text方法只将beautiful soup对象的文本内容保存了下来，

    # with open('gai1.html','r',encoding = 'utf-8') as f:
    #     new_soup = BeautifulSoup(f.read(), features='lxml')
    with open('./原始文本/DOI_10.1016_j.aca.2018.10.022_2019.html', 'r', encoding='utf-8') as f:
        new_soup = BeautifulSoup(f.read(), features='lxml')
    orginal_text = new_soup.find_all('sections')
    print(len(orginal_text[0].find_all('para')))
    exit()
    #print(orginal_text)

    #想删除重复的'\n'子节点，'\n'节点位于两个子节点之间  甚至是父节点与子节点之间
    orginal_text[0].contents = del_n(orginal_text[0].contents)

    #para子节点的个数
    counts = len(orginal_text[0].find_all('para'))
    #print(counts)

    #对两种不同的构造进行循环，因为最多是三级标题故只需两个循环即可
    number, paras = 0,[]                                      #段落数量需要相加，段落文本需要列表拓展
    print(len(new_soup.find_all("section")))
    for element in new_soup.find_all("section"):
        if 'section' not in [tag.name for tag in del_n(element.contents)]:
            number_result,paras_result = titletag_merge_paratag(element)
            number += number_result
            paras += paras_result
            print('>>>>>>>>>><<<<<<<<<<<<<<')
    if number != len(paras):
        print('{}分段错误'.format(url))
        #continue
    data = []
    data.append([number,paras,number*[0]])
    with open('result dataset.csv','a',newline="",encoding='utf-8')as f:           #写改为追加的方式；‘ab+’以二进制的形式写入
        writer = csv.writer(f)
        header = 'doi', 'year','count','paras','label'
        writer.writerow(header)
        for line in data:
            writer.writerow(line)


        #print([tag.name for tag in del_n(content.contents)])
        # print(content.contents[3])
        # print(content.contents[5])
        # print(content.contents[3].find_next_sibling())                          #find_next_sibling不会包括空值
    print('...下载完成...')

#将段落总结（section-title）的内容嵌入段落内部（paratag）,返回一个列表包含
def titletag_merge_paratag(content):
    texts= []
    tags = del_n(content.contents)
    tag_names = [tag.name for tag in tags]
    # 10.1016/j.jssc.2004.02.023 仅有section-title     10.1016/j.molstruc.2018.04.080  section——title被删除
    if ('section-title' in tag_names and len(tag_names) == 1) or len(tag_names) == 0:
        return 0, []
    #print(tag_names)
    #段落标题在子节点列表中的位置
    if 'section-title' in tag_names:
        index = tag_names.index('section-title')
        title = tags[index].text.replace("\n", "")
        title = re.sub(r'^\d(.\d)*([A-z]+)',r'\2',title)      #标题2.2Synthesis of
    else:                                                                              #该sections的子节点全部是段落            不用试探，其传下来的sections的子节点
        index = -1
        title = ''
    #print(tags[index])                                                                #index返回第一个匹配元素的位置，此处在section节点中section-title对应一个para
    # print(count)
    print(tag_names)

    for element in tags[index+1:]:
        #print(element.prettify())
        for hyperlink in element.find_all(["cross-refs", "cross-ref", "footnote", "footnotes"]):
            #print(hyperlink)
            hyperlink.extract()
            #print(element.name)
        # print(text1.replace("\n", " "))
        # print(element.text.replace("\n", " "))
        # print('>>>>>>><<<<<<<<<<<<<<<<')
        texts.append(unicodedata.normalize('NFKC',element.text.replace("\n"," ")))
    texts[0] = title + ' ' + texts[0]
    #print(texts)
    #print(len(texts))

    return len(texts),texts

def parsing(file):
    elements = []
    text_list = []
    with open(file, 'r',encoding = 'utf-8') as f:
        soup = BeautifulSoup(f, 'lxml')
    # print(soup.prettify())                                                                                          #为什么要去除换行符的问题
    # exit()
    for element in soup.find_all(["ce:section", "ce:para", 'ce:section-title']):
        for hyperlink in element.find_all(["ce:cross-refs", "ce:cross-ref", "ce:footnote", "ce:footnotes"]):          #for循环为了去除文献中的引用
            # print(element)
            hyperlink.extract()
            # print(hyperlink.extract())
            # print(element)
            # exit()

        text = _cleanup_tag(element)
        #1 print('>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
        elements.append(element)
        text_list.append(text)
        #print(text)
    print(text_list)


        # if not text or text in text_list:
        #     continue
        # elif element.name in ["ce:abstract-sec", "ce:para"]:
        #     element = Paragraph(text)
        # elif element.name in ['ce:section-title']:
        #     element = Heading(text)
        # else:
        #     raise ReaderError('Can not parse these paper')
        #
        # elements.append(element)
        # text_list.append(text)

    if not elements:
        print('There are no paragraph in paper')

    return elements

'''为什么html文档的tag对象中的文本内容打印后有许多的换行符;HTML中的标签元素通常会被包围在标签的开始标记和结束标记之间，并且开始和结束标记与文本之间也存在空格。当我们获取标签元素的文本内容时，这些空格和换行符也会被包括在内。'''
def _cleanup_tag(element):
    #1 print(element)
    remove_space = regex.sub(r"(?<=<.+?>)\n(?=<.+?>)", "", str(element))                    #可以不让’/n‘作为子节点之一了
    #1 print(remove_space)
    text = BeautifulSoup(remove_space, 'lxml').get_text()
    return text.replace("\n", " ")                                                          #有部分节点包含许多链接，装换格式后变成/n符         其实可以直接替换成空元素，即可不用第一步删除子节点

def del_n(contents):                #变量命名不能和方法函数命名一样           一共三种节点sections，section，section_title, label,para
    list1 = list(set(contents))
    #列表去重保留原有顺序
    list1.sort(key = contents.index)
    if '\n' in list1:
        list1.remove('\n')
    return list1

def download_html(df):
    list_urls, list_years, list_dois = df['urls'], df['year'], df['doi']
    con_file = open("config.json")
    config = json.load(con_file)
    api_key = config['apikey']
    headers = {
        "Accept": "text/xml",
        "X-ELS-APIKey": api_key
    }
    for i in range(len(list_urls)):
        try:
            url = list_urls[i]
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'lxml-xml')
            article_text = soup.find_all('ce:sections')
            new_soup = BeautifulSoup(str(article_text[0]),'lxml-xml')           #str会减少换行节点的出现
            rename = 'DOI_10.1016_' + list_dois[i][list_dois[i].find('/') + 1:] + '_' + str(list_years[i])
            with open(rename + '.html', 'w',encoding='utf-8') as f:
                f.write(str(new_soup))
            print(url)
        except:
            print('download error')

def preprocess():        #10.1134/S0036023619090195复杂
    df = pd.read_csv('count_year_url_publiser1016.csv', header=0)
    df_doi = df['doi']
    vals = [{}]*len(df)
    df.insert(loc=len(df.columns),column='name_dicts', value=vals)   #loc=0
    df.insert(loc=len(df.columns), column='compound_dicts', value=vals)
    list_html = glob('./1016/*.html')     #1016-process

    # doi_list = list(df_doi)
    # index = []
    # num = 0
    # for i in range(len(list_html)):
    #     if list_html[i][11:-10].replace('_','/') in doi_list:
    #         index.append(doi_list.index(list_html[i][11:-10].replace('_','/')))
    #         num += 1
    #         if df['flags'].iloc[doi_list.index(list_html[i][11:-10].replace('_','/'))] != 1:
    #             print(list_html[i][11:-10])
    #             df['flags'].iloc[doi_list.index(list_html[i][11:-10].replace('_', '/'))] = 1
    # print(num)
    # df.to_csv('count_year_url_publiser1016.csv', index=False)
    # exit()

    dois = [list_html[i][list_html[i].find('_') + 1:list_html[i].rfind('_')] for i in range(len(list_html))]
    dois = [dois[i].replace('_', '/') for i in range(len(dois))]
    years = [list_html[i][list_html[i].rfind('_') + 1:list_html[i].rfind('.')] for i in range(len(list_html))]
    for j in range(len(list_html)):  # len(list_html)
        index = df[df.doi == dois[j]].index.tolist()[0]
        print(dois[j])
        # index = df[df.doi == dois[j]].index.tolist()[0]
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
        for element in soup.find_all(text=lambda text: isinstance(text, str) and text.strip() == ''):
            element.extract()
        for element in soup.find_all(text=lambda text: text is not None and re.search(r'\s*\n\s*',text)):
            element.string.replace_with(re.sub(r'\s*\n\s*',' ',element.string))
        for element in soup.find_all(lambda tag: isinstance(tag, Tag) and tag.get_text().strip() == ''):
            element.extract()
        display_tags = [tag for tag in soup.find_all('display')]
        for tag in display_tags:
            tag.extract()

        #print(soup.prettify())
        # 10.1016/j.ica.2015.07.016  带单位的字符串节点前有空格节点，在爱斯维尔的api下载后会生成一个hsp节点
        hsp_tags = [tag for tag in soup.find_all(text=lambda text: text is not None) if isinstance(tag.previous_sibling, NavigableString)]
        for tag in hsp_tags:
            if tag.previous_sibling[-1] == '·':
                continue
            tag.string.replace_with(' '+tag.string)

        for hyperlink in soup.find_all(["cross-refs", "cross-ref", "footnote", "footnotes"]):  #10.1016/j.inoche.2011.08.009   10.1016/j.inoche.2016.07.006  10.1016/j.inoche.2016.11.024
            hyperlink.extract()


        #10.1016/j.inoche.2017.06.021  实验部分在致谢之后

        metals = ['Si', 'K', 'Ce', 'La', 'Mo', 'Fe', 'Ru', 'W', 'Ba', 'Ga', 'Sm', 'Ho', 'Zr', 'Be', 'Y', 'Cd', 'As', 'Yb', 'V', 'Er', 'Ca', 'Lu', 'Ag', 'Cu', 'Na', 'Dy', 'U', 'Tb', 'Mg', 'Co', 'Zn', 'Li', 'Mn', 'In', 'Ni', 'Sr', 'Eu', 'Nd', 'Sc', 'Th', 'Gd', 'Bi', 'Cs', 'Pr', 'Al', 'Pb', 'Hg']
        elements = ['Si', 'K', 'Ce', 'La', 'Mo', 'Fe', 'Ru', 'W', 'Ba', 'Ga', 'Sm', 'Ho', 'Zr', 'Be', 'Y', 'Cd', 'As',
                  'Yb', 'V', 'Er', 'Ca', 'Lu', 'Ag', 'Cu', 'Na', 'Dy', 'U', 'Tb', 'Mg', 'Co', 'Zn', 'Li', 'Mn', 'In',
                  'Ni', 'Sr', 'Eu', 'Nd', 'Sc', 'Th', 'Gd', 'Bi', 'Cs', 'Pr', 'Al', 'Pb', 'Hg', 'Cl', 'Br', 'Si']

        pattern_item = r'[A-Za-z\)\[\]\·\-\{](\d|\∞|}n|]n|\)n|\·){1}((\.\d+)|[A-Za-z\(\)\[\]|\{|\}])+'    #r'[A-Za-z\(\)\[\]\·]+(\d|\∞|}n|]n|\)n){1}[A-Za-z\(\)\[\]\·]*' 避免(2017).这样的错误指代词 10.1007/s10876-020-01848-x  结尾部分该不该加*
        pattern_metal = r'(?:{})'.format('|'.join(metals))
        pattern_element = r'(?:{})$'.format('|'.join(elements))
        pattern_element_change = r'(?:{})'.format('|'.join(elements))
        pattern_element_charge = r'(?:{})\,'.format('|'.join(elements))
        pattern_1 = r'\(\S+\)'  #[Sc(HCOO)(bdc)]
        patt_equ = r'\s*=\s*(\S+)'
        patt_equ_split = r'([\S|*]+)\s*=\s*(\S+)'     #10.1039/b008807m处改善
        patt_compounds = r'[\d|N](,[\d|N](′)*)*-[A-Za-z]{2,}'
        patt_math_formula = r'[^0-9]\/\d+'    #可能是公式

        # # b节点变成strong或者是span.bold节点
        # bold_tags = [tag for tag in list(soup.select('bold'))]
        # for tag in bold_tags:
        #     target_text = tag.get_text()
        #     b_node = soup.new_tag('bold')
        #     b_node.string = target_text
        #     tag.insert_before(b_node)
        #     tag.extract()

        #统一small和  sub节点或者时sup节点
        small_to_strong = [tag for tag in soup.find_all('inf') if not tag.find_parents('inf')]
        for tag in small_to_strong:
            #10.1016/j.ica.2012.08.027的  <section-title>Synthesis of [Cu(L)(N3)]<italic>n</italic> (2)</section-title>
            if isinstance(tag.parent,Tag):
                if tag.parent.name == 'italic':
                    tag.parent.name = 'sub'
                    tag.parent.string = tag.text
                    tag.extract()
                    continue
            if len(tag.contents) == 1:
                tag.name = 'sub'

        italic_bold_tags = [tag for tag in soup.find_all('italic') if isinstance(tag.parent,Tag) ]
        for tag in italic_bold_tags:   #10.1016/j.jorganchem.2003.10.024
            if tag.parent and tag.parent.name == 'bold':
                tag.parent.string = tag.text
                tag.extract()


        subs = [tag for tag in soup.find_all('sub') if tag.find_all('bold') and not tag.find_parents('sub') and len(tag.contents) == 1]
        for parent in subs:
            child = parent.contents[-1]
            parent.name = "bold"
            child.name = "sub"

        #10.1016_j.ica.2019
        section_title_tag = [tag for tag in list(soup.find_all('section-title')) if isinstance(tag.next_sibling,Tag)]
        for tag in section_title_tag:
            if tag.next_sibling.name == 'section':
                local = tag.next_sibling.contents[0].contents[0]
                for child in tag.contents:
                    local.insert_before(child)
                local.insert_before('. ')
                tag.extract()

        #文本人为的编辑错误  10.1039/b102131c
        text_tag = [tag for tag in soup.find_all(text=lambda text: text is not None and re.search(r'\s+\)' + '|' + r'\(\s+', text)) if isinstance(tag,NavigableString)]
        for tag in text_tag:
            tag.string.replace_with(re.sub(r'\(\s+','(',re.sub(r'\s+\)',')',tag.string)))
        text1_tag = [tag for tag in soup.find_all(text=lambda text: text is not None and re.search(r'\(\S+\-(\S+\s+\S+)\-\S+\)', text)) if isinstance(tag, NavigableString)]
        for tag in text1_tag:
            wd = re.search(r'\(\S+\-(\S+\s+\S+)\-\S+\)', tag.string).group(1)
            word = re.sub('\s+', '', re.search(r'\(\S+\-(\S+\s+\S+)\-\S+\)', tag.string).group(1))
            if is_english_word(word):
                tag.string.replace_with(tag.string.replace(wd,word))
        text2_tag = [tag for tag in soup.find_all(text=lambda text: text is not None and re.search(r'(\S+)=(\S+)',text)) if isinstance(tag,NavigableString)]
        for tag in text2_tag:
            tag.string.replace_with(re.sub(r'(\S+)=(\S+)',r'\1 = \2',tag.string))
        #BUT-20 and -21
        text2_tag = [tag for tag in soup.find_all('bold') if isinstance(tag.next_sibling,NavigableString) and isinstance(tag.next_sibling.next_sibling,Tag)]
        for tag in text2_tag:
            if tag.text.find('-')>-1:
                if tag.next_sibling.string == ' and ' and tag.next_sibling.next_sibling.text[0]=='-' and len(tag.next_sibling.next_sibling.contents) == 1:
                    target_text = tag.text[:tag.text.find('-')]
                    tag.next_sibling.next_sibling.string = target_text + tag.next_sibling.next_sibling.string
        #10.1016/j.carres.2007.08.022
        text3_tag = [tag for tag in soup.find_all(text=lambda text: text is not None and re.search(r'\s+α-', text)) if isinstance(tag, NavigableString)]
        for tag in text3_tag:
            tag.string.replace_with(re.sub(r'\s+α-','α-',tag.string))


        sbu_tag = [tag for tag in soup.find_all(string=lambda string: string is not None and re.match(r'\s+SBU\w{0,1}\s+',string)) if tag.previous_siblings]
        for tag in sbu_tag:
            string = ''
            target_text = ''
            for i in tag.previous_siblings:
                if isinstance(i, NavigableString):
                    string = re.sub(r'\s+', ' ', i.string) + string  # 不能用+=,因为存入字符串的顺序要使得新存入的字符串压入最末尾
                elif isinstance(i, Tag) and i.name == 'sub':
                    string = re.sub(r'\s+', ' ', i.text) + string
                elif isinstance(i, Tag) and i.name == 'sup':
                    string = re.sub(r'\s+', ' ', i.text) + string
                elif isinstance(i, Tag) and i.name == 'small':
                    string = re.sub(r'\s+', ' ', i.text) + string
                elif isinstance(i, Tag) and i.name == 'italic':
                    string = re.sub(r'\s+', ' ', i.text) + string
                elif isinstance(i, Tag) and i.name == 'bold':
                    string = re.sub(r'\s+', ' ', i.text) + string
                elif isinstance(i, Tag) and i.name == 'span' and ('class' in i.attrs):
                    if i['class'][0] == 'c-stack' or i['class'][0] == 'italic':
                        string = re.sub(r'\s+', ' ', i.text) + string
                else:
                    break
            index1 = string.rfind(' ')
            target_text = string[index1:]
            if re.search(pattern_item,target_text):
                tag.string.replace_with(re.sub(r'\s+SBU\w{0,1}\s+',' ',tag.string))



        # 和10.1039/b102739p
        sub_tag = [tag for tag in soup.find_all('sub') + soup.find_all('italic')]
        for tag in sub_tag:
            tag.string = re.sub(r'\s+',' ',tag.text)


        #直接将一些可能的连接字符也转换成黑体节点  10.1039/c0dt01174f 2·5H2O 1-Fe  r'[A-Z]$' 10.1039/C6DT00414H  2L·KF
        pre_strong = [tag for tag in list(soup.find_all('bold',text=lambda text: text is not None and re.match(r'\d$' + '|' + r'[A-z]$', text))) if tag.next_sibling and (tag.parent.name == 'para' or tag.parent.name == 'th') and not tag.find_all()]
        for tag in pre_strong:
            if isinstance(tag.next_sibling,NavigableString):
                # print(tag)
                # print(tag.next_sibling)
                #替换一下顺序  10.1039/b810479d
                if tag.next_sibling.string[0] == '·' and tag.next_sibling.string.find(' ') == -1:  #or (tag.next_sibling.string[0] == '-' and tag.next_sibling.string )
                    # print(tag.next_sibling)
                    # print(tag.next_sibling.next_sibling)
                    target_text = tag.next_sibling.string
                    b_node = soup.new_tag('bold')
                    b_node.string = target_text
                    tag.next_sibling.extract()
                    tag.insert_after(b_node)
                    if tag.next_sibling.next_sibling:
                        if isinstance(tag.next_sibling.next_sibling,Tag):
                            if tag.next_sibling.next_sibling.name == 'sub':
                                b_node = soup.new_tag('bold')
                                b_node.append(tag.next_sibling.next_sibling)
                                #tag.next_sibling.next_sibling.extract()
                                tag.next_sibling.insert_after(b_node)
                                if tag.next_sibling.string[-1] == 'H' and isinstance(tag.next_sibling.next_sibling.next_sibling,NavigableString):
                                    if tag.next_sibling.next_sibling.next_sibling.string.find('O ') == 0 or tag.next_sibling.next_sibling.next_sibling.string.find('O)') == 0:
                                        tag.next_sibling.next_sibling.next_sibling.string.replace_with(tag.next_sibling.next_sibling.next_sibling.string[1:])
                                        strong_node = soup.new_tag('bold')
                                        strong_node.string = 'O'
                                        tag.next_sibling.next_sibling.next_sibling.insert_before(strong_node)
                            elif tag.next_sibling.next_sibling.name != 'bold':
                                continue
                        else:
                            continue


        # 10.1039/c0dt00864h  2-Mn
        strong_tag = [tag for tag in list(soup.find_all('bold')) if isinstance(tag.next_sibling, NavigableString) and tag.next_sibling.next_sibling and re.match(r'\d$',tag.text)]
        for tag in strong_tag:
            if tag.next_sibling.string == '-' and isinstance(tag.next_sibling.next_sibling, Tag):
                if re.match(pattern_element, tag.next_sibling.next_sibling.text):
                    target_text = tag.next_sibling.text
                    strong_node = soup.new_tag('bold')
                    strong_node.string = target_text
                    tag.next_sibling.insert_after(strong_node)
                    tag.next_sibling.extract()


        #rsc中多个黑体的节点可以并合处理   10.1039/b910994c
        strong_tags = [tag for tag in list(soup.find_all('bold')) if tag.next_sibling ]  #and not tag.find_parents('table')
        for tag in strong_tags:
            while isinstance(tag.next_sibling,Tag) and tag.next_sibling.text:
                if tag.next_sibling.name == 'bold' and tag.next_sibling.text[0] != ' ' and tag.text[-1] != ' ':
                    if tag.next_sibling.find_all():
                        for child in list(tag.next_sibling.contents):
                            tag.append(child)                  #append移动兄弟节点的位置
                        tag.next_sibling.extract()
                        # print(tag.text)
                        # print(tag.next_sibling)
                    else:  #扩展项
                        tag.append(tag.next_sibling.text)
                        tag.next_sibling.extract()
                else:
                    break



        # 避免b节点和字符串节点紧贴，且无空格
        string_b_tags = [tag for tag in soup.find_all('bold', text=lambda text: text is not None) if isinstance(tag.previous_sibling, NavigableString) and not tag.find_parents('sub') and not tag.find_parents('sup')]
        for tag in string_b_tags:
            if tag.previous_sibling.string[-1] == '(':
                pass
            elif (tag.previous_sibling.string[-1] != ' ' or tag.previous_sibling.string[-1] != '\xa0') and tag.next_sibling:
                if tag.next_sibling.string is None:
                    tag.previous_sibling.string.replace_with(tag.previous_sibling.string + ' ')
                elif tag.next_sibling.string[0] == ',' or tag.next_sibling.string[0] == '.' or (tag.next_sibling.string[0] == ' ' and is_english_word(tag.next_sibling.string, 0)):
                    tag.previous_sibling.string.replace_with(tag.previous_sibling.string + ' ')
                else:  # 此b节点在化学式之后作为一个代词
                    pass

        # 避免sub节点和之前字符串节点紧贴且有空格，
        string_b_tags = [tag for tag in soup.find_all('sub', text=lambda text: text is not None) if isinstance(tag.previous_sibling, NavigableString)]
        for tag in string_b_tags:
            if tag.previous_sibling.string[-1] == ' ':
                tag.previous_sibling.string.replace_with(
                    tag.previous_sibling.string[:len(tag.previous_sibling.string) - 1])

        # 避免sup节点和字符串节点紧贴，且无空格
        string_b_tags = [tag for tag in soup.find_all('sup', text='′') if isinstance(tag.previous_sibling, NavigableString)]
        for tag in string_b_tags:
            if tag.previous_sibling.string[-1] == ' ':
                tag.previous_sibling.string.replace_with(tag.previous_sibling.string[:len(tag.previous_sibling.string) - 1])



        #section小标题节点的特殊处理（Elsevier）
        section_tag = [tag for tag in list(soup.find_all('label')) if tag.parent.name == 'section' and (tag.text.find('.') == -1 or all(tag.name == 'section' for tag in list(tag.next_sibling.find_next_siblings())))]
        for tag in section_tag:
            if isinstance(tag.next_sibling,Tag):
                if tag.next_sibling.name == 'section-title':
                    tag.next_sibling.extract()
                tag.extract()



        section_tags = [tag for tag in list(soup.find_all('label')) if tag.next_sibling and not tag.find_next_siblings('section')]
        for tag in section_tags:
            if isinstance(tag.next_sibling,Tag):
                if tag.next_sibling.name == 'section-title':
                    # print(len(tag.next_sibling.contents))
                    # print(isinstance(tag.next_sibling.contents[-1], NavigableString))
                    # print(tag.find_all('sub'))
                    if isinstance(tag.next_sibling.contents[-1],NavigableString):
                        if re.match(r'\(\d\)',tag.next_sibling.contents[-1].string):
                            tag.next_sibling.contents[-1].string = ' ' + tag.next_sibling.contents[-1].string
                    if len(tag.next_sibling.contents) > 1 and isinstance(tag.next_sibling.contents[-1], NavigableString) and (tag.next_sibling.find_all('sub') or tag.next_sibling.find_all('italic')):
                        if tag.next_sibling.contents[-1].string.count(' ') > 1 or tag.next_sibling.contents[-1].string.find(' ') != 0:
                            tag.next_sibling.contents[-1].insert_after('. ')
                            continue
                        target_text = tag.next_sibling.contents[-1].string[1:]
                        if is_english_word(target_text):
                            continue
                        b_node = soup.new_tag('bold')
                        b_node.string = target_text
                        space = NavigableString(' ')
                        tag.next_sibling.contents[-1].insert_before(b_node)
                        tag.next_sibling.contents[-1].insert_after('. ')
                        tag.next_sibling.contents[-3].insert_before(space)
                        tag.next_sibling.contents[-2].extract()
                    else:
                        tag.next_sibling.contents[-1].insert_after('. ')
                    tag.extract()


        # with open(list_html[j], 'wb') as f:
        #     f.write(str(soup).encode())
        # exit()


        #10.1016/j.ica.2015.07.016
        section_title_tag = [tag for tag in list(soup.find_all('label')) if isinstance(tag.next_sibling,Tag)]
        for tag in section_title_tag:
            if tag.next_sibling.name == 'para':
                for child in tag.contents:
                    tag.next_sibling.contents[0].insert_before(child)

        #配合物的一些错误描述，(2, 2'-bipy)(H2O)] 多了一个空格
        compounds_excess = [tag for tag in soup.find_all(text=lambda text: text is not None and re.search(patt_compounds, text)) if tag.string]
        for tag in compounds_excess:
            tag.string.replace_with(re.sub(r'(N|\d),(\s+)(N|\d)',r'\1,\3',tag.string))


        #解码latex文本 专属于elsevier   10.1016/j.ica.2006.09.021
        # print(soup.prettify())

        mn_bold = [tag for tag in soup.find_all('mn') if 'mathvariant' in tag.attrs and len(list(tag.previous_siblings))>1]
        for tag in mn_bold:
            if tag['mathvariant'].find('bold') > -1:
                if tag.previous_sibling.text == '(' and tag.previous_sibling.previous_sibling.text[-1] != ' ':
                    tag.previous_sibling.string = ' ' + tag.previous_sibling.text


        math_tags = [tag for tag in soup.find_all('math')]
        for tag in math_tags:
            if len(tag.contents) == 1:
                for child in tag.descendants:
                    if isinstance(child,Tag) and len(child.contents) == 1:
                        if isinstance(child.contents[0],NavigableString):
                            if child.name == 'mi':
                                target_text = child.text
                                b_node = soup.new_tag('italic')
                                b_node.string = target_text
                                tag.insert_before(b_node)
                            elif child.name == 'mo':
                                tag.insert_before(child.text)
                            elif child.name == 'mn' and (child.find_parents('msub') or child.find_parents('msubsup')) and ('mathvariant' not in child.attrs):
                                target_text = child.text
                                b_node = soup.new_tag('sub')
                                b_node.string = target_text
                                tag.insert_before(b_node)
                            elif child.name == 'mn' and not (child.find_parents('msub') or child.find_parents('msubsup')) and ('mathvariant' not in child.attrs):
                                tag.insert_before(child.text)
                            elif child.name == 'mtext':
                                tag.insert_before(child.text)
                            if child.attrs and ('mathvariant' in child.attrs):
                                if child['mathvariant'].find('bold')>-1:  #and child['mathvariant']
                                    target_text = child.text
                                    b_node = soup.new_tag('bold')
                                    b_node.string = target_text
                                    tag.insert_before(b_node)
            elif len(tag.contents) > 1:
                print('有异常')
            tag.extract()



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
                        elif isinstance(pre_next, Tag) and pre_next.name == 'small':
                            next_string = next_string + re.sub(r'\s+[∙·⋅]\s+', '·', re.sub(r'\s+', ' ', pre_next.text))
                        elif isinstance(pre_next, Tag) and pre_next.name == 'italic':
                            next_string = next_string + re.sub(r'\s+[∙·⋅]\s+', '·', re.sub(r'\s+', ' ', pre_next.text))
                        elif isinstance(pre_next, Tag) and pre_next.name == 'bold':
                            next_string = next_string + re.sub(r'\s+[∙·⋅]\s+', '·', re.sub(r'\s+', ' ', pre_next.text))
                        elif isinstance(pre_next, Tag) and pre_next.name == 'sapn':
                            next_string = next_string + re.sub(r'\s+[∙·⋅]\s+', '·', re.sub(r'\s+', ' ', pre_next.text))
                        elif isinstance(pre_next, Tag) and pre_next.name == 'em':
                            next_string = next_string + re.sub(r'\s+[∙·⋅]\s+', '·', re.sub(r'\s+', ' ', pre_next.text))
                        elif isinstance(pre_next, Tag) and pre_next.name == 'small-caps':
                            next_string = next_string + re.sub(r'\s+[∙·⋅]\s+', '·', re.sub(r'\s+', ' ', pre_next.text))
                        else:
                            break
                    if re.search(pattern_item,next_string[1:next_string[1:].find(' ')+1]):
                        if len(list(tag.next_siblings))>2:     #next_sibling和next_element的不同
                            if isinstance(list(tag.next_siblings)[1],Tag) and isinstance(tag.previous_sibling,NavigableString):
                                continue
                        tag.next_sibling.string.replace_with(tag.next_sibling.string[1:])
                        #print(tag.next_sibling)

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
        spilt_text_and = [tag for tag in soup.find_all('bold', text=lambda text: text is not None and re.search(patt_text_and, text)) if tag.string]
        #print(len(spilt_text_and))
        for tag in spilt_text_and:
            # print(tag.string)
            # print(re.search(patt_text_and, tag.string).span())
            # print(tag.string[:re.search(patt_text_and, tag.string).span()[0]])
            # print(tag.string[re.search(patt_text_and, tag.string).span()[0]:re.search(patt_text_and, tag.string).span()[1]])
            # print(tag.string[re.search(patt_text_and, tag.string).span()[1]:])
            text = tag.string[re.search(patt_text_and, tag.string).span()[0]:re.search(patt_text_and, tag.string).span()[1]]
            b_next_node = soup.new_tag('bold')
            b_next_node.string = tag.string[re.search(patt_text_and, tag.string).span()[1]:]
            tag.string.replace_with(tag.string[:re.search(patt_text_and, tag.string).span()[0]])
            tag.insert_after(b_next_node)
            tag.insert_after(text)


        # test = [tag for tag in list(soup.find_all('bold',text=lambda text: text is not None and 'SBU2' in text))]   #text=lambda text: text is not None and 'Etypy' in text

        # 统一格式 Tb (7) Ce(9)数字代词前要有空格   10.1039_b900522f
        bold_num_tags = [tag for tag in list(soup.find_all('bold')) if re.match(r'\d$',tag.text) and isinstance(tag.next_sibling,NavigableString) and isinstance(tag.previous_sibling,NavigableString)]
        for tag in bold_num_tags:
            if len(tag.previous_sibling)>2 and len(tag.next_sibling)>2:
                if tag.previous_sibling.string[-1] == '(' and tag.previous_sibling.string[-2] != ' ' and tag.next_sibling.string[1] == ' ':
                    tag.previous_sibling.string.replace_with(tag.previous_sibling.string[:-1] + ' (')

        #规范格式(Ln = Pr,6;Nd,7;Y, 8).  10.1039/b911100j
        bold_num_tags = [tag for tag in list(soup.find_all('bold')) if re.match(r'\d$', tag.text) and isinstance(tag.previous_sibling,NavigableString)]
        for tag in bold_num_tags:
            if re.search(r'(?:{})\,$'.format('|'.join(elements)), tag.previous_sibling.string):
                tag.previous_sibling.string.replace_with(re.sub(r'((?:{})\,)$'.format('|'.join(elements)), r'\1 ',tag.previous_sibling.string))



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
        patt3_supp = r'\s+[–-−]\s+'   #将search修改一下
        line_tag = [tag for tag in list(soup.find_all(text=lambda text: text is not None and re.search(patt3_supp,text))) if tag.string]
        for i in line_tag:
            i.string.replace_with(re.sub(patt3_supp,'–', i.string))
        #与patt3的不一样的处理   #10.1007/s12039-015-0966-z
        patt4 = r'[–-−]\s+'
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
        #10.1039/c0dt01174f  [Zn (3-pytz)0.5(OH)0.5Cl]n
        patt7 = r'(\[\S+)\s+(\()'
        text_tag7 = [tag for tag in list(soup.find_all(text=lambda text: text is not None and re.search(patt7, text))) if tag.string]
        for i in text_tag7:
            i.string.replace_with(re.sub(patt7, r'\1\2', i.string))
        #10.1039/c0dt01718c   }IrCl(cod)]·2 CH
        patt8 = r'(\·\d+)\s+'
        text_tag8 = [tag for tag in list(soup.find_all(text=lambda text: text is not None and re.search(patt8, text))) if tag.string]
        for i in text_tag8:
            i.string.replace_with(re.sub(patt8, r'\1', i.string))

        patt9 = r'\]\('   #10.1039/c0jm01318h  使用match方法和下一个节点为strong节点
        text_tag9 = [tag for tag in list(soup.find_all(text=lambda text: text is not None and re.match(patt9, text))) if isinstance(tag.next_sibling, Tag)]
        for i in text_tag9:
            if i.next_sibling.name == 'bold':
                i.string.replace_with(re.sub(patt9, r'] (', i.string))


        #10.1039/c0dt01718c   [(cod)HIr{μ-B(mt)3}IrCl(cod)]·2CH2Cl211·2CH2Cl2
        sub_blank_strong_tags = [tag for tag in list(soup.find_all('sub',text=lambda text: text is not None and re.match('[\d]', text))) + list(soup.find_all('sup',text=lambda text: text is not None and re.match('[\d]', text))) if tag.next_sibling]
        for tag in sub_blank_strong_tags:
            #10.1039/c0dt01718c K+2−
            if isinstance(tag.next_sibling,Tag):
                if tag.next_sibling.name == 'bold' and re.match('[\d]', tag.next_sibling.text):
                    #elsevier特加  10.1016/S0020-1693(03)00195-6
                    if tag.next_sibling.next_sibling:
                        if isinstance(tag.next_sibling.next_sibling,Tag):
                            continue
                    tag.insert_after(' ')

        iupac_tags = [tag for tag in list(soup.find_all('sub',text = '2')) if tag.next_sibling and tag.previous_sibling]
        for tag in iupac_tags:
            string = ''
            wd =''
            if not tag.next_sibling.string or not tag.previous_sibling.string:
                continue
            if tag.next_sibling.string[0] == 'O' and tag.previous_sibling.string[-1] == 'H':
                for i in tag.previous_siblings:
                    if isinstance(i, NavigableString):
                        string = re.sub(r'\s+', ' ', i.string) + string      #不能用+=,因为存入字符串的顺序要使得新存入的字符串压入最末尾
                    elif isinstance(i, Tag) and i.name == 'sub':
                        string = re.sub(r'\s+', ' ', i.text) + string
                    elif isinstance(i, Tag) and i.name == 'sup':
                        string = re.sub(r'\s+', ' ', i.text) + string
                    elif isinstance(i, Tag) and i.name == 'small':
                        string = re.sub(r'\s+', ' ', i.text) + string
                    elif isinstance(i, Tag) and i.name == 'italic':
                        string = re.sub(r'\s+', ' ', i.text) + string
                    elif isinstance(i, Tag) and i.name == 'bold':
                        string = re.sub(r'\s+', ' ', i.text) + string
                    elif isinstance(i, Tag) and i.name == 'span':
                        string = re.sub(r'\s+', ' ', i.text) + string
                    elif isinstance(i, Tag) and i.name == 'em':
                        string = re.sub(r'\s+', ' ', i.text) + string
                    elif isinstance(i, Tag) and i.name == 'small-caps':
                        string = re.sub(r'\s+', ' ', i.text) + string
                    else:
                        break
                index1 = string.rfind(' ')
                index2 = string[:string.rfind(' ')].rfind(' ')
                if index1 > index2:
                    wd = string[index2 + 1:index1]
                if re.search(pattern_item, wd) and len(tag.previous_sibling.string) > 2:
                    if tag.previous_sibling.string.rfind(' ') > -1:
                        # [{Cupz)4SO4}{Cu(pz)4SO4(H2O)}]. H2O  这种情况
                        if tag.previous_sibling.string[tag.previous_sibling.string.rfind(' ') - 1] == '.':
                            continue
                        else:
                            tag.previous_sibling.string.replace_with(tag.previous_sibling.string[0:tag.previous_sibling.string.rfind(' ')] + tag.previous_sibling.string[tag.previous_sibling.string.rfind(' ') + 1:])
                    # 10.1007/s10847-007-9293-4
                    elif tag.previous_sibling.previous_sibling.string:
                        if tag.previous_sibling.previous_sibling.string.rfind(' ') > -1:
                            tag.previous_sibling.previous_sibling.string.replace_with(tag.previous_sibling.previous_sibling.string[0:tag.previous_sibling.previous_sibling.string.rfind(' ')] + tag.previous_sibling.previous_sibling.string[tag.previous_sibling.previous_sibling.string.rfind(' ') + 1:])


        patt_text = r'\(\S+\)\.'  # .在此种情况下只能是句号不可能是逗号
        excess = [tag for tag in soup.find_all('bold', text=lambda text: text is not None and re.search(patt_text, text)) if tag.string and isinstance(tag.next_sibling, NavigableString)]
        for tag in list(excess):
            target_text = ''
            target_text = tag.string[re.search(patt_text, tag.string).span()[0]+1:re.search(patt_text, tag.string).span()[1]-2]
            tag.string.replace_with(tag.text[:re.search(patt_text, tag.string).span()[0]])
            b_node = soup.new_tag('bold')
            b_node.string = target_text
            tag.insert_after('). ')
            tag.insert_after(b_node)
            tag.insert_after('(')


        patt_text_b = r'\s+\((\S+)\)'  # .在此种情况下只能是句号不可能是逗号
        excess_b = [tag for tag in soup.find_all('bold', text=lambda text: text is not None and re.search(patt_text_b, text)) if tag.string and isinstance(tag.next_sibling, NavigableString)]
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
                elif isinstance(i, Tag) and i.name == 'small':
                    string = re.sub(r'\s+', ' ', i.text) + string
                elif isinstance(i, Tag) and i.name == 'italic':
                    string = re.sub(r'\s+', ' ', i.text) + string
                elif isinstance(i, Tag) and i.name == 'bold':
                    string = re.sub(r'\s+', ' ', i.text) + string
                elif isinstance(i, Tag) and i.name == 'span':
                    string = re.sub(r'\s+', ' ', i.text) + string
                elif isinstance(i, Tag) and i.name == 'em':
                    string = re.sub(r'\s+', ' ', i.text) + string
                elif isinstance(i, Tag) and i.name == 'small-caps':
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
                b_node = soup.new_tag('bold')
                b_node.string = tag.string[re.search(patt_text_b, tag.string).start(1):re.search(patt_text_b, tag.string).end(1)]
                b_next_node = soup.new_tag('bold')
                b_next_node.string = tag.string[re.search(patt_text_b, tag.string).end(1):]
                tag.string.replace_with(tag.string[:re.search(patt_text_b, tag.string).start(1)])
                tag.insert_after(b_next_node)
                tag.insert_after(b_node)
                # print(tag.string)
                # print(tag.next_sibling)
                # print(tag.next_sibling.next_sibling)

        patt_text_single_b = r'\((\S+)\)'  # .在此种情况下只能是句号不可能是逗号
        excess_single_b = [tag for tag in soup.find_all('bold', text=lambda text: text is not None and re.search(patt_text_single_b, text)) if tag.string and tag.next_sibling is None]
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
                elif isinstance(i, Tag) and i.name == 'small':
                    string = re.sub(r'\s+', ' ', i.text) + string
                elif isinstance(i, Tag) and i.name == 'italic':
                    string = re.sub(r'\s+', ' ', i.text) + string
                elif isinstance(i, Tag) and i.name == 'bold':
                    string = re.sub(r'\s+', ' ', i.text) + string
                elif isinstance(i, Tag) and i.name == 'span':
                    string = re.sub(r'\s+', ' ', i.text) + string
                elif isinstance(i, Tag) and i.name == 'em':
                    string = re.sub(r'\s+', ' ', i.text) + string
                elif isinstance(i, Tag) and i.name == 'small-caps':
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
                elif isinstance(i, Tag) and i.name == 'small':
                    string = re.sub(r'\s+', ' ', i.text) + string
                elif isinstance(i, Tag) and i.name == 'italic':
                    string = re.sub(r'\s+', ' ', i.text) + string
                elif isinstance(i, Tag) and i.name == 'bold':
                    string = re.sub(r'\s+', ' ', i.text) + string
                elif isinstance(i, Tag) and i.name == 'span':
                    string = re.sub(r'\s+', ' ', i.text) + string
                elif isinstance(i, Tag) and i.name == 'em':
                    string = re.sub(r'\s+', ' ', i.text) + string
                elif isinstance(i, Tag) and i.name == 'small-caps':
                    string = re.sub(r'\s+', ' ', i.text) + string
                else:
                    break
            string = string + tag.string[0:re.search(patt5, tag.string).start(0)]
            index1 = string.rfind(' ')
            if index1 > -1:
                wd = string[index1:]
            for pre_next in (list(tag.next_siblings)):
                if isinstance(pre_next, NavigableString):
                    next_string = next_string + re.sub(r'\s+[∙·⋅]\s+', '·', re.sub(r'\s+', ' ', pre_next.string))  # 不能用+=,因为存入字符串的顺序要使得线存入的字符串压入最末尾
                elif isinstance(pre_next, Tag) and pre_next.name == 'sub':
                    next_string = next_string + re.sub(r'\s+[∙·⋅]\s+', '·', re.sub(r'\s+', ' ', pre_next.text))
                elif isinstance(pre_next, Tag) and pre_next.name == 'sup':
                    next_string = next_string + re.sub(r'\s+[∙·⋅]\s+', '·', re.sub(r'\s+', ' ', pre_next.text))
                elif isinstance(pre_next, Tag) and pre_next.name == 'small':
                    next_string = next_string + re.sub(r'\s+[∙·⋅]\s+', '·', re.sub(r'\s+', ' ', pre_next.text))
                elif isinstance(pre_next, Tag) and pre_next.name == 'italic':
                    next_string = next_string + re.sub(r'\s+[∙·⋅]\s+', '·', re.sub(r'\s+', ' ', pre_next.text))
                elif isinstance(pre_next, Tag) and pre_next.name == 'bold':
                    next_string = next_string + re.sub(r'\s+[∙·⋅]\s+', '·', re.sub(r'\s+', ' ', pre_next.text))
                elif isinstance(pre_next, Tag) and pre_next.name == 'span':
                    next_string = next_string + re.sub(r'\s+[∙·⋅]\s+', '·', re.sub(r'\s+', ' ', pre_next.text))
                elif isinstance(pre_next, Tag) and pre_next.name == 'small-caps':
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

        pronoun_tags = [tag for tag in list(soup.find_all('bold')) if isinstance(tag.parent, Tag)]
        for tag in pronoun_tags:
            if tag.parent.name == 'sup' or tag.parent.name == 'sub':
                if isinstance(tag.parent.previous_sibling, Tag):
                    if tag.parent.previous_sibling.name == 'bold':
                        if tag.parent.previous_sibling.text[-1] != ' ':
                            new_tag = tag.parent
                            tag.parent.previous_sibling.append(new_tag)
                            tag.parent.extract()

        pronoun_tag = [tag for tag in list(soup.find_all('italic')) if isinstance(tag.parent, Tag) and tag.parent.previous_sibling]
        for tag in pronoun_tag:
            if tag.parent.name == 'bold':
                if isinstance(tag.parent.previous_sibling, Tag):
                    if tag.parent.previous_sibling.name == 'bold':
                        if tag.parent.previous_sibling.text[-1] != ' ':
                            new_tag = tag          #同名标签的append插入有问题
                            tag.parent.previous_sibling.append(new_tag)
                            if isinstance(tag.parent.next_sibling, Tag):
                                tag.parent.next_sibling.extract()

        # 10.1039/c0nj00204f
        text2_tag = [tag for tag in soup.find_all('sub', text='1∞') if isinstance(tag.previous_sibling, NavigableString)]
        for tag in text2_tag:
            if tag.previous_sibling.string[-1] != ' ':
                tag.previous_sibling.string.replace_with(tag.previous_sibling.string + ' ')

        dct = {}
        compound_dct = {}
        b_tags = [tag for tag in list(soup.find_all('bold'))]    #[tag for tag in list(soup.select('.c-article-section__content b')) if tag.parent.name == 'p']
        b_tags = [tag for tag in b_tags if tag.text != '·']
        #print(len(b_tags))
        #print(len(set(b_tags)))
        for b_tag in b_tags:
            #是不是可以加一个判别式来判断b节点后面是否有能够分隔开的标志
            #正常情况，以及表格中p节点的情况  此段代码的功能是取出之前字符串的最后一个单词
            string = ''
            next_string = ''
            wd = ''
            #判别等号后的字符串
            seq_wd = ''
            key = ''
            text = ''
            if b_tag.text.find('–') >-1 or b_tag.text.find('-') >-1:
                continue
            if list(b_tag.previous_siblings):
                for pre_str in b_tag.previous_siblings:
                    if isinstance(pre_str, NavigableString):
                        string = re.sub(r'\s+[∙·⋅]\s+', '·',re.sub(r'\s+', ' ', pre_str.string)) + string      #不能用+=,因为存入字符串的顺序要使得新存入的字符串压入最末尾
                    elif isinstance(pre_str, Tag) and pre_str.name == 'sub':
                        string = re.sub(r'\s+[∙·⋅]\s+', '·', re.sub(r'\s+', ' ', pre_str.text)) + string
                    elif isinstance(pre_str, Tag) and pre_str.name == 'sup':
                        string = re.sub(r'\s+[∙·⋅]\s+', '·', re.sub(r'\s+', ' ', pre_str.text)) + string
                    elif isinstance(pre_str, Tag) and pre_str.name == 'small':
                        string = re.sub(r'\s+[∙·⋅]\s+', '·', re.sub(r'\s+', ' ', pre_str.text)) + string
                    elif isinstance(pre_str, Tag) and pre_str.name == 'italic':
                        string = re.sub(r'\s+[∙·⋅]\s+', '·', re.sub(r'\s+', ' ', pre_str.text)) + string
                    elif isinstance(pre_str, Tag) and pre_str.name == 'bold':
                        string = re.sub(r'\s+[∙·⋅]\s+', '·', re.sub(r'\s+', ' ', pre_str.text)) + string
                    elif isinstance(pre_str, Tag) and pre_str.name == 'span':
                        string = re.sub(r'\s+[∙·⋅]\s+', '·', re.sub(r'\s+', ' ', pre_str.text)) + string
                    elif isinstance(pre_str, Tag) and pre_str.name == 'em':
                        string = re.sub(r'\s+[∙·⋅]\s+', '·', re.sub(r'\s+', ' ', pre_str.text)) + string
                    elif isinstance(pre_str, Tag) and pre_str.name == 'small-caps':
                        string = re.sub(r'\s+[∙·⋅]\s+', '·', re.sub(r'\s+', ' ', pre_str.text)) + string
                    else:
                        break
                if string.find('\\') != -1:
                    print('出现异常字符')
                index1 = string.rfind(' ')
                index2 = string[:string.rfind(' ')].rfind(' ')
                if index1 > index2:
                    wd = string[index2+1:index1]
                elif index1==index2:
                    pass
                # print(b_tag.text)
                # print(string)
                # print(wd)

                if (re.match(pattern_element,wd) or re.match(pattern_element_charge,wd)) and re.findall(r'[\(\[][^\[\]\s]+\s*=\s*(?:[^\[\]\s]+\s)*{}'.format(wd), string):     #[^\[\s]替换\S   re.findall(r'\[[\w\(\),]+\s*=\s*(?:[\w\(\),]+\s*)*{}'.format(wd), string
                    # print(b_tag.text)
                    # print(string)
                    # print(wd)
                    # print(re.findall(r'\[[^\[\]\s]+\s*=\s*(?:[^\[\s]+\s*)*{}'.format(wd), string))
                    # print(re.findall(r'\[[^\[\]\s]+\s*=\s*(?:[^\[\s]+\s*)*{}'.format(wd), string)[-1] + string[string.rfind(' '):])
                    if len(string) == string.find(re.findall(r'[\(\[][^\[\]\s]+\s*=\s*(?:[^\[\s]+\s)*{}'.format(wd), string)[-1]) + len(re.findall(r'[\(\[][^\[\]\s]+\s*=\s*(?:[^\[\s]+\s*)*{}'.format(wd), string)[-1] + string[string.rfind(' '):]):
                        # print(b_tag.text)
                        # print(string)
                        # print(wd)
                        if re.match(pattern_element_charge, wd):
                            wd = wd.replace(',','')
                        # print(len(string))
                        # print(string.find(re.findall(r'[\(\[][^\[\]\s]+\s*=\s*(?:[^\[\s]+\s)*{}'.format(wd), string)[-1]))
                        # print(string[:string.find(re.findall(r'[\(\[][^\[\]\s]+\s*=\s*(?:[^\[\s]+\s)*{}'.format(wd), string)[-1])])
                        new_string = string[:string.find(re.findall(r'[\(\[][^\[\]\s]+\s*=\s*(?:[^\[\s]+\s)*{}'.format(wd), string)[-1])]
                        text = string[string.find(re.findall(r'[\(\[][^\[\]\s]+\s*=\s*(?:[^\[\s]+\s)*{}'.format(wd), string)[-1])+1:]
                        #print(repr(new_string))
                        index1 = new_string.rfind(' ')
                        index2 = new_string[:new_string.rfind(' ')].rfind(' ')
                        #match = re.findall(r'\[([^\[\]\s]+)\s*=\s*(?:[^\[\s]+\s*)*({})'.format(wd), string)[-1]
                        match = list(re.findall(r'[\(\[](?:[^\[\s]+\s)*([^\[\]\(\s]+|[^\[\]\s]+I+\))\s*=\s*(?:[^\[\s]+\s)*({})'.format(wd), string)[-1])
                        # print(text)
                        # print(match)
                        # print(match[0])
                        # print(match[1])
                        #10.1039/b820935a  [M(II) = Mn
                        if re.search(r'[^\[\]\s]+I+\)',match[0]):
                            match[0] = re.sub(r'\(I+\)','',match[0])
                        if index1 > index2:
                            wd = new_string[index2 + 1:index1]
                            wd = wd.replace(match[0], match[1])
                        elif index1 == index2:
                            pass
                        if wd.find('compound') > -1 or wd.find('complex') > -1:
                            new_string = new_string[:string.rfind(' ')].replace(wd, '')
                            index1 = new_string.rfind(' ')
                            index2 = new_string[:new_string.rfind(' ')].rfind(' ')
                            if index1 > index2:
                                wd = new_string[index2 + 1:index1]
                            elif index1 == index2:
                                wd = ''
                        #print(wd)

                #10.1039/c0dt00864h
                if re.match(pattern_element,wd) and re.search(r'(with )[^\[\]\s]+\s*=\s*(?:[^\[\]\s]+\s*)*{}'.format(wd), string):
                    #print(b_tag.text)
                    # print(re.search(r'(with )[^\[\]\s]+\s*=\s*(?:[^\[\]\s]+\s*)*{}'.format(wd), string))
                    #print(string)
                    match = re.findall(r'(?:[^\[\s]+\s*)*([^\[\]\s]+)\s*=\s*(?:[^\[\s]+\s*)*({})'.format(wd), string)[-1]
                    if match:
                        #print(match)
                        new_string = string[:string.find(re.search(r'(with )[^\[\]\s]+\s*=\s*(?:[^\[\]\s]+\s*)*{}'.format(wd), string).group())]
                        index1 = new_string.rfind(' ')
                        index2 = new_string[:new_string.rfind(' ')].rfind(' ')
                        if index1 > index2:
                            wd = new_string[index2 + 1:index1]
                            wd = wd.replace(match[0], match[1])
                        elif index1 == index2:
                            pass
                        if wd.find('compound') > -1 or wd.find('complex') > -1:
                            new_string = new_string[:string.rfind(' ')].replace(wd, '')
                            index1 = new_string.rfind(' ')
                            index2 = new_string[:new_string.rfind(' ')].rfind(' ')
                            if index1 > index2:
                                wd = new_string[index2 + 1:index1]
                            elif index1 == index2:
                                wd = ''
                        #print(wd)

                #10.1039/C6CE02476A   化学式 compound 1    10.1016/j.cclet.2015.12.034  5-(2,6-Bis(4-carboxyphenyl)pyridin-4-yl)isophthalic acid (
                if wd.find('compound') >-1 or wd.find('complex') > -1 or wd.find('acid') > -1:
                    string = string[:string.rfind(' ')].replace(wd,'')
                    index1 = string.rfind(' ')
                    index2 = string[:string.rfind(' ')].rfind(' ')
                    if index1 > index2:
                        wd = string[index2 + 1:index1]
                    elif index1 == index2:
                        wd = ''
                # 10.1039/b107369a   化学式 structure 2,
                if wd.find('structure') > -1:
                    string = string[:string.rfind(' ')].replace(wd, '')
                    index1 = string.rfind(' ')
                    index2 = string[:string.rfind(' ')].rfind(' ')
                    if index1 > index2:
                        wd = string[index2 + 1:index1]
                    elif index1 == index2:
                        wd = ''

            if b_tag.next_siblings and not re.search(pattern_item, wd):
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
                    elif isinstance(pre_next, Tag) and pre_next.name == 'italic':
                        next_string = next_string + re.sub(r'\s+[∙·⋅]\s+', '·',re.sub(r'\s+', ' ', pre_next.text))
                    elif isinstance(pre_next, Tag) and pre_next.name == 'bold':
                        next_string = next_string + re.sub(r'\s+[∙·⋅]\s+', '·',re.sub(r'\s+', ' ', pre_next.text))
                    elif isinstance(pre_next, Tag) and pre_next.name == 'span':
                        next_string = next_string + re.sub(r'\s+[∙·⋅]\s+', '·', re.sub(r'\s+', ' ', pre_next.text))
                    elif isinstance(pre_next, Tag) and pre_next.name == 'em':
                        next_string = next_string + re.sub(r'\s+[∙·⋅]\s+', '·', re.sub(r'\s+', ' ', pre_next.text))
                    elif isinstance(pre_next, Tag) and pre_next.name == 'small-caps':
                        next_string = next_string + re.sub(r'\s+[∙·⋅]\s+', '·', re.sub(r'\s+', ' ', pre_next.text))
                    else:
                        break

                if -1 < next_string.find(' = ') < 2 :
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
                    #10.1039/C9DT03511G   But unlike 1[BF4], 1[IMP-DMA] and 1[IMP-pipA]  可能把同级别的命名当作wd
                    if b_tag.text.find(']')>-1:
                        continue
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
                        #10.1039/c0nj00217h  Synthesis of 3: H2SDC   10.1039/C9DT03511G ; 2-(3,5-bis(trifluoromethyl)phenyl)-1H-imidazole
                        if next_string.find(':') == 0 or next_string.find(';') == 0 :
                            continue
                        if next_string.count(' ')>=2:
                            seq_wd = next_string[2:next_string[2:].find(' ') + 2]
                        elif next_string.count(' ') == 1 and next_string[-1] == '.' and next_string.find('.') == len(next_string)-1:
                            seq_wd = next_string[2:]
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
                            # 10.1039/C6DT00414H  排比介绍一些材料 且这些代码的指代词都可以被识别为wd
                            if next_string[len(wd)+2] == ',' and next_string.find(',') == 0 and next_string[len(wd)+1] != ')':
                                continue
                # print(next_string)
                # print(b_tag.text)
                #print(b_tag.previous_sibling)
                #print(string)
                # print(seq_wd)
                # print(wd)


            #创建以及更新,字典的更新以及文本冗余的指代词的删除,同时进行
            if (re.search(pattern_item,wd) or (re.search(pattern_metal,wd) and len(re.findall(pattern_1, wd))>0)) and ' ' not in b_tag.text:  #and ']' not in b_tag.text and '[' not in b_tag.text
                # print(b_tag.text)
                # print(wd)
                # print(string)
                # print(next_string)
                # print(b_tag.parent.text)
                # print(b_tag.parent.prettify())
                #10.1016/j.ica.2015.07.016
                if wd.find('⋯')>-1:
                    continue
                if wd.count('[') != wd.count(']') or wd.count('{') != wd.count('}'):
                    continue
                #10.1016/j.micromeso.2010.12.016
                if string[string.rfind(' ') + 1:] and string[-1] != ' ':
                    #10.1039/b315291j
                    # print(string)
                    if dct:
                        if b_tag.text in dct:
                            if wd.find(dct[b_tag.text])>-1:
                                continue
                    # print(string[string.rfind(' ')+1:])
                    # print(string[string.rfind(' ')+2:])
                    if (string[string.rfind(' ')+1:] and wd.find(string[string.rfind(' ')+1:])==-1 and string[-1] != '(') or (string[string.rfind(' ')+2:] and wd.find(string[string.rfind(' ')+2:])==-1 and string[-1] != '(') :
                        continue
                    if wd.find(string[string.rfind(' ')+1:])==0:
                        wd = wd.replace(string[string.rfind(' ') + 1:], '',1)
                    elif wd.find(string[string.rfind(' ')+2:])==0:
                        wd = wd.replace(string[string.rfind(' ') + 2:], '',1)
                    if not wd:
                        continue
                #10.1039/b315291j
                after_string = ''
                if list(b_tag.next_siblings):
                    for pre_next in (list(b_tag.next_siblings)):
                        if isinstance(pre_next, NavigableString):
                            after_string = after_string + re.sub(r'\s+[∙·⋅]\s+', '·', re.sub(r'\s+', ' ',pre_next.string))  # 不能用+=,因为存入字符串的顺序要使得线存入的字符串压入最末尾
                        elif isinstance(pre_next, Tag) and pre_next.name == 'sub':
                            after_string = after_string + re.sub(r'\s+[∙·⋅]\s+', '·', re.sub(r'\s+', ' ', pre_next.text))
                        elif isinstance(pre_next, Tag) and pre_next.name == 'sup':
                            after_string = after_string + re.sub(r'\s+[∙·⋅]\s+', '·', re.sub(r'\s+', ' ', pre_next.text))
                        elif isinstance(pre_next, Tag) and pre_next.name == 'small':
                            after_string = after_string + re.sub(r'\s+[∙·⋅]\s+', '·', re.sub(r'\s+', ' ', pre_next.text))
                        elif isinstance(pre_next, Tag) and pre_next.name == 'i':
                            after_string = after_string + re.sub(r'\s+[∙·⋅]\s+', '·', re.sub(r'\s+', ' ', pre_next.text))
                        # elif isinstance(pre_next, Tag) and pre_next.name == 'strong':
                        #     after_string = after_string + re.sub(r'\s+[∙·⋅]\s+', '·', re.sub(r'\s+', ' ', pre_next.text))
                        elif isinstance(pre_next, Tag) and pre_next.name == 'span' and ('class' in pre_next.attrs):
                            if pre_next['class'][0] == 'c-stack' or pre_next['class'][0] == 'italic' or pre_next['class'][0] == 'small_caps':
                                after_string = after_string + re.sub(r'\s+[∙·⋅]\s+', '·',re.sub(r'\s+', ' ', pre_next.text))
                        else:
                            break
                    if after_string:
                        #print(after_string[:after_string.find(' ')])
                        if after_string[0] != ' ' and after_string[:after_string.find(' ')]:
                            after_wd = after_string[:after_string.find(' ')]
                            if wd.find(after_string[:after_string.find(' ')]) == len(wd) - len(after_string[:after_string.find(' ')]):
                                wd = wd.replace(after_string[:after_string.find(' ')],'')
                            elif after_string.find(' ') > 1 and wd.find(after_string[:after_string.find(' ') - 1]) == len(wd) - len(after_string[:after_string.find(' ')-1]):
                                wd = wd.replace(after_string[:after_string.find(' ') - 1], '')
                            elif after_string.find(' ') > 2 and wd.find(after_string[:after_string.find(' ') - 2]) == len(wd) - len(after_string[:after_string.find(' ')-2]) :
                                wd = wd.replace(after_string[:after_string.find(' ') - 2], '')
                    if not wd:
                        continue

                #10.1134/S0036023619090195   ((Ph4SbOC(O)C6H4(OH-3)
                if wd[-1] == ';' or wd[-1] == '.' or wd[-1] == ',' or wd[-1] == ':':
                    wd = wd[:len(wd) - 1]
                if wd.count('(') != wd.count(')'):
                    wd1 = wd
                    wd = wd.strip(')').strip('(')
                    if wd.count('(') == wd.count(')') + 1:
                        wd = wd +')'
                    elif wd.count('(') + 1 == wd.count(')'):
                        wd = '(' + wd
                    if wd.count('(') != wd.count(')'):
                        wd = wd1
                #10.1039/C4CY00125G  10.1039/b103107b
                if wd[-1] == ',' and string.rfind(' ') < len(string)-3:
                    continue
                if wd.count(']') == wd.count('[') == 1 and wd[0] == '[' and wd[-1] == ']':
                    wd = wd[1:len(wd) - 1]
                if wd.count(')') == wd.count('(') == 1 and wd[0] == '(' and wd[-1] == ')':
                    wd = wd[1:len(wd) - 1]
                # 10.1016/j.ica.2017.08.062
                # if re.search(pattern_item,b_tag.text) and not re.search(r'\d·\S+',b_tag.text):
                #     continue
                if wd.find('—')>-1 or wd.find('/')>-1 or wd.find(' ')>-1 or re.search(r'\w\.[A-Za-z]+',wd) or (wd.count('{') != wd.count ('}')) or (wd.count('(') != wd.count (')')) or re.search(patt_math_formula,wd):   #中文版的长破折号  #10.1039/b901404g .句号
                    continue
                #print(b_tag.text and (b_tag.text[-1] == ')' or b_tag.text[0] == '(' or b_tag.text.find('−')>-1))
                if b_tag.text in dct:
                    if len(wd)>=len(dct[b_tag.text]):                                         #and b_tag.text.find('.')!=-1              '[Pr(H2salen)1.5(NO3)3]n'与'[Pr(H2salen)1.5(NO3)3]'
                        if wd == next_string[1:next_string[1:].find(' ')+1]:
                            continue
                        #C19H20CoCuN4O10与[LCuCo(NO3)2]   10.1039/c0nj00238k,只在覆盖的情况下处理
                        if re.search(r'\(\S+\)',wd) is None and re.search(r'\(\S+\)',dct[b_tag.text]):
                            continue
                        dct[b_tag.text] = wd
                        b_tag.extract()
                    else:
                        #10.1016/j.poly.2007.08.011
                        if dct[b_tag.text].find('[' + wd + ']') == 0 and len(wd)+3>=len(dct[b_tag.text]):
                            dct[b_tag.text] = wd
                        pass
                else:
                    # print(b_tag.text)
                    # print(b_tag.next_sibling)
                    if (b_tag.text.count(')') != b_tag.text.count ('(')  or b_tag.text.find('−')>-1) or (b_tag.text.count('(') != b_tag.text.count(')')) or (b_tag.text.count('{') != b_tag.text.count('}')):
                        continue
                    dct[b_tag.text] = wd
                    b_tag.extract()                  #之后剩余即是无化学式前文的b标签节点
            if re.search(patt_compounds,wd):
                # print(b_tag.text)
                # print(wd)
                key = b_tag.text
                if wd.find('—')>-1 or re.search(r'\d+\/\d+\-',wd) or re.search(r'\-connected',wd):    #特例 1/2-spins  4-connected #10.1039/C5CC08941G
                    continue
                if wd[-1] == ';' or wd[-1] == ':' or wd[-1] == '.' or wd[-1] == ',':
                    wd = wd[:len(wd) - 1]
                if wd.find(':')>-1:
                    wd = wd[wd.find(':')+1:]
                #c5ce01454a 10.1039/C5CE02174J   μ8-bridging和4-connnected
                if wd.count('-') == 1:
                    word = wd[wd.find('-')+1:]
                    if is_english_word(word):
                        continue
                text = wd
                if key in compound_dct:
                    if text in compound_dct[key]:
                        pass
                    else:
                        compound_dct[key].append(text)
                else:
                    if not key or key.find(' ') >-1 or (text.count(')') != text.count ('(')) or (text.count('{') != text.count ('}')) or (text.count('[') != text.count (']')):
                        continue
                    compound_dct[key] = [text]
        #print(len(dct))
        print(dct)
        #exit()
        #print(compound_dct)
        #print(list(dct.keys()))


        # 删除所有的table
        rtable_tags = soup.select('div .rtable__wrapper')       #属性不一定要全部取得，尤其是中间有空格
        for m in range(len(rtable_tags)):
            rtable_tags[m].extract()
        table_container = soup.select('div .table')
        for h in range(len(table_container)):
            table_container[h].extract()

        #若是字典中出现两个相同的值，保留后一个键值对
        keys,values = list(dct.keys()),list(dct.values())
        repeat_values = []
        for value in values:
            if values.count(value)>1 and value not in repeat_values:
                repeat_values.append(value)
        for v in repeat_values:
            key = keys[values.index(v)]
            del dct[key]

        for key in list(dct.keys()):
            if key.find('(') > -1 or key.find('[') > -1:
                continue
            pattern = r'(\s+){}$'.format(key)
            tags = [tag for tag in list(soup.find_all('bold',text = lambda text: text is not None and re.match(pattern,text))) if tag.string]
            for tag in tags:
                print('测试')
                tag.string.replace_with(key)

        brackets2 = [f"({x}" for x in list(dct.keys())]
        brackets1 = [f"{x})" for x in list(dct.keys())]
        #print(adds)
        #print(len(dashs))
        #处理括号，应该在，-符号之前，因为这些符号在括号内部
        b_strong_tags = [tag for tag in list(soup.find_all('bold') + soup.find_all('bold')) if tag.parent.name == 'para']
        for tag in b_strong_tags:
            for brac in brackets1:
                if tag.text.endswith(brac) and tag.string:
                    tag.insert_after(')')
                    tag.string.replace_with(tag.string[:len(tag.string)-1])

        b_strong_tags = [tag for tag in list(soup.find_all('bold') + soup.find_all('bold')) if tag.parent.name == 'para']
        for tag in b_strong_tags:
            for brac in brackets2:
                if tag.text.find(brac) == 0 and tag.string:
                    tag.insert_before('(')
                    tag.string.replace_with(tag.string[1:])

        b_strong_tags = [tag for tag in list(soup.find_all('bold') + soup.find_all('bold')) if tag.parent.name == 'para']
        combinations = [f"{x}, {y}" for x in list(dct.keys()) for y in list(dct.keys()) if x != y]
        dashs = [f"{x}-{y}" for x in list(dct.keys()) for y in list(dct.keys()) if x != y]
        adds = [f"{x}," for x in list(dct.keys())] + [f"{x}." for x in list(dct.keys())]
        for tag in b_strong_tags:
            for opt in combinations:
                str_copy = tag.text
                if tag.text.find(opt)>-1 and tag.string and len(tag.text)>=len(opt):                                    #tag.string而不是tag.text是为了使b节点内只有一个子节点
                    if tag.text.find(opt) == 0:
                        tag.string.replace_with(str_copy[:str_copy.find(', ')])
                        b_node = soup.new_tag('bold')
                        b_node.string = opt[opt.find(', ')+2:]
                        tag.insert_after(b_node)
                        tag.insert_after(', ')
                    else:
                        tag.string.replace_with(str_copy[:str_copy.find(opt)])
                        b_node1 = soup.new_tag('bold')
                        b_node1.string = opt[:opt.find(',')]
                        b_node2 = soup.new_tag('bold')
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
                    b_node = soup.new_tag('bold')
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

        #10.1039/c0dt01137a 在合成段落中未出现应有的化学结构
        if len(dct) == 1:
            key = list(dct.keys())[0]
            value = list(dct.values())[0]
            h3_span_proun = [tag for tag in soup.find_all('h3') if isinstance(tag.next_sibling,Tag) and len(tag.contents) == 1]
            for tag in h3_span_proun:
                if tag.next_sibling.name == 'para' and not tag.find_all('bold',text = key) and not tag.next_sibling.find_all('bold',text = key):
                    if re.search(r'[Ss]ynthesis',tag.text) and re.search(r'MOF' + '|' + r'[Cc]ompound',tag.text):
                        print(tag.text)
                        if isinstance(tag.contents[0],NavigableString):
                            tag.contents[0].string.replace_with(tag.text + ' ' + value)
                        elif isinstance(tag.contents[0],Tag):
                            tag.contents[0].string = tag.text + ' ' + value

        # 将各处包含-转为，
        for key in list(dct.keys()):
            b_strong_tags = soup.find_all('bold', string=key) + soup.find_all('bold', string=key)
            b_strong_tags = [tag for tag in b_strong_tags if tag.parent.name == 'para']
            # print(len(b_strong_tags))
            for b_strong in b_strong_tags:
                if isinstance(b_strong.next_sibling, NavigableString):
                    if b_strong.next_sibling.string == '–' or b_strong.next_sibling.string == '-':
                        b_strong.next_sibling.extract()
                        if isinstance(b_strong.next_sibling, Tag) and b_strong.next_sibling.name == 'bold' and b_strong.next_sibling.text in list(dct.keys()):
                            if b_strong.text.isdigit() and b_strong.next_sibling.text.isdigit():
                                for dig in reversed(range(int(b_strong.text) + 1, int(b_strong.next_sibling.text))):
                                    b_strong.insert_after(', ')
                                    new_b_tag = soup.new_tag('bold')  # 创建新的<b>标签节点
                                    new_b_tag.string = str(dig)  # 设置<b>标签节点的文本内容
                                    b_strong.insert_after(new_b_tag)
                                b_strong.insert_after(', ')
                            elif list(dct.keys()).index(b_strong.text)>-1 and list(dct.keys()).index(b_strong.next_sibling.text)>-1:
                                for i in range(list(dct.keys()).index(b_strong.text) + 1,list(dct.keys()).index(b_strong.next_sibling.text)):
                                    b_strong.insert_after(', ')
                                    new_b_tag = soup.new_tag('bold')  # 创建新的<b>标签节点
                                    new_b_tag.string = str(dct[list(dct.keys())[i]])  # 设置<b>标签节点的文本内容
                                    b_strong.insert_after(new_b_tag)
                                b_strong.insert_after(', ')
                        elif isinstance(b_strong.next_sibling, Tag) and b_strong.next_sibling.name == 'bold':
                            if b_strong.next_sibling.text in list(dct.keys()):
                                if b_strong.text.isdigit() and b_strong.next_sibling.text.isdigit():
                                    for dig in reversed(range(int(b_strong.text) + 1, int(b_strong.next_sibling.text))):
                                        b_strong.insert_after(', ')
                                        new_b_tag = soup.new_tag('bold')  # 创建新的<b>标签节点
                                        new_b_tag.string = str(dig)  # 设置<b>标签节点的文本内容
                                        b_strong.insert_after(new_b_tag)
                                    b_strong.insert_after(', ')
                                elif list(dct.keys()).index(b_strong.text)>-1 and list(dct.keys()).index(b_strong.next_sibling.text)>-1:
                                    for i in range(list(dct.keys()).index(b_strong.text)+1,list(dct.keys()).index(b_strong.next_sibling.text)):
                                        b_strong.insert_after(', ')
                                        new_b_tag = soup.new_tag('bold')  # 创建新的<b>标签节点
                                        new_b_tag.string = str(dct[list(dct.keys())[i]])  # 设置<b>标签节点的文本内容
                                        b_strong.insert_after(new_b_tag)
                                    b_strong.insert_after(', ')

        # 10.1039/c0dt01718c  '1': '[HB(mt)2(pz3,5-Me)]−',
        for key in list(dct.keys()):
            # print(dct[key])
            if dct[key][-1] == '−':
                dct[key] = dct[key][:-1]
            # 10.1016/j.molstruc.2018.05.097
            if re.search(r'\(\d+\)', key):
                new_key = re.sub(r'\((\d+)\)', r'\1', key)
                dct[new_key] = dct[key]

        #将各处的指示代词替换为原形
        for key in list(dct.keys()):
            b_strong_tags = [tag for tag in soup.find_all('bold') + soup.find_all('b') if tag.text == key] + soup.find_all('bold',text= key)
            b_tags = [tag for tag in b_strong_tags if tag.parent.name == 'para' or tag.parent.name == 'section-title']
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
                    elif isinstance(pre, Tag) and pre.name == 'italic':
                        string = re.sub(r'\s+', ' ', pre.text) + string
                    elif isinstance(pre, Tag) and pre.name == 'bold':
                        string = re.sub(r'\s+', ' ', pre.text) + string
                    elif isinstance(pre, Tag) and pre.name == 'span':
                        string = re.sub(r'\s+', ' ', pre.text) + string
                    elif isinstance(pre, Tag) and pre.name == 'em':
                        string = re.sub(r'\s+', ' ', pre.text) + string
                    elif isinstance(pre, Tag) and pre.name == 'small-caps':
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
                if wd != dct[key] and wd != '[' +dct[key] + ']' and wd != '(' + dct[key] + ')':
                    if b_tags[i].string is None:
                        new_b_tag = soup.new_tag('bold')
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
        compounud_tags = [tag for tag in soup.find_all(text=lambda text: text is not None and re.search(patt_equ, text)) if tag.parent.name == 'para']
        for tag in compounud_tags:
            text=''
            pre_string = tag.string
            for pre_str in tag.previous_siblings:
                if isinstance(pre_str, NavigableString):
                    if pre_str.string.find(']') > -1:
                        pre_string = re.sub(r'\s+', ' ', pre_str.string) + pre_string
                        break
                    pre_string = re.sub(r'\s+[∙·⋅]\s+', '·',re.sub(r'\s+', ' ', pre_str.string)) + pre_string  # 不能用+=,因为存入字符串的顺序要使得新存入的字符串压入最末尾
                elif isinstance(pre_str, Tag) and pre_str.name == 'sub':
                    if pre_str.text.find(']') > -1:
                        pre_string = re.sub(r'\s+', ' ', pre_str.text) + pre_string
                        break
                    pre_string = re.sub(r'\s+[∙·⋅]\s+', '·', re.sub(r'\s+', ' ', pre_str.text)) + pre_string
                elif isinstance(pre_str, Tag) and pre_str.name == 'sup':
                    if pre_str.text.find(']') > -1:
                        pre_string = re.sub(r'\s+', ' ', pre_str.text) + pre_string
                        break
                    pre_string = re.sub(r'\s+[∙·⋅]\s+', '·', re.sub(r'\s+', ' ', pre_str.text)) + pre_string
                elif isinstance(pre_str, Tag) and pre_str.name == 'italic':
                    if pre_str.text.find(']') > -1:
                        pre_string = re.sub(r'\s+', ' ', pre_str.text) + pre_string
                        break
                    pre_string = re.sub(r'\s+[∙·⋅]\s+', '·', re.sub(r'\s+', ' ', pre_str.text)) + pre_string
                elif isinstance(pre_str, Tag) and pre_str.name == 'bold':
                    if pre_str.text.find(']') > -1:
                        pre_string = re.sub(r'\s+', ' ', pre_str.text) + pre_string
                        break
                    pre_string = re.sub(r'\s+[∙·⋅]\s+', '·', re.sub(r'\s+', ' ', pre_str.text)) + pre_string
                elif isinstance(pre_str, Tag) and pre_str.name == 'span':
                    if pre_str.text.find(']') > -1:
                        pre_string = re.sub(r'\s+', ' ', pre_str.text) + pre_string
                        break
                    pre_string = re.sub(r'\s+[∙·⋅]\s+', '·', re.sub(r'\s+', ' ', pre_str.text)) + pre_string
                elif isinstance(pre_str, Tag) and pre_str.name == 'em':
                    if pre_str.text.find(']') > -1:
                        pre_string = re.sub(r'\s+', ' ', pre_str.text) + pre_string
                        break
                    pre_string = re.sub(r'\s+[∙·⋅]\s+', '·', re.sub(r'\s+', ' ', pre_str.text)) + pre_string
                elif isinstance(pre_str, Tag) and pre_str.name == 'small-caps':
                    if pre_str.text.find(']') > -1:
                        pre_string = re.sub(r'\s+', ' ', pre_str.text) + pre_string
                        break
                    pre_string = re.sub(r'\s+[∙·⋅]\s+', '·', re.sub(r'\s+', ' ', pre_str.text)) + pre_string
                else:
                    break
            for pre_str in tag.next_siblings:
                if isinstance(pre_str, NavigableString):
                    if pre_str.string.find(' ') > -1:
                        pre_string = pre_string + re.sub(r'\s+', ' ', pre_str.string)
                        break
                    pre_string = pre_string + re.sub(r'\s+[∙·⋅]\s+', '·', re.sub(r'\s+', ' ',pre_str.string))  # 不能用+=,因为存入字符串的顺序要使得新存入的字符串压入最末尾
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
                elif isinstance(pre_str, Tag) and pre_str.name == 'italic':
                    if pre_str.text.find(' ') > -1:
                        pre_string = pre_string + re.sub(r'\s+', ' ', pre_str.text)
                        break
                    pre_string = pre_string + re.sub(r'\s+[∙·⋅]\s+', '·', re.sub(r'\s+', ' ', pre_str.text))
                elif isinstance(pre_str, Tag) and pre_str.name == 'bold':
                    if pre_str.text.find(' ') > -1:
                        pre_string = pre_string + re.sub(r'\s+', ' ', pre_str.text)
                        break
                    pre_string = pre_string + re.sub(r'\s+[∙·⋅]\s+', '·', re.sub(r'\s+', ' ', pre_str.text))
                elif isinstance(pre_str, Tag) and pre_str.name == 'span':
                    if pre_str.text.find(' ') > -1:
                        pre_string = pre_string + re.sub(r'\s+', ' ', pre_str.text)
                        break
                    pre_string = pre_string + re.sub(r'\s+[∙·⋅]\s+', '·', re.sub(r'\s+', ' ', pre_str.text))
                elif isinstance(pre_str, Tag) and pre_str.name == 'small-caps':
                    if pre_str.text.find(' ') > -1:
                        pre_string = pre_string + re.sub(r'\s+', ' ', pre_str.text)
                        break
                    pre_string = pre_string + re.sub(r'\s+[∙·⋅]\s+', '·', re.sub(r'\s+', ' ', pre_str.text))
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
                    if string[0].split('(')[-1].split('[')[-1] and string[0].split('(')[-1].split('[')[-1].find('http') == -1 and string[1].find('/') == -1:
                        text = string[1]
                        key = string[0].split('(')[-1].split('[')[-1]
                        if key.rfind('{')>-1:
                            key = key[key.rfind('{')+1:]
                        if (key.count(')') != key.count('(')) or (key.count('[') != key.count(']')) or (key.count('{') != key.count('}')):
                            continue
                        if string[0].split('(')[-1].split('[')[-1].rfind('(')>-1:
                            key = key[key.rfind('(')+1:]
                        if text.count('[') != text.count(']') or text.count('{') != text.count('}') or text.count('(') != text.count(')'):
                            continue
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
        df.at[index, 'name_dicts'] = dct
        df.at[index, 'compound_dicts'] = compound_dct

        #exit()

        # with open(list_html[j], 'wb') as f:   #encoding='utf-8'
        #     f.write(str(soup).encode())

    print(len(df))
    if 'flags' in list(df.columns):
        df = df.drop(df[df['flags'] == 2].index, axis=0)
    df.to_csv('count_year_url_publiser_dict1016.csv', index=False)



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


if __name__ == '__main__':
    # df = pd.read_csv('count_year_url_publiser1016.csv', header=0)
    # list_flags = download_html(df)
    # df.insert(6, 'flags', list_flags)
    # df.to_csv('count_year_url_publiser1016.csv', index=False)
    #contact(df)
    #test_download('https://www.sciencedirect.com/science/article/pii/S0022328X07001969')
    #test_download('https://api.elsevier.com/content/article/pii/S0003267020310989')
    #parsing('flag_download.html')
    #orignaltext_batch_process()
    # df = pd.read_csv('Dataset.csv', header=0)
    # print(len(df))
    preprocess()
    exit()


# 新旧标签替换，加上root根节点
        # print(soup.find('originalText').prettify())
        # soup.find('originalText').replace_with(new_tag)
        # print(soup.prettify())
        #text = soup.prettify()
        #text = re.sub(u"[\x00-\x08\x0b-\x0c\x0e-\x1f]+", u"", soup.prettify())        #添加\：,就不报警告
        # text = text.replace('xmlns:="http://www.elsevier.com/xml/svapi/article/dtd" ','',1)
        # text = text.replace(' xmlns:="http://www.elsevier.com/xml/ja/dtd"', '', 1)
        # text = text.replace(' xmlns:="http://www.elsevier.com/xml/common/cals/dtd"', '', 1)
        # text = text.replace('xmlns:="http://www.elsevier.com/xml/common/dtd"', 'xmlns:ce="http://www.elsevier.com/xml/common/dtd"', 96)
        # print(text)
        # ns = {'ce':'http://www.elsevier.com/xml/ja/dtd'}
        #xml_full_text = response.text
        # print(xml_full_text)
        #root = et.fromstring(text)                    #xml模块解析xml格式字符串的时候, 无法调用getroot方法，问题原因是此处的fromstring直接返回的就是root,不是用parse解析本地文档
        # for tag in article_text:
        #     #print(tag.tag,tag.attrib)
        #     for c_tag in tag:
        #         print(c_tag.tag,c_tag.attrib)
        #print(soup.prettify())
        # print(root.tag)
        # for tag in root:
        #     #print(tag.tag,tag.attrib)
        #     for c_tag in tag:
        #         print(c_tag.tag,c_tag.attrib)
        # exit()
