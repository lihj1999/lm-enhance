from bs4 import BeautifulSoup
import pandas as pd
import requests
import csv
import time
from glob import glob
import csv
import unicodedata
import os
from glob import glob
import csv
import unicodedata
import regex as  re
from bs4.element import NavigableString,Tag,Script,ProcessingInstruction
import copy
import nltk
from nltk.corpus import wordnet
from pylatexenc.latex2text import LatexNodes2Text
import warnings
warnings.filterwarnings("ignore")


#选出2000年后的发表的文献
df = pd.read_csv('count_year_url_publiser1039.csv', header=0)
# df = df.loc[df['year'].astype(int)>2000]
# df.to_csv('count_year_url_publiser1039.csv', index=False)
# exit()
urls = list(df['url'])        #错的原因是列名叫’url ‘，多了一个空格
dois = list(df['doi'])
years = list(df['year'])

def get_resonse(url):
    header = {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36 Edg/112.0.1722.34',
              "Cookie":'ShowEUCookieLawBanner=true; Hm_lvt_d7c7037093938390bc160fc28becc542=1660705937; X-Mapping-hhmaobcf=7DDC481DC5026D33311E710FD9D30B13; _PubsBFCleared=1; ASP.NET_SessionId=n5ahicccr24s0hbhxbpbedyf; Branding=; AuthSystemSessionId=b6476847-e9ea-42b8-86dc-7fb7ec1a3fc1; ApplicationCheckAccessCookie=PD94bWwgdmVyc2lvbj0iMS4wIj8+DQo8Q2hlY2tBY2Nlc3MgeG1sbnM6eHNkPSJodHRwOi8vd3d3LnczLm9yZy8yMDAxL1hNTFNjaGVtYSIgeG1sbnM6eHNpPSJodHRwOi8vd3d3LnczLm9yZy8yMDAxL1hNTFNjaGVtYS1pbnN0YW5jZSI+DQogIDxEb2N1bWVudFR5cGU+QWxsPC9Eb2N1bWVudFR5cGU+DQogIDxKb3VybmFsQ29kZT5OSjwvSm91cm5hbENvZGU+DQogIDxZZWFyPjIwMDk8L1llYXI+DQogIDxET0k+YjluajAwMzE2YTwvRE9JPg0KICA8Vm9sdW1lPjMzPC9Wb2x1bWU+DQogIDxJc3N1ZUlEPjExPC9Jc3N1ZUlEPg0KICA8Q29udGVudFR5cGU+QXJ0aWNsZTwvQ29udGVudFR5cGU+DQogIDxQdWJsaWNhdGlvbkRhdGU+MjAwOS0wOS0yMlQwMDowMDowMDwvUHVibGljYXRpb25EYXRlPg0KICA8U2Vzc2lvbklEPmI2NDc2ODQ3LWU5ZWEtNDJiOC04NmRjLTdmYjdlYzFhM2ZjMTwvU2Vzc2lvbklEPg0KICA8SXNJUFJlY29nbmlzZWQ+ZmFsc2U8L0lzSVBSZWNvZ25pc2VkPg0KICA8VXNlckxvZ2dlZEluPmZhbHNlPC9Vc2VyTG9nZ2VkSW4+DQogIDxDdXN0b21UYWdzIC8+DQogIDxJc0F1dGhlbnRpY2F0ZWQ+ZmFsc2U8L0lzQXV0aGVudGljYXRlZD4NCiAgPElzTW9iaWxlQXBwPmZhbHNlPC9Jc01vYmlsZUFwcD4NCiAgPElzRG93bmxvYWQ+ZmFsc2U8L0lzRG93bmxvYWQ+DQogIDxQbGF0Zm9ybUlEPjFDNTc2OTYyLUI5OTQtNDEzOS1BMTg2LTgxMjA0MzNCRTdCNzwvUGxhdGZvcm1JRD4NCiAgPElzQ29udGVudEFjY2Vzc2libGU+ZmFsc2U8L0lzQ29udGVudEFjY2Vzc2libGU+DQo8L0NoZWNrQWNjZXNzPg==; EPLATFORMURL=https%3a%2f%2fpubs.rsc.org%2fen%2fcontent%2farticlelanding%2f2009%2fnj%2fb9nj00316a%2funauth|; Branding=50010439'}
    response = requests.get(url,headers=header)
    response.encoding = 'utf-8'
    return response


#文本用unicode编码，为str类型，二进制数据则为bytes类型;用二进制写入保存为html格式文件，python有两种类型转换的函数encode()——字符串型转为字节型,decode()
def savehtml(response,rename):
    with open(rename +'.html', 'wb') as f:
        f.write(response.text.encode())


def orignaltext_clean():
    df = pd.read_csv('count_year_url_publiser1039.csv', header=0)
    print(len(df))
    list_html = glob('./1039-process/*.html')
    print(len(list_html))

    #比较文件数量和重复问题
    # list_html1 = glob('./原始文档/*.html')
    # list1 = [i[9:].lower() for i in list_html]
    # print(len(set(list1)))
    # #print(list1)
    # list2 = [i[7:].lower() for i in list_html1]
    # print(len(set(list2)))
    # #print(list2)
    # print(set(list2).difference(set(list1)))
    # print(len(set(list2).difference(set(list1))))
    # print(set(list1).difference(set(list2)))
    # print(len(set(list1).difference(set(list2))))
    # exit()
    '''对每个文件名查询是否有三个'_'符号'''
    # print(len(list_html))
    # print([i.count('_') for i in list_html])

    dois = [list_html[i][list_html[i].find('_')+1:list_html[i].rfind('_')] for i in range(len(list_html))]
    dois = [dois[i].replace('_','/') for i in range(len(dois))]
    years = [list_html[i][list_html[i].rfind('_')+1:list_html[i].rfind('.')] for i in range(len(list_html))]

    with open('Dataset_rsc.csv', 'a', newline="", encoding='utf-8') as f:  # 写改为追加的方式；‘ab+’以二进制的形式写入
        writer = csv.writer(f)
        header = 'doi', 'year', 'count', 'number', 'paras', 'label'
        writer.writerow(header)

    for j in range(len(list_html)):  # len(list_html)
        print(dois[j])
        with open(list_html[j], 'r', encoding='utf-8') as f:   #list_html[j]
            soup = BeautifulSoup(f.read(), 'html.parser')
            #print(soup.prettify())

        span_italic_tags = [tag for tag in soup.find_all('span', class_='italic') if isinstance(tag.next_sibling, Tag)]
        for tag in span_italic_tags:
            if tag.next_sibling.name == 'span' and 'italic' in tag.next_sibling.get('class', []):
                tag.next_sibling.string = ' ' + tag.next_sibling.text

    #测试，判断有多少文献有div类似的结构，以及其他特殊情况
    #     for link in soup.find_all(["br", "hr"]):
    #         link.extract()
    #     for link in soup.find_all(text="\n"):
    #         link.extract()
    #     if soup.select('span.c_heading_indent'):
    #         doc += 1
    #         div_list = [tag.parent for tag in soup.select('span.c_heading_indent') if tag.parent.name == 'div']
    #         count = 0
    #         for div in div_list:
    #             print([child.name for child in div.contents])
    #             child_name_list = [child.name for child in div.contents]
    #             if child_name_list.count('span')>6:
    #                 abnormal_value += 1
    #             if 'p' not in child_name_list:
    #                 pass
    #             else:
    #                 count += 1
    #                 print(count)
    #     print('<<<<<<<<>>>>>>>>>>>')
    # print(doc)
    # print(abnormal_value)
    # exit()


        rename = 'DOI_10.1039_' + dois[j][dois[j].rfind('/') + 1:] + '_' + str(years[j])

        main_content = soup.select('div #wrapper')
        #print(len(main_content[0].contents))

        # 删除所有的图像节点
        figure_tags = soup.select('div .image_table')
        # print(len(figure_tags))
        for h in range(len(figure_tags)):
            figure_tags[h].extract()

        # 删除所有参考文献上标和脚注
        ref_tags = soup.select('a[title="Select to navigate to references"]') + soup.select('a[title="Select to navigate to reference"]') + soup.select('a[title="Select to navigate to footnote"]')  # 属性值   加了s代表多个，未加s表示一个
        # print(len(ref_tags))
        for k in range(len(ref_tags)):
            ref_tags[k].extract()

        # 删除所有的table节点 可能是公式之类的 （1）（2）（3）（4）...
        table = soup.select('table')
        for q in range(len(table)):
            table[q].extract()

        # 删除所有表格节点
        table_tags = soup.select('div .table_caption')
        rtable_tags = soup.select('div .rtable__wrapper')
        # print(len(table_tags))
        # print(len(rtable_tags))
        for m in range(len(table_tags)):
            table_tags[m].extract()
        for n in range(len(rtable_tags)):
            rtable_tags[n].extract()

        '''不是很准'''
        span_and_p = [index for index, value in enumerate(main_content[0].contents) if value.name == 'span' or value.name == 'p']
        #print(len(span_and_p))

        span = soup.select('span')
        p = soup.select('p')
        p_span = p + span
        #print(len(p_span))

        h2 = soup.select('h2')
        h3 = soup.select('h3')
        h4 = soup.select('h4')
        #print([h2[i].get_text() for i in range(len(h2))])

        for link in soup.find_all(["br", "hr"]):
            link.extract()
        for link in soup.find_all(text="\n"):
            link.extract()

        #删除什么abstract块之前的兄弟节点和Conflicts of interest和Acknowledgements块之后所有的兄弟节点   如果运行一次就不要在运行了
        abstract_tag = soup.select('div .abstract')
        if abstract_tag:
            for i in list(abstract_tag[0].previous_siblings):
                i.extract()
            abstract_tag[0].extract()
        for i in h2:
            if i.get_text().strip() == 'Conflicts of interest' or i.get_text().strip() == 'Acknowledgements' or i.get_text().strip() == 'Notes and references':
                if 0 < len(list(i.next_siblings)) < 10:
                    for tag in list(i.next_siblings):  # 加上list函数，打成一个循环体
                        tag.extract()
                    i.extract()  # 注意节点去除的顺序
                    break
                elif 0 < len(list(i.parent.next_siblings)) < 10:
                    for tag in list(i.parent.next_siblings):  # 加上list函数，打成一个循环体
                        tag.extract()
                    i.extract()  # 注意节点去除的顺序
                    break

        # 文字链接节点
        text_tag = soup.select('span.CH') + soup.select('span.TC') + soup.select('span.RTC') + soup.select('span.AN')
        for tag in text_tag:
            if isinstance(tag.previous_sibling, NavigableString):
                tag.previous_sibling.replace_with(tag.previous_sibling.string + tag.text)
                tag.extract()
            elif isinstance(tag.next_sibling, NavigableString):
                tag.next_sibling.replace_with(tag.next_sibling.string + tag.text)
                tag.extract()
            elif isinstance(tag.previous_sibling, Tag):
                tag.next_sibling.replace_with(tag.previous_sibling.text + tag.text)
                tag.extract()
            elif isinstance(tag.next_sibling, Tag):
                tag.next_sibling.replace_with(tag.next_sibling.text + tag.text)
                tag.extract()
            # 可以直接不处理这些极端情况；如有时将h3标题也当作文字链接节点
            # else:
            #     print('>>>>>>>文字链接节点有错误<<<<<<<')

        number, paras = 0, []
        for element in [tag for tag in soup.select('div #wrapper')[0].contents if tag.name == 'span' or tag.name == 'p']:
            if element.find_all('a'):
                # print([i.string for i in element.find_all('a')])
                # print(len([i.string for i in element.find_all('a')]))
                #print([tag.text.strip() for tag in element.find_all('a')])
                for child in element.find_all('a'):  # find_next_sibling和next_sibling，前一个只找寻tag节点
                    try:
                        if find_count(str(child.previous_sibling.string), '(') > find_count(str(child.previous_sibling.string), ')') and find_count(str(child.next_sibling.string),'(') < find_count(str(child.next_sibling.string), ')'):
                            child.previous_sibling.replace_with(str(child.previous_sibling.string)[:str(child.previous_sibling.string).rfind('(')])  # 本来想用节点替换的方式，结果发现tag中包含的字符串（即Navigablestring对象）不能编辑,但是可以被替换成其它的字符串
                            # print(str(child.next_sibling.string)[str(child.next_sibling.string).find(')')+1:])
                            child.next_sibling.replace_with(str(child.next_sibling.string)[str(child.next_sibling.string).find(')') + 1:])
                            child.extract()
                            continue

                        if find_count(str(child.previous_sibling.string), '(') > find_count(str(child.previous_sibling.string), ')'):
                            '''如果有多个节点，则第一个节点的下一个兄弟节点绝不会包括括号'''
                            if str(child.next_sibling).find(')') >= 0:  # find返回的是列表索引位置
                                child.next_sibling.replace_with(str(child.next_sibling.string)[str(child.next_sibling.string).find(')') + 1:])
                                child.previous_sibling.replace_with(str(child.previous_sibling.string)[:str(child.previous_sibling.string).rfind('(')])
                                child.extract()
                                continue
                            for target in list(child.next_siblings):
                                '''print(target.find(')'))与print(target.find(')')>=0)的区别，一个是bs4节点的查找函数一个是字符串的查找函数'''
                                if target.name == 'a' or str(target).find(')') >= 0:
                                    break
                                target.extract()
                        if find_count(str(child.next_sibling.string), '(') < find_count(str(child.next_sibling.string),')'):
                            if str(child.next_sibling).find(')') >= 0:  # find返回的是列表索引位置
                                child.next_sibling.replace_with(str(child.next_sibling.string)[str(child.next_sibling.string).find(')') + 1:])
                                child.previous_sibling.replace_with(str(child.previous_sibling.string)[:str(child.previous_sibling.string).rfind('(')])
                                child.extract()
                                continue
                            for target in list(child.previous_siblings):
                                if target.name == 'a' or str(target).rfind('(') >= 0:
                                    break
                                target.extract()

                        if find_count(str(child.previous_sibling.string), '[') > find_count(str(child.previous_sibling.string), ']'):
                            if str(child.next_sibling).find(']') >= 0:  # find返回的是列表索引位置
                                child.next_sibling.replace_with(str(child.next_sibling.string)[str(child.next_sibling.string).find(']') + 1:])
                                child.previous_sibling.replace_with(str(child.previous_sibling.string)[:str(child.previous_sibling.string).rfind('[')])
                                child.extract()
                                continue
                            for target in list(child.next_siblings):
                                if target.name == 'a' or str(target).find(']') >= 0:
                                    break
                                target.extract()

                        if find_count(str(child.next_sibling.string), '[') < find_count(str(child.next_sibling.string),']'):
                            if str(child.next_sibling).find(']') >= 0:  # find返回的是列表索引位置
                                child.next_sibling.replace_with(
                                    str(child.next_sibling.string)[str(child.next_sibling.string).find(']') + 1:])
                                child.previous_sibling.replace_with(
                                    str(child.previous_sibling.string)[:str(child.previous_sibling.string).rfind('[')])
                                child.extract()
                                continue
                            for target in list(child.previous_siblings):
                                if target.name == 'a' or str(target).rfind('[') >= 0:
                                    break
                                target.extract()

                        if find_count(str(child.previous_sibling.string), '(') == find_count(str(child.previous_sibling.string), ')') or find_count(str(child.next_sibling.string),'(') == find_count(str(child.next_sibling.string), ')'):  # 判别条件方宽松一些
                            if re.match('[fF]ig', child.get_text()):
                                if isinstance(child.next_sibling, NavigableString):
                                    child.next_sibling.replace_with('Figure ' + str(child.next_sibling.string))
                                    child.extract()
                                    continue
                                elif isinstance(child.previous_sibling, NavigableString):
                                    child.previous_sibling.replace_with(str(child.previous_sibling.string) + ' Fig')
                                    child.extract()
                                    continue
                            if re.match('[tT]ab', child.get_text()):
                                if isinstance(child.next_sibling, NavigableString):
                                    child.next_sibling.replace_with('Table' + str(child.next_sibling.string))
                                    child.extract()
                                    continue
                                elif isinstance(child.previous_sibling, NavigableString):
                                    child.previous_sibling.replace_with(str(child.previous_sibling.string) + ' Table')
                                    child.extract()
                                    continue
                    except Exception as e:
                        print(str(e))
                        print('>>>>>>>>>>>>段首或者段尾为链接节点<<<<<<<<<<')

        '''最终认为div节点中的span和p做为一个整体段落,关联性极强，同样也更简单一些  测试后发现div节点十分多样，其中超过三个span的也有例如10.1039/b009151k，10.1039/b104388a'''
        # div2span,建议在上述节点删除完后在执行，以使得有统一的规律
        if soup.select('span.c_heading_indent'):
            div_list = [tag.parent for tag in soup.select('span.c_heading_indent') if tag.parent.name == 'div']
            for div in div_list:
                # print([child.name for child in div.contents])
                # child_name_list = [child.name for child in div.contents]
                text = div.text
                div.clear()  # 用clear而不用contents、children加上extract方法时因为总有一个节点删除不了
                div.append(text)
                div['class'] = 'new_class'
                div.name = 'span'
                div.append(soup.new_tag('br'))

        spec = soup.find_all("span", "new_class")
        for i in range(len(spec) - 1, -1, -1):
            if spec[i].previous_sibling.name == 'span' and spec[i].previous_sibling.get('class') == 'new_class':
                spec[i].name = 'p'
                del spec[i]['class']

        # # 将三级标题或者四级标题和下一段的文本结合，最好还是在删除节点后执行，或者再次查找一次标题节点，好像不用因为之前没修改h3和h4的节点
        '''h4节点合并 h3节点合并    要让BeautifulSoup4 (bs4)忽略HTML标记之间的空格和换行符'''
        '''第一个办法找到某个tag，将下面的子节点之间的换行符用re.sub()删除，第二种用content方法删除'\n'节点,第三种跳过空格等空节点，查找span节点'''
        '''之前的代码仅修改了h2部分节点'''
        if h4:
            print('有h4节点')
            for i in range(len(h4)):
                if h4[0].next_sibling and h4[0].next_sibling.name == 'span':
                    pass
                    #print(h4[0].next_sibling.contents[0])
        elif h3:
            #print(len(h3))
            for i in range(len(h3)):
                # print(h3[i].next_siblings)
                # print([i.name for i in h3[i].next_siblings])
                if h3[i].next_sibling.name == 'span':  # 不能用find_next_sibling('span')，可能会导致跨过该h3节点指导的范围
                    if isinstance(h3[i].next_sibling.contents[0], NavigableString):
                        # print(h3[i].find_next_sibling('span').contents[0].replace("\n", " "))
                        h3[i].next_sibling.contents[0].replace_with(h3[i].text + ' . ' + str(h3[i].next_sibling.contents[0].string))
                    elif h3[i].next_sibling.contents[0].name == 'a':  # 链接节点
                        h3[i].next_sibling.contents[0].replace_with(h3[i].text + ' . ' + str(h3[i].next_sibling.contents[0].text))
                    elif isinstance(h3[i].next_sibling.contents[0], Tag):
                        h3[i].next_sibling.contents[0].replace_with(h3[i].text + ' . ' + str(h3[i].next_sibling.contents[0].text))
                    else:
                        print('>>>>>>>>>>>>修改错误<<<<<<<<<<')
                else:
                    print('>>>>>>>>>>>>h3节点后未跟span节点错误<<<<<<<<<<')

        # with open(list_html[j], 'wb') as f:
        #     f.write(str(soup.prettify()).encode())               #最好不要保存main_content[0],这样而可能会打乱数据的结构，不能在使用soup.select()

        doc = soup.find_all(id = 'wrapper')[0]
        if len(soup.find_all(id = 'wrapper')) == 1:
            span_p_tags = [tag for tag in doc.contents if (tag.name == 'span' or tag.name == 'p') and tag.text]
        else:
            print('文本结构有问题')


        counts = len(span_p_tags)
        print(counts)
        # 删除不包含字母和数字的中括号及其内容
        pattern = r'\[[^\w\d]*?\]'
        pattern1 = r'\([^\w\d]*?\)'
        pattern_excess_text = r'\(\)' + '|' r'\[\s*([-,]+\s*)*\s*\]'

        for i,element in enumerate(span_p_tags):
            '''只有参考文献的链接节点有中括号'''
            # print(re.sub(pattern1, '', re.sub(pattern, '', unicodedata.normalize('NFKC',element.text.replace("\n"," ").replace("\t", "")))))
            # print('>>><<<<')
            paras.append('第{}段 :'.format(i+1) + re.sub(pattern1, '', re.sub(pattern, '', unicodedata.normalize('NFKC',element.text.replace("\n"," ").replace("\t", "")))))
            #paras.append(unicodedata.normalize('NFKC', element.get_text()))
            number += 1
        if number != len(paras):
            print('{}分段错误'.format(url))
            # continue
        data = []
        data.append([dois[j], years[j], counts, len(paras), paras, number * [0]])
        with open('Dataset_rsc.csv', 'a', newline="", encoding='utf-8') as f:  # 写改为追加的方式；‘ab+’以二进制的形式写入
            writer = csv.writer(f)
            for line in data:
                writer.writerow(line)


def preprocess():
    df = pd.read_csv('count_year_url_publiser1039.csv', header=0)
    df_doi = df['doi']
    vals = [{}]*len(df)
    df.insert(loc=len(df.columns),column='name_dicts', value=vals)   #loc=0
    df.insert(loc=len(df.columns), column='compound_dicts', value=vals)
    list_html = glob('./1039/*.html')
    print(len(list_html))

    dois = [list_html[i][list_html[i].find('_') + 1:list_html[i].rfind('_')] for i in range(len(list_html))]
    dois = [dois[i].replace('_', '/') for i in range(len(dois))]
    years = [list_html[i][list_html[i].rfind('_') + 1:list_html[i].rfind('.')] for i in range(len(list_html))]
    # for i in range(len(df)):
    #     if df.doi[i] not in dois:
    #         df = df.drop(index = i)
    # df = df.reset_index(drop=True)
    # print(df)
    # df.to_csv('count_year_url_publiser1039.csv', index=False)
    # exit()
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
        for element in soup.find_all(text=lambda text: isinstance(text, str) and text.strip() == ''):
            element.extract()
        for element in soup.find_all(text=lambda text: text is not None and re.search(r'\s*\n\s*',text)):
            element.string.replace_with(re.sub(r'\s*\n\s*',' ',element.string))
        for element in soup.find_all(lambda tag: isinstance(tag, Tag) and tag.get_text().strip() == ''):
            element.extract()
        # 找到所有标签内仅包含空白字符的节点，并删除它们
        # for tag in soup.find_all():
        #     if tag.get_text(strip=True) == "":
        #         print(tag)
        #         tag.extract()

        # #适用于preprocess的文本
        main_text = soup.select('div #wrapper')          #div .main-content section .c-article-section__content

        # 删除所有的figure
        # figure_tags = soup.select('div .rtable__wrapper')       #属性不一定要全部取得，尤其是中间有空格
        # for m in range(len(figure_tags)):
        #     figure_tags[m].extract()
        # table_container = soup.select('div .table')
        # for h in range(len(table_container)):
        #     table_container[h].extract()
        table_tags = soup.select('div .table_caption')
        for n in range(len(table_tags)):
            table_tags[n].extract()
        img_tags = soup.select('div .image_table')
        for g in range(len(img_tags)):
            img_tags[g].extract()

        # 删除所有参考文献上标
        ref_tags = soup.select('sup a')
        for k in range(len(ref_tags)):
            ref_tags[k].extract()
        equ_tags = soup.select('.c-article-equation')
        for l in range(len(equ_tags)):
            print('有等式')
            equ_tags[l].extract()

        text_tag = soup.select('span.CH') + soup.select('span.TC') + soup.select('span.RTC') + soup.select('span.AN')   #10.1039/b008807m,不要新建一个节点导致后续一些判断失误，只添加到字符串节点的尾部
        for tag in text_tag:
            if isinstance(tag.previous_sibling, NavigableString):
                if isinstance(tag.next_sibling, NavigableString) and re.match(r'\w+', tag.next_sibling.string):
                    tag.next_sibling.string.replace_with(' ' + tag.next_sibling.string)
                tag.previous_sibling.string.replace_with(tag.previous_sibling.string + tag.text)
                tag.extract()
            elif isinstance(tag.next_sibling, NavigableString):
                tag.next_sibling.replace_with(tag.text + tag.next_sibling.string)
                tag.extract()
            elif isinstance(tag.previous_sibling, Tag):
                tag.previous_sibling.insert_after(tag.text + ' ')
                tag.extract()
            elif isinstance(tag.next_sibling, Tag):
                tag.next_sibling.insert_before(' ' + tag.text)
                tag.extract()


        metals = ['Si', 'K', 'Ce', 'La', 'Mo', 'Fe', 'Ru', 'W', 'Ba', 'Ga', 'Sm', 'Ho', 'Zr', 'Be', 'Y', 'Cd', 'As', 'Yb', 'V', 'Er', 'Ca', 'Lu', 'Ag', 'Cu', 'Na', 'Dy', 'U', 'Tb', 'Mg', 'Co', 'Zn', 'Li', 'Mn', 'In', 'Ni', 'Sr', 'Eu', 'Nd', 'Sc', 'Th', 'Gd', 'Bi', 'Cs', 'Pr', 'Al', 'Pb', 'Hg']
        elements = ['Si', 'K', 'Ce', 'La', 'Mo', 'Fe', 'Ru', 'W', 'Ba', 'Ga', 'Sm', 'Ho', 'Zr', 'Be', 'Y', 'Cd', 'As',
                  'Yb', 'V', 'Er', 'Ca', 'Lu', 'Ag', 'Cu', 'Na', 'Dy', 'U', 'Tb', 'Mg', 'Co', 'Zn', 'Li', 'Mn', 'In',
                  'Ni', 'Sr', 'Eu', 'Nd', 'Sc', 'Th', 'Gd', 'Bi', 'Cs', 'Pr', 'Al', 'Pb', 'Hg', 'Cl', 'Br', 'Si','ClO4−','BF4−' 'CF3SO3−', 'CF3CO2−', 'Se', 'tBu', 'H']

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

        # b节点变成strong或者是span.bold节点
        bold_tags = [tag for tag in list(soup.select('span.bold'))]
        for tag in bold_tags:
            if tag.text == '(' or tag.text == ')':
                tag.insert_before(tag.text)
                tag.extract()
                continue
            target_text = tag.get_text()
            b_node = soup.new_tag('strong')
            b_node.string = target_text
            tag.insert_before(b_node)
            tag.extract()

        #统一small和  sub节点或者时sup节点
        small_to_strong = [tag for tag in soup.find_all('small') if tag.find_all('sub') and not tag.find_parents('small')]
        for tag in small_to_strong:
            if len(tag.contents) == 1:
                tag.insert_before(tag.contents[0])
                tag.extract()

        small_to_strongs = [tag for tag in soup.find_all('small') if tag.find_all('sup') and not tag.find_parents('small')]
        for tag in small_to_strongs:
            if len(tag.contents) == 1:
                tag.insert_before(tag.contents[0])
                tag.extract()

        sups = [tag for tag in soup.find_all('sup') if tag.find_all('strong') and not tag.find_parents('sup') and len(tag.contents) == 1]
        for parent in sups:
            child = parent.contents[-1]
            parent.name = "strong"
            child.name = "sup"

        subs = [tag for tag in soup.find_all('sub') if tag.find_all('strong') and not tag.find_parents('sup') and len(tag.contents) == 1]
        for parent in subs:
            child = parent.contents[-1]
            parent.name = "strong"
            child.name = "sub"

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
        #10.1039 / c1cc12802g
        text2_tag = [tag for tag in soup.find_all('strong') if isinstance(tag.previous_sibling,NavigableString) and re.match(r'\d+',tag.text)]
        for tag in text2_tag:
            if tag.previous_sibling.string[-1] == '-':
                if re.search(r'\s+\(*(\S+)-', tag.previous_sibling.string):
                    text2 = re.search(r'\s+\(*(\S+-)', tag.previous_sibling.string).group(1)
                    if tag.previous_sibling.string.find(text2) + len(text2) == len(tag.previous_sibling.string):
                        tag.previous_sibling.string.replace_with(tag.previous_sibling.string.replace(text2,''))
                        tag.string = text2 + tag.text
        #exit()

        sbu_tag = [tag for tag in soup.find_all(string=lambda string: string is not None and re.match(r'\s+SBU\s+',string)) if tag.previous_siblings]
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
                elif isinstance(i, Tag) and i.name == 'i':
                    string = re.sub(r'\s+', ' ', i.text) + string
                elif isinstance(i, Tag) and i.name == 'strong':
                    string = re.sub(r'\s+', ' ', i.text) + string
                elif isinstance(i, Tag) and i.name == 'span' and ('class' in i.attrs):
                    if i['class'][0] == 'c-stack' or i['class'][0] == 'italic':
                        string = re.sub(r'\s+', ' ', i.text) + string
                else:
                    break
            index1 = string.rfind(' ')
            target_text = string[index1:]
            if re.search(pattern_item,target_text):
                tag.string.replace_with(re.sub(r'\s+SBU\s+',' ',tag.string))

        # 和10.1039/b102739p
        sub_tag = [tag for tag in soup.find_all('sub') + soup.find_all('span',class_='italic')]
        for tag in sub_tag:
            tag.string = re.sub(r'\s+',' ',tag.text)

        #直接将一些可能的连接字符也转换成黑体节点  10.1039/c0dt01174f 2·5H2O 1-Fe  r'[A-Z]$' 10.1039/C6DT00414H  2L·KF
        pre_strong = [tag for tag in list(soup.find_all('strong',text=lambda text: text is not None and re.match(r'\d$' + '|' + r'[A-z]$', text))) if tag.next_sibling and (tag.parent.name == 'span' or tag.parent.name == 'p' or tag.parent.name == 'th') and not tag.find_all()]
        for tag in pre_strong:
            if isinstance(tag.next_sibling,NavigableString):
                # print(tag)
                # print(tag.next_sibling)
                #替换一下顺序  10.1039/b810479d
                if tag.next_sibling.string[0] == '·' and tag.next_sibling.string.find(' ') == -1:  #or (tag.next_sibling.string[0] == '-' and tag.next_sibling.string )
                    # print(tag.next_sibling)
                    # print(tag.next_sibling.next_sibling)
                    target_text = tag.next_sibling.string
                    b_node = soup.new_tag('strong')
                    b_node.string = target_text
                    tag.next_sibling.extract()
                    tag.insert_after(b_node)
                    if tag.next_sibling.next_sibling:
                        if isinstance(tag.next_sibling.next_sibling,Tag):
                            if tag.next_sibling.next_sibling.name == 'sub':
                                b_node = soup.new_tag('strong')
                                b_node.append(tag.next_sibling.next_sibling)
                                #tag.next_sibling.next_sibling.extract()
                                tag.next_sibling.insert_after(b_node)
                                if tag.next_sibling.string[-1] == 'H' and isinstance(tag.next_sibling.next_sibling.next_sibling,NavigableString):
                                    if tag.next_sibling.next_sibling.next_sibling.string.find('O ') == 0 or tag.next_sibling.next_sibling.next_sibling.string.find('O)') == 0:
                                        tag.next_sibling.next_sibling.next_sibling.string.replace_with(tag.next_sibling.next_sibling.next_sibling.string[1:])
                                        strong_node = soup.new_tag('strong')
                                        strong_node.string = 'O'
                                        tag.next_sibling.next_sibling.next_sibling.insert_before(strong_node)
                            elif tag.next_sibling.next_sibling.name != 'strong':
                                continue
                        else:
                            continue



        # 10.1039/c0dt00864h  2-Mn
        strong_tag = [tag for tag in list(soup.find_all('strong')) if isinstance(tag.next_sibling, NavigableString) and tag.next_sibling.next_sibling and re.match(r'\d$',tag.text)]
        for tag in strong_tag:
            if tag.next_sibling.string == '-' and isinstance(tag.next_sibling.next_sibling, Tag):
                if re.match(pattern_element, tag.next_sibling.next_sibling.text):
                    target_text = tag.next_sibling.text
                    strong_node = soup.new_tag('strong')
                    strong_node.string = target_text
                    tag.next_sibling.insert_after(strong_node)
                    tag.next_sibling.extract()

        #rsc中多个黑体的节点可以并合处理   10.1039/b910994c
        strong_tags = [tag for tag in list(soup.find_all('strong')) if tag.next_sibling ]  #and not tag.find_parents('table')
        for tag in strong_tags:
            while isinstance(tag.next_sibling,Tag) and tag.next_sibling.text:
                if tag.next_sibling.name == 'strong' and tag.next_sibling.text[0] != ' ' and tag.text[-1] != ' ':
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


        # sect416 > span.c_heading_indent div节点的特殊处理（rsc）  10.1039/b008147g  div节点由h4和其之后的span节点结合而成
        div_heading_tags = [tag for tag in list(soup.select('span.c_heading_indent')) if tag.find_all("sub")]
        for tag in div_heading_tags:
            if isinstance(tag.contents[-1],NavigableString):
                target_text = tag.contents[-1].string
                if target_text.find(' ')>-1:
                    continue
                b_node = soup.new_tag('strong')
                b_node.string = target_text
                tag.contents[-1].insert_before(b_node)
                tag.contents[-1].extract()



        # #避免b节点和字符串节点紧贴，且无空格   少量文本的情况下影响不大   10.1039/c1cc12273h 加强约束
        string_b_tags = [tag for tag in soup.find_all('strong',text=lambda text: text is not None) if isinstance(tag.previous_sibling, NavigableString) and re.match('\d$',tag.text) and not tag.find_parents('sub') and not tag.find_parents('sup')]
        for tag in string_b_tags:
            if tag.previous_sibling.string[-1] == '(':
                pass
            elif (tag.previous_sibling.string[-1] != ' ' or tag.previous_sibling.string[-1] != '\xa0' ) and tag.next_sibling:
                if tag.next_sibling.string is None:
                    tag.previous_sibling.string.replace_with(tag.previous_sibling.string + ' ')
                elif tag.next_sibling.string[0]==',' or tag.next_sibling.string[0]=='.' or (tag.next_sibling.string[0] == ' ' and is_english_word(tag.next_sibling.string,0)):
                    tag.previous_sibling.string.replace_with(tag.previous_sibling.string + ' ')
                else:     #此b节点在化学式之后作为一个代词
                    pass

        # 避免sub节点和之前字符串节点紧贴且有空格，
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



        #10.1039/b102525m  sup和sub节点和strong节点紧贴
        sup_sup_strong_tags = [tag for tag in soup.find_all('strong') if isinstance(tag.previous_sibling, Tag) and re.match(r'\d$',tag.text) and isinstance(tag.next_sibling,NavigableString)]
        for tag in sup_sup_strong_tags:
            if tag.previous_sibling.name == 'sup' or tag.previous_sibling.name == 'sub':
                tag.insert_before(' ')

        # with open(list_html[j], 'wb') as f:
        #     f.write(str(soup).encode())
        # exit()


        #配合物的一些错误描述，(2, 2'-bipy)(H2O)] 多了一个空格
        compounds_excess = [tag for tag in soup.find_all(text=lambda text: text is not None and re.search(patt_compounds, text)) if tag.string]
        for tag in compounds_excess:
            tag.string.replace_with(re.sub(r'(N|\d),(\s+)(N|\d)',r'\1,\3',tag.string))

        #解码latex文本
        math_tags = [tag for tag in soup.find_all('span',class_="mathjax-tex") if tag.next_sibling and tag.previous_sibling]
        patt_latex = r'[\s|_]+'
        for tag in math_tags:
            latex_expr = tag.text
            unicode_text = LatexNodes2Text().latex_to_text(latex_expr)
            # print(unicode_text)
            # print(re.sub(patt_latex,'',unicode_text))
            tag.insert_after(re.sub(patt_latex,'',unicode_text))
            tag.extract()

        # with open(list_html[j], 'wb') as f:
        #     f.write(str(soup).encode())
        # exit()


        #sub节点后的字符串节点莫名出现多余的空格
        sub_blank_tags = [tag for tag in soup.find_all('sub') if tag.next_sibling and tag.previous_sibling]  #and tag.find_all('strong')  太绝对
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
                        elif isinstance(pre_next, Tag) and pre_next.name == 'i':
                            next_string = next_string + re.sub(r'\s+[∙·⋅]\s+', '·', re.sub(r'\s+', ' ', pre_next.text))
                        elif isinstance(pre_next, Tag) and pre_next.name == 'strong':
                            next_string = next_string + re.sub(r'\s+[∙·⋅]\s+', '·', re.sub(r'\s+', ' ', pre_next.text))
                        elif isinstance(pre_next, Tag) and pre_next.name == 'span' and ('class' in pre_next.attrs):
                            if pre_next['class'][0] == 'c-stack' or pre_next['class'][0] == 'italic' or pre_next['class'][0] == 'small_caps':
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
        spilt_text_and = [tag for tag in soup.find_all('strong', text=lambda text: text is not None and re.search(patt_text_and, text)) if tag.string]
        #print(len(spilt_text_and))
        for tag in spilt_text_and:
            # print(tag.string)
            # print(re.search(patt_text_and, tag.string).span())
            # print(tag.string[:re.search(patt_text_and, tag.string).span()[0]])
            # print(tag.string[re.search(patt_text_and, tag.string).span()[0]:re.search(patt_text_and, tag.string).span()[1]])
            # print(tag.string[re.search(patt_text_and, tag.string).span()[1]:])
            text = tag.string[re.search(patt_text_and, tag.string).span()[0]:re.search(patt_text_and, tag.string).span()[1]]
            b_next_node = soup.new_tag('strong')
            b_next_node.string = tag.string[re.search(patt_text_and, tag.string).span()[1]:]
            tag.string.replace_with(tag.string[:re.search(patt_text_and, tag.string).span()[0]])
            tag.insert_after(b_next_node)
            tag.insert_after(text)


        # test = [tag for tag in list(soup.find_all('strong',text=lambda text: text is not None and 'SBU2' in text))]   #text=lambda text: text is not None and 'Etypy' in text

        # 统一格式 Tb (7) Ce(9)数字代词前要有空格   10.1039_b900522f
        bold_num_tags = [tag for tag in list(soup.find_all('strong')) if re.match(r'\d$',tag.text) and isinstance(tag.next_sibling,NavigableString) and isinstance(tag.previous_sibling,NavigableString)]
        for tag in bold_num_tags:
            if len(tag.previous_sibling)>2 and len(tag.next_sibling)>2:
                if tag.previous_sibling.string[-1] == '(' and tag.previous_sibling.string[-2] != ' ' and tag.next_sibling.string[1] == ' ':
                    tag.previous_sibling.string.replace_with(tag.previous_sibling.string[:-1] + ' (')

        #规范格式(Ln = Pr,6;Nd,7;Y, 8).  10.1039/b911100j
        bold_num_tags = [tag for tag in list(soup.find_all('strong')) if re.match(r'\d$', tag.text) and isinstance(tag.previous_sibling,NavigableString)]
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
            if i.next_sibling.name == 'strong':
                i.string.replace_with(re.sub(patt9, r'] (', i.string))


        #10.1039/c0dt01718c   [(cod)HIr{μ-B(mt)3}IrCl(cod)]·2CH2Cl211·2CH2Cl2
        sub_blank_strong_tags = [tag for tag in list(soup.find_all('sub',text=lambda text: text is not None and re.match('[\d]', text))) + list(soup.find_all('sup',text=lambda text: text is not None and re.match('[\d]', text))) if tag.next_sibling]
        for tag in sub_blank_strong_tags:
            #10.1039/c0dt01718c K+2−
            if isinstance(tag.next_sibling,Tag):
                if tag.next_sibling.name == 'strong' and re.match('[\d]', tag.next_sibling.text):
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
                    elif isinstance(i, Tag) and i.name == 'i':
                        string = re.sub(r'\s+', ' ', i.text) + string
                    elif isinstance(i, Tag) and i.name == 'strong':
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
        excess = [tag for tag in soup.find_all('strong', text=lambda text: text is not None and re.search(patt_text, text)) if tag.string and isinstance(tag.next_sibling, NavigableString)]
        for tag in list(excess):
            target_text = ''
            target_text = tag.string[re.search(patt_text, tag.string).span()[0]+1:re.search(patt_text, tag.string).span()[1]-2]
            tag.string.replace_with(tag.text[:re.search(patt_text, tag.string).span()[0]])
            b_node = soup.new_tag('strong')
            b_node.string = target_text
            tag.insert_after('). ')
            tag.insert_after(b_node)
            tag.insert_after('(')


        patt_text_b = r'\s+\((\S+)\)'  # .在此种情况下只能是句号不可能是逗号
        excess_b = [tag for tag in soup.find_all('strong', text=lambda text: text is not None and re.search(patt_text_b, text)) if tag.string and isinstance(tag.next_sibling, NavigableString)]
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
                elif isinstance(i, Tag) and i.name == 'i':
                    string = re.sub(r'\s+', ' ', i.text) + string
                elif isinstance(i, Tag) and i.name == 'strong':
                    string = re.sub(r'\s+', ' ', i.text) + string
                elif isinstance(i, Tag) and i.name == 'span' and ('class' in i.attrs):
                    if i['class'][0] == 'c-stack' or i['class'][0] == 'italic' or i['class'][0] == 'small_caps':
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
                b_node = soup.new_tag('strong')
                b_node.string = tag.string[re.search(patt_text_b, tag.string).start(1):re.search(patt_text_b, tag.string).end(1)]
                b_next_node = soup.new_tag('strong')
                b_next_node.string = tag.string[re.search(patt_text_b, tag.string).end(1):]
                tag.string.replace_with(tag.string[:re.search(patt_text_b, tag.string).start(1)])
                tag.insert_after(b_next_node)
                tag.insert_after(b_node)
                # print(tag.string)
                # print(tag.next_sibling)
                # print(tag.next_sibling.next_sibling)

        patt_text_single_b = r'\((\S+)\)'  # .在此种情况下只能是句号不可能是逗号
        excess_single_b = [tag for tag in soup.find_all('strong', text=lambda text: text is not None and re.search(patt_text_single_b, text)) if tag.string and tag.next_sibling is None]
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
                elif isinstance(i, Tag) and i.name == 'i':
                    string = re.sub(r'\s+', ' ', i.text) + string
                elif isinstance(i, Tag) and i.name == 'strong':
                    string = re.sub(r'\s+', ' ', i.text) + string
                elif isinstance(i, Tag) and i.name == 'span' and ('class' in i.attrs):
                    if i['class'][0] == 'c-stack' or i['class'][0] == 'italic' or i['class'][0] == 'small_caps':
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
                elif isinstance(i, Tag) and i.name == 'i':
                    string = re.sub(r'\s+', ' ', i.text) + string
                elif isinstance(i, Tag) and i.name == 'strong':
                    string = re.sub(r'\s+', ' ', i.text) + string
                elif isinstance(i, Tag) and i.name == 'span' and ('class' in i.attrs):
                    if i['class'][0] == 'c-stack' or i['class'][0] == 'italic' or i['class'][0] == 'small_caps':
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
                elif isinstance(pre_next, Tag) and pre_next.name == 'small':
                    next_string = next_string + re.sub(r'\s+[∙·⋅]\s+', '·', re.sub(r'\s+', ' ', pre_next.text))
                elif isinstance(pre_next, Tag) and pre_next.name == 'i':
                    next_string = next_string + re.sub(r'\s+[∙·⋅]\s+', '·', re.sub(r'\s+', ' ', pre_next.text))
                elif isinstance(pre_next, Tag) and pre_next.name == 'strong':
                    next_string = next_string + re.sub(r'\s+[∙·⋅]\s+', '·', re.sub(r'\s+', ' ', pre_next.text))
                elif isinstance(pre_next, Tag) and pre_next.name == 'span' and ('class' in pre_next.attrs):
                    if pre_next['class'][0] == 'c-stack' or pre_next['class'][0] == 'italic' or pre_next['class'][0] == 'small_caps':
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

        pronoun_tags = [tag for tag in list(soup.find_all('strong')) if isinstance(tag.parent, Tag)]
        for tag in pronoun_tags:
            if tag.parent.name == 'sup' or tag.parent.name == 'sub':
                if isinstance(tag.parent.previous_sibling, Tag):
                    if tag.parent.previous_sibling.name == 'strong':
                        if tag.parent.previous_sibling.text[-1] != ' ':
                            new_tag = tag.parent
                            tag.parent.previous_sibling.append(new_tag)
                            tag.parent.extract()


        pronoun_tag = [tag for tag in list(soup.find_all('i')) if isinstance(tag.parent, Tag) and tag.parent.previous_sibling]
        for tag in pronoun_tag:
            if tag.parent.name == 'strong':
                if isinstance(tag.parent.previous_sibling, Tag):
                    if tag.parent.previous_sibling.name == 'strong':
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

        #10.1039/b102525m
        strong_connect_tags = [tag for tag in soup.find_all('strong') if re.match('\d–\d',tag.text)]
        for tag in strong_connect_tags:
            num1 = tag.text[:tag.text.find('–')]
            num2 = tag.text[tag.text.find('–')+1:]
            if num1.isdigit() and num2.isdigit():
                b_node = soup.new_tag('strong')
                b_node.string = num2
                tag.insert_after(b_node)
                tag.insert_after('–')
                tag.string = num1

        #10.1039/C5CE02174J table下的tfoot
        tfoot_tags = [tag for tag in soup.find_all('tfoot')]
        for tag in tfoot_tags:
            tag.extract()

        dct = {}
        compound_dct = {}
        b_tags = [tag for tag in list(soup.find_all('strong'))]    #[tag for tag in list(soup.select('.c-article-section__content b')) if tag.parent.name == 'p']
        b_tags_text = [tag.text for tag in b_tags]
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
            if b_tag.text.find('–') >-1:
                continue
            #10.1039/c0nj00144a
            if b_tag.find_parents('table'):  # table>thead>tr>th table>tbody>tr>td th和td内部可能也有节点     C9DT03511G不一样的表格
                if b_tag.parent.name == 'th':   #定位是tr的哪个th
                    th = b_tag.parent
                    tr = th.parent
                    thead = tr.parent
                    tbody = thead.next_sibling
                    if not tbody:
                        continue
                    tr_position = list(tr.children).index(th)
                    # print(len(tr))
                    # print(len(tbody.contents[0]))
                    if len(tr) + 1 == len(tbody.contents[0]) :
                        for tbody_tr in list(tbody):
                            if len(tbody_tr.contents) == len(tbody.contents[0]):
                                if re.search(pattern_item, tbody_tr.contents[tr_position + 1].text):
                                    wd = tbody_tr.contents[tr_position + 1].text
                    elif len(tr) == len(tbody.contents[0]):
                        for tbody_tr in list(tbody):
                            if len(tbody_tr.contents) == len(tbody.contents[0]):
                                if re.search(pattern_item, tbody_tr.contents[tr_position].text):
                                    wd = tbody_tr.contents[tr_position].text

            if list(b_tag.previous_siblings):
                for pre_str in b_tag.previous_siblings:
                    if isinstance(pre_str, NavigableString):
                        string = re.sub(r'\s+[∙·⋅]\s+', '·',re.sub(r'\s+', ' ', pre_str.string)) + string      #不能用+=,因为存入字符串的顺序要使得新存入的字符串压入最末尾
                    elif isinstance(pre_str, Tag) and pre_str.name == 'sub':
                        string = re.sub(r'\s+[∙·⋅]\s+', '·',re.sub(r'\s+', ' ', pre_str.text)) + string
                    elif isinstance(pre_str, Tag) and pre_str.name == 'sup':
                        string = re.sub(r'\s+[∙·⋅]\s+', '·',re.sub(r'\s+', ' ', pre_str.text)) + string
                    elif isinstance(pre_str, Tag) and pre_str.name == 'small':
                        string = re.sub(r'\s+[∙·⋅]\s+', '·', re.sub(r'\s+', ' ', pre_str.text)) + string
                    elif isinstance(pre_str, Tag) and pre_str.name == 'i':
                        string = re.sub(r'\s+[∙·⋅]\s+', '·',re.sub(r'\s+', ' ', pre_str.text)) + string
                    elif isinstance(pre_str, Tag) and pre_str.name == 'strong':
                        string = re.sub(r'\s+[∙·⋅]\s+', '·',re.sub(r'\s+', ' ', pre_str.text)) + string
                    elif isinstance(pre_str, Tag) and pre_str.name == 'span' and ('class' in pre_str.attrs):
                        if pre_str['class'][0] == 'c-stack' or pre_str['class'][0] == 'italic' or pre_str['class'][0] == 'small_caps':
                            string = re.sub(r'\s+', ' ', pre_str.text) + string
                    else:
                        break
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
                # print(wd)
                # print(string)
                # print(re.match(pattern_element,wd))


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

                #10.1039/C6CE02476A   化学式 compound 1
                if wd.find('compound') >-1 or wd.find('complex') > -1:
                    string = string[:string.rfind(' ')].replace(wd,'')
                    index1 = string.rfind(' ')
                    index2 = string[:string.rfind(' ')].rfind(' ')
                    if index1 > index2:
                        wd = string[index2 + 1:index1]
                    elif index1 == index2:
                        wd = ''
                # 10.1039/b107369a   化学式 structure 2,
                if wd.find('structure') > -1:
                    string = string[:-1].replace(wd, '')
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
                    elif isinstance(pre_next, Tag) and pre_next.name == 'i':
                        next_string = next_string + re.sub(r'\s+[∙·⋅]\s+', '·',re.sub(r'\s+', ' ', pre_next.text))
                    elif isinstance(pre_next, Tag) and pre_next.name == 'strong':
                        next_string = next_string + re.sub(r'\s+[∙·⋅]\s+', '·',re.sub(r'\s+', ' ', pre_next.text))
                    elif isinstance(pre_next, Tag) and pre_next.name == 'span' and ('class' in pre_next.attrs):
                        if pre_next['class'][0] == 'c-stack' or pre_next['class'][0] == 'italic' or pre_next['class'][0] == 'small_caps':
                            next_string = next_string + re.sub(r'\s+', ' ', pre_next.text)
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
                        if (next_string.find(':') == 0 and b_tag.previous_sibling) or next_string.find(';') == 0 :
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
                            # 10.1039/C6DT00414H  排比介绍一些材料 且这些代码的指代词都可以被识别为wd   10.1039/c1cc12796a
                            if next_string[len(wd)+2] == ',' and next_string.find(',') == 0 and next_string[len(wd)+1] != ')' and not b_tag.text.isdigit():
                                continue
                # print(next_string)
                # print(b_tag.text)
                #print(b_tag.previous_sibling)
                #print(string)
                # print(seq_wd)
                # print(wd)

            # with open(list_html[j], 'wb') as f:
            #     f.write(str(soup).encode())
            # exit()
            # for tag in soup.find_all('strong'):
            #     print(tag)

            #创建以及更新,字典的更新以及文本冗余的指代词的删除,同时进行
            if (re.search(pattern_item,wd) or (re.search(pattern_metal,wd) and len(re.findall(pattern_1, wd))>0)) and ' ' not in b_tag.text:  #and ']' not in b_tag.text and '[' not in b_tag.text
                # print(b_tag.text)
                # print(wd)
                # print(string)
                # print(next_string)
                # print(b_tag.parent.text)
                # print(b_tag.parent.prettify())
                #c5dt03178H
                if wd.find('⋯')>-1 or b_tag.text.find('(')>-1:
                    continue
                #10.1039/c1dt10778j
                if string[string.rfind(' ')+1:] and string[-1] != ' ':
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
                    # print(after_string)
                    # print(after_string[:after_string.find(' ')])
                    # print(after_string[:after_string.find(' ') - 1])
                    # print(after_string[:after_string.find(' ') - 2])


                if isinstance(b_tag.next_sibling,NavigableString):
                    if 2>b_tag.next_sibling.string.find('and')>-1:
                        continue
                if wd.count('(') != wd.count(')'):
                    wd1 = wd
                    wd = wd.strip(')').strip('(')
                    if wd.count('(') == wd.count(')') + 1:
                        wd = wd +')'
                    elif wd.count('(') + 1 == wd.count(')'):
                        wd = '(' + wd
                    if wd.count('(') != wd.count(')'):
                        wd = wd1
                #10.1039/b315243j
                if b_tag.text.find(',') >-1:
                    continue
                #10.1039/C4CY00125G  10.1039/b103107b
                if wd[-1] == ',' and string.rfind(' ') < len(string)-3:
                    continue
                if wd[-1] == ';'  or wd[-1] == ':' or wd[-1] == '.' or wd[-1] == ',':
                    wd = wd[:len(wd) - 1]
                if wd.find(':')>-1:
                    wd = wd[wd.find(':')+1:]
                if wd.count(']') == wd.count('[') == 1 and wd[0] == '[' and wd[-1] == ']':
                    wd = wd[1:len(wd) - 1]
                if wd.count(')') == wd.count('(') == 1 and wd[0] == '(' and wd[-1] == ')':
                    wd = wd[1:len(wd) - 1]
                if isinstance(b_tag.next_sibling,NavigableString):
                    if b_tag.next_sibling.string[0] == '·' and b_tag.text.find('·') == -1:
                        continue
                if re.search(pattern_item,b_tag.text) and not re.search(r'\d·\S+',b_tag.text):
                    continue
                #10.1039/b315291j   [VO(O2)(3OH-pic)2]−/[V(O2)2(3OH-pic)2]− (3b,
                if wd.find('/') > -1 and re.search(pattern_item,wd[wd.find('/')+1:]):
                    wd = wd[wd.find('/')+1:]
                if wd.find('—')>-1 or wd.find('/')>-1 or wd.find(' ')>-1 or re.search(r'\.[A-Za-z]+',wd) or (wd.count('{') != wd.count ('}')) or (wd.count('(') != wd.count (')')) or re.search(patt_math_formula,wd):   #中文版的长破折号  #10.1039/b901404g .句号
                    continue
                #print(b_tag.text and (b_tag.text[-1] == ')' or b_tag.text[0] == '(' or b_tag.text.find('−')>-1))
                if b_tag.text in dct :
                    if len(wd)>=len(dct[b_tag.text]):                                         #and b_tag.text.find('.')!=-1
                        if wd == next_string[1:next_string[1:].find(' ')+1]:
                            continue
                        #C19H20CoCuN4O10与[LCuCo(NO3)2]   10.1039/c0nj00238k,只在覆盖的情况下处理
                        if re.search(r'\(\S+\)',wd) is None and re.search(r'\(\S+\)',dct[b_tag.text]):
                            continue
                        dct[b_tag.text] = wd
                        b_tag.extract()
                    else:
                        pass
                else:
                    # print(b_tag.text)
                    # print(b_tag.next_sibling)
                    #print(wd)
                    if (b_tag.text.count(')') != b_tag.text.count ('(')  or b_tag.text.find('−')>-1) or (b_tag.text.count('(') != b_tag.text.count(')')) or (b_tag.text.count('{') != b_tag.text.count('}')):
                        continue
                    dct[b_tag.text] = wd
                    b_tag.extract()                  #之后剩余即是无化学式前文的b标签节点
                    # 10.1039/b102570h
                    if re.match(r'\d·\d', b_tag.text):
                        num = b_tag.text[0]
                        excess = b_tag.text[1:]
                        if num in b_tags_text and wd.find(b_tag.text[1:]) == len(wd) - len(b_tag.text[1:]):
                            wd = wd.replace(b_tag.text[1:], '')
                            dct[num] = wd
            if re.search(patt_compounds,wd):
                # print(b_tag.text)
                # print(wd)
                if wd.find('⋯') > -1 or b_tag.text.find('(') > -1:
                    continue
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
            # 10.1039/c0dt01718c  '1': '[HB(mt)2(pz3,5-Me)]−',
            for key in dct.keys():
                # print(dct[key])
                if dct[key][-1] == '−' or dct[key][-1] == '+':
                    dct[key] = dct[key][:-1]
        #print(len(dct))
        print(dct)
        #print(compound_dct)
        #print(list(dct.keys()))

        #10.1039/c0dt01718c  '1': '[HB(mt)2(pz3,5-Me)]−',
        for key in dct.keys():
            #print(dct[key])
            if dct[key][-1] == '−' or dct[key][-1] == '+':
                dct[key] = dct[key][:-1]

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
            pattern = r'\s+{}$'.format(key)
            tags = [tag for tag in list(soup.find_all('strong',text = lambda text: text is not None and re.match(pattern,text))) if tag.string and tag.previous_sibling]
            for tag in tags:
                if isinstance(tag.previous_sibling,NavigableString):
                    tag.previous_sibling.string.replace_with(tag.previous_sibling.string + ' ')
                    tag.string.replace_with(key)
                elif isinstance(tag.previous_sibling,Tag):
                    tag.insert_before(' ')
                    tag.string.replace_with(key)

        brackets2 = [f"({x}" for x in list(dct.keys())]
        brackets1 = [f"{x})" for x in list(dct.keys())]
        #print(adds)
        #print(len(dashs))
        #处理括号，应该在，-符号之前，因为这些符号在括号内部
        b_strong_tags = [tag for tag in list(soup.find_all('strong') + soup.find_all('strong')) if tag.parent.name == 'p' or tag.parent.name == 'span']
        for tag in b_strong_tags:
            for brac in brackets1:
                if tag.text.endswith(brac) and tag.string:
                    tag.insert_after(')')
                    tag.string.replace_with(tag.string[:len(tag.string)-1])

        b_strong_tags = [tag for tag in list(soup.find_all('strong') + soup.find_all('strong')) if tag.parent.name == 'p' or tag.parent.name == 'span']
        for tag in b_strong_tags:
            for brac in brackets2:
                if tag.text.find(brac) == 0 and tag.string:
                    tag.insert_before('(')
                    tag.string.replace_with(tag.string[1:])

        b_strong_tags = [tag for tag in list(soup.find_all('strong') + soup.find_all('strong')) if tag.parent.name == 'p' or tag.parent.name == 'span']
        combinations = [f"{x}, {y}" for x in list(dct.keys()) for y in list(dct.keys()) if x != y]
        dashs = [f"{x}-{y}" for x in list(dct.keys()) for y in list(dct.keys()) if x != y]
        adds = [f"{x}," for x in list(dct.keys())] + [f"{x}." for x in list(dct.keys())]
        for tag in b_strong_tags:
            for opt in combinations:
                str_copy = tag.text
                if tag.text.find(opt)>-1 and tag.string and len(tag.text)>=len(opt):                                    #tag.string而不是tag.text是为了使b节点内只有一个子节点
                    if tag.text.find(opt) == 0:
                        tag.string.replace_with(str_copy[:str_copy.find(', ')])
                        b_node = soup.new_tag('strong')
                        b_node.string = opt[opt.find(', ')+2:]
                        tag.insert_after(b_node)
                        tag.insert_after(', ')
                    else:
                        tag.string.replace_with(str_copy[:str_copy.find(opt)])
                        b_node1 = soup.new_tag('strong')
                        b_node1.string = opt[:opt.find(',')]
                        b_node2 = soup.new_tag('strong')
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
                    b_node = soup.new_tag('strong')
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
                if tag.next_sibling.name == 'span' and not tag.find_all('strong',text = key) and not tag.next_sibling.find_all('strong',text = key):
                    if re.search(r'[Ss]ynthesis',tag.text) and re.search(r'MOF' + '|' + r'[Cc]ompound',tag.text):
                        print(tag.text)
                        if isinstance(tag.contents[0],NavigableString):
                            tag.contents[0].string.replace_with(tag.text + ' ' + value)
                        elif isinstance(tag.contents[0],Tag):
                            tag.contents[0].string = tag.text + ' ' + value



        # 将各处包含-转为，
        for key in list(dct.keys()):
            b_strong_tags = soup.find_all('strong', string=key) + soup.find_all('strong', string=key)
            b_strong_tags = [tag for tag in b_strong_tags if tag.parent.name == 'p' or tag.parent.name == 'span']
            # print(len(b_strong_tags))
            for b_strong in b_strong_tags:
                if isinstance(b_strong.next_sibling, NavigableString):
                    if b_strong.next_sibling.string == '–' or b_strong.next_sibling.string == '-':
                        b_strong.next_sibling.extract()
                        if isinstance(b_strong.next_sibling, Tag) and b_strong.next_sibling.name == 'strong' and b_strong.next_sibling.text in list(dct.keys()):
                            if b_strong.text.isdigit() and b_strong.next_sibling.text.isdigit():
                                for dig in reversed(range(int(b_strong.text) + 1, int(b_strong.next_sibling.text))):
                                    b_strong.insert_after(', ')
                                    new_b_tag = soup.new_tag('strong')  # 创建新的<b>标签节点
                                    new_b_tag.string = str(dig)  # 设置<b>标签节点的文本内容
                                    b_strong.insert_after(new_b_tag)
                                b_strong.insert_after(', ')
                            elif list(dct.keys()).index(b_strong.text)>-1 and list(dct.keys()).index(b_strong.next_sibling.text)>-1:
                                for i in range(list(dct.keys()).index(b_strong.text) + 1,list(dct.keys()).index(b_strong.next_sibling.text)):
                                    b_strong.insert_after(', ')
                                    new_b_tag = soup.new_tag('strong')  # 创建新的<b>标签节点
                                    new_b_tag.string = str(dct[list(dct.keys())[i]])  # 设置<b>标签节点的文本内容
                                    b_strong.insert_after(new_b_tag)
                                b_strong.insert_after(', ')
                        elif isinstance(b_strong.next_sibling, Tag) and b_strong.next_sibling.name == 'strong':
                            if b_strong.next_sibling.text in list(dct.keys()):
                                if b_strong.text.isdigit() and b_strong.next_sibling.text.isdigit():
                                    for dig in reversed(range(int(b_strong.text) + 1, int(b_strong.next_sibling.text))):
                                        b_strong.insert_after(', ')
                                        new_b_tag = soup.new_tag('strong')  # 创建新的<b>标签节点
                                        new_b_tag.string = str(dig)  # 设置<b>标签节点的文本内容
                                        b_strong.insert_after(new_b_tag)
                                    b_strong.insert_after(', ')
                                elif list(dct.keys()).index(b_strong.text)>-1 and list(dct.keys()).index(b_strong.next_sibling.text)>-1:
                                    for i in range(list(dct.keys()).index(b_strong.text)+1,list(dct.keys()).index(b_strong.next_sibling.text)):
                                        b_strong.insert_after(', ')
                                        new_b_tag = soup.new_tag('strong')  # 创建新的<b>标签节点
                                        new_b_tag.string = str(dct[list(dct.keys())[i]])  # 设置<b>标签节点的文本内容
                                        b_strong.insert_after(new_b_tag)
                                    b_strong.insert_after(', ')

        #将各处的指示代词替换为原形
        for key in list(dct.keys()):
            # b_strong_tags = soup.find_all('b',text= key) + soup.find_all('strong',text= key)
            b_strong_tags = [tag for tag in soup.find_all('strong') + soup.find_all('b') if tag.text == key]
            b_tags = [tag for tag in b_strong_tags if tag.parent.name == 'p' or tag.parent.name == 'span']
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
                    elif isinstance(pre, Tag) and pre.name == 'strong':
                        string = re.sub(r'\s+', ' ', pre.text) + string
                    elif isinstance(pre, Tag) and pre.name == 'span' and ('class' in pre.attrs):
                        if pre['class'][0] == 'c-stack' or pre['class'][0] == 'italic' or pre['class'][0] == 'small_caps':
                            string = string + re.sub(r'\s+', ' ', pre.text)
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
                        new_b_tag = soup.new_tag('strong')
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
        compounud_tags = [tag for tag in soup.find_all(text=lambda text: text is not None and re.search(patt_equ, text)) if tag.parent.name == 'p' or tag.parent.name == 'span']
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
                elif isinstance(pre_str, Tag) and pre_str.name == 'i':
                    if pre_str.text.find(']') > -1:
                        pre_string = re.sub(r'\s+', ' ', pre_str.text) + pre_string
                        break
                    pre_string = re.sub(r'\s+[∙·⋅]\s+', '·', re.sub(r'\s+', ' ', pre_str.text)) + pre_string
                elif isinstance(pre_str, Tag) and pre_str.name == 'strong':
                    if pre_str.text.find(']') > -1:
                        pre_string = re.sub(r'\s+', ' ', pre_str.text) + pre_string
                        break
                    pre_string = re.sub(r'\s+[∙·⋅]\s+', '·', re.sub(r'\s+', ' ', pre_str.text)) + pre_string
                elif isinstance(pre_str, Tag) and pre_str.name == 'span' and ('class' in pre_str.attrs):
                    if pre_str['class'][0] == 'c-stack' and pre_str.text.find(']') > -1:
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
                    if string[0].split('(')[-1].split('[')[-1] and string[0].split('(')[-1].split('[')[-1].find('http') == -1 and string[1].find('/') == -1:
                        text = string[1]
                        key = string[0].split('(')[-1].split('[')[-1]
                        if key.rfind('{')>-1:
                            key = key[key.rfind('{')+1:]
                        if (key.count(')') != key.count('(')) or (key.count('[') != key.count(']')) or (key.count('{') != key.count('}')):
                            continue
                        if string[0].split('(')[-1].split('[')[-1].rfind('(')>-1:
                            key = key[key.rfind('(')+1:]
                        if text.count('[') < text.count(']') and text[-1] != ']':
                            text = text[:text.rfind(']')]
                        if text.count('{') < text.count('}') and text[-1] != '}':
                            text = text[:text.rfind('}')]
                        if text.count('(') < text.count(')') and text[-1] != ')':
                            text = text[:text.rfind(')')]
                        if text.count('[') > text.count(']') and text[0] != '[':
                            text = text[text.find('[')+1:]
                        if text.count('{') > text.count('}') and text[0] != '{':
                            text = text[text.find('{')+1:]
                        if text.count('(') > text.count(')') and text[0] != '(':
                            text = text[text.find('(')+1:]
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

        # 10.1039/c0nj00217h footnotes中有合成段落
        # footnotes_tags = [tag for tag in soup.find_all('span', attrs={'class': 'sup_ref'}) if len(tag.get('id', [])) == 1 and 'sup_ref' in tag.get('class', []) and tag.find_parents('td')]
        footnotes_tags = [tag for tag in soup.find_all('span', id=True) if tag.find_parents('td')]
        h3_tags = [tag for tag in soup.find_all('h3')]
        h2_tags = [tag for tag in soup.find_all('h2')]
        for tag in footnotes_tags:
            if len(h2_tags) > 1:  # footnotes和refrences 可能有h2和h3节点
                if h2_tags[-2].text.find('knowledgement') > -1 and ('id' in h2_tags[-2].attrs):  # 不包括开头的字母，避免首字母大小写问题
                    h2_tags[-1].insert_before(tag)
                elif h2_tags[-1].text.find('eferen') > -1 and ('id' in h2_tags[-1].attrs) and isinstance(
                        h2_tags[-1].parent, Tag):
                    if tag.text.find('ynthesi') > -1 and h2_tags[-1].parent.name == 'span':
                        h2_tags[-1].parent.insert_before(tag)


        #10.1134/S1066362221040056  append和insert_after的差异      合并段落，部分段落以，结尾
        for l in range(len(main_text)):
            for content in [p_tag for p_tag in main_text[l].contents if p_tag.name=='p' or p_tag.name == 'span']:
                if content.next_sibling:
                    if (content.next_sibling.name == 'p' or content.next_sibling.name == 'span') and content.text[-1]==',':
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

        #清空在以追加模式存入，无法以追加模式覆盖
        for l in range(len(main_text)):
            new_tag = ptag_merge_h3tag(main_text[l])
            main_text[l].replace_with(new_tag)  # 如何返回一个bs4.element.Tag类型       其实也可以不用再将修改后main_text[i]内容置入main_text[i],直接分部存入文档就行   继续打印main_text[i],其实其值是并未改变的，改变的是Beautifuisoup对象，oldtag会从Beautifulsoup对象中删除，newtag会被添加到oldtag位置上。
        # with open(list_html[j], 'wb') as f:
        #     f.write(str(soup).encode())

    if 'flags' in list(df.columns):
        df = df.drop(df[df['flags'] == 2].index, axis=0)
    df.to_csv('count_year_url_publiser_dict1039.csv', index=False)



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
                if p_tag.name == 'p' or p_tag.name == 'span':
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
                if p_tag.name == 'p' or p_tag.name == 'span':
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

    h3_tags = soup.find_all('h3')
    for i in range(len(h3_tags)):
        p_tag = h3_tags[i].find_next_sibling()
        if p_tag:
            if p_tag.name == 'p' or p_tag.name == 'span':
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

    h2_tags = soup.find_all('h2')
    for i in range(len(h2_tags)):
        p_tag = h2_tags[i].find_next_sibling()
        if p_tag:
            if p_tag.name == 'p' or p_tag.name == 'span':
                if isinstance(h2_tags[i].contents[-1], NavigableString):
                    h2_tags[i].contents[-1].replace_with(h2_tags[i].contents[-1].string + '. ')  # 标题文本的字符串形式影响小
                elif isinstance(h2_tags[i].contents[-1], Tag):
                    h2_tags[i].contents[-1].append('. ')
                for content in reversed(list(h2_tags[i].contents)):
                    p_tag.contents[0].insert_before(content)
                h2_tags[i].extract()
            else:
                h2_tags[i].extract()
        else:
            h2_tags[i].extract()


    if len(soup.contents) == 1:
        return soup.contents[0]


def test(path):
    with open(path, 'r', encoding='utf-8') as f:  # list_html[j]
        soup = BeautifulSoup(f.read(),'lxml')
        #print(soup.prettify())

    main_content = soup.select('div #wrapper')
    #print(len(main_content[0].contents))
    print(path)

    print(len(soup.find_all(text=None)))
    # 好像删除了下面两个就没有None节点l
    for link in soup.find_all(["br", "hr"]):
        link.extract()
    for link in soup.find_all(text="\n"):
        link.extract()
    # for link in soup.find_all(text=None):
    #     link.extract()
    print(len(soup.find_all(text=None)))

    # 删除所有的图像节点
    figure_tags = soup.select('div .image_table')
    # print(len(figure_tags))
    for h in range(len(figure_tags)):
        figure_tags[h].extract()

    #删除所有的table节点 可能是公式之类的 （1）（2）（3）（4）...
    table = soup.select('table')
    for j in range(len(table)):
        table[j].extract()

    # 删除所有参考文献上标和脚注
    ref_tags = soup.select('a[title="Select to navigate to references"]')+soup.select('a[title="Select to navigate to reference"]') + soup.select('a[title="Select to navigate to footnote"]')           # 属性值   加了s代表多个，未加s表示一个
    # print(len(ref_tags))
    for k in range(len(ref_tags)):
        ref_tags[k].extract()

    # 删除所有表格节点
    table_tags = soup.select('div .table_caption')
    rtable_tags = soup.select('div .rtable__wrapper')
    # print(len(table_tags))
    # print(len(rtable_tags))
    for m in range(len(table_tags)):
        table_tags[m].extract()
    for n in range(len(rtable_tags)):
        rtable_tags[n].extract()

    span_and_p = [index for index, value in enumerate(main_content[0].contents) if value.name == 'span' or value.name == 'p']
    print(len(span_and_p))

    span = soup.select('span')
    p = soup.select('p')
    p_span = p+span
    print(len(p_span))

    h2 = soup.select('h2')
    h3 = soup.select('h3')
    h4 = soup.select('h4')
    print([h2[i].get_text().strip() for i in range(len(h2))])                            #用strip函数来节点文本内容中的空白符
    print([repr(h3[i].get_text()) for i in range(len(h3))])            #.replace("\n", " ").replace("\t", "")
    #print(len(h3))
    #print(len(h2))


    #删除什么abstract块之前的兄弟节点和Conflicts of interest和Acknowledgements块之后所有的兄弟节点
    abstract_tag = soup.select('div .abstract')
    if abstract_tag:
        for i in list(abstract_tag[0].previous_siblings):
            i.extract()
        abstract_tag[0].extract()


    '''只要找到acknowledge节点即可终止循环，那么也不需要在h2-indexs循环'''
    for i in h2:
        if i.get_text().strip() == 'Conflicts of interest' or i.get_text().strip() == 'Acknowledgements' or i.get_text().strip() == 'Notes and references':
            print(i.get_text())
            print(len(list(i.next_siblings)))
            if 0<len(list(i.next_siblings))<10:
                for tag in list(i.next_siblings):         #加上list函数，打成一个循环体
                    print('>>>>><<<<<<')
                    print(len(list(i.next_siblings)))
                    if isinstance(tag,NavigableString):
                        print('it is a NavigableString')
                    else:
                        print('it is a tag')
                    tag.extract()
                i.extract()     # 注意节点去除的顺序
                break
            elif 0<len(list(i.parent.next_siblings))<10:
                for tag in list(i.parent.next_siblings):         #加上list函数，打成一个循环体
                    tag.extract()
                i.extract()     # 注意节点去除的顺序
                break


    '''有很多的文字节点也要清除一下，以免于链接节点混肴'''
    '''特殊情况，两个文字节点连续叠在一起,兄节点返回空节点'''
    text_tag = soup.select('span.CH') + soup.select('span.TC') + soup.select('span.RTC') + soup.select('span.AN')
    # print(len(text_tag))
    for tag in text_tag:  # 段首或者段尾的极端情况
        if isinstance(tag.previous_sibling, NavigableString):
            tag.previous_sibling.replace_with(tag.previous_sibling.string + tag.text)
            tag.extract()
        elif isinstance(tag.next_sibling, NavigableString):
            tag.next_sibling.replace_with(tag.text + tag.next_sibling.string)
            tag.extract()
        elif isinstance(tag.previous_sibling, Tag):
            tag.next_sibling.replace_with(tag.previous_sibling.text + tag.text)
            tag.extract()
        elif isinstance(tag.next_sibling, Tag):
            tag.next_sibling.replace_with(tag.text + tag.next_sibling.text)
            tag.extract()
        else:
            print(tag)
            print('>>>>>>>文字链接无兄弟节点有错误<<<<<<<')

    #测试文字节点删除
    text_tag = soup.select('span.CH') + soup.select('span.TC')
    print(len(text_tag))

    # for child in soup.select('a'):
    #     if re.match('[fF]ig', child.get_text()):
    #         child.replace_with('Fig')
    #     if re.match('[tT]ab', child.get_text()):
    #         child.replace_with('Table')

    print(soup.select('a'))
    number, paras = 0, []
    #加上div标签是因为若是在修正rsc结构后提取文本格式的内容，损失了很多的信息,故先处理冗余信息，在修改结构
    for element in [tag for tag in soup.select('div #wrapper')[0].contents if tag.name == 'span' or tag.name == 'p' or tag.name == 'div' ]:
        if element.find_all('a'):
            print([tag.text for tag in element.find_all('a')])
            # print([i.string for i in element.find_all('a')])
            # print(len([i.string for i in element.find_all('a')]))
            for child in element.find_all('a'):  # find_next_sibling和next_sibling，前一个只找寻tag节点
                try:
                    if child.previous_sibling and child.next_sibling:     #避开前后两个节点均为链接节点的错误
                        print(find_count(str(child.previous_sibling.string), '(') > find_count(str(child.previous_sibling.string),')'))
                        print(find_count(str(child.next_sibling.string), '(') < find_count(str(child.next_sibling.string), ')'))
                        if find_count(str(child.previous_sibling.string), '(') > find_count(str(child.previous_sibling.string),')') and find_count(str(child.next_sibling.string), '(') < find_count(str(child.next_sibling.string), ')'):
                            print(1)
                            child.previous_sibling.replace_with(str(child.previous_sibling.string)[:str(child.previous_sibling.string).rfind('(')])  # 本来想用节点替换的方式，结果发现tag中包含的字符串（即Navigablestring对象）不能编辑,但是可以被替换成其它的字符串
                            # print(str(child.next_sibling.string)[str(child.next_sibling.string).find(')')+1:])
                            child.next_sibling.replace_with(str(child.next_sibling.string)[str(child.next_sibling.string).find(')') + 1:])
                            child.extract()
                            continue

                        if find_count(str(child.previous_sibling.string), '(') > find_count(str(child.previous_sibling.string), ')'):
                            '''如果有多个节点，则第一个节点的下一个兄弟节点绝不会包括括号'''
                            if str(child.next_sibling).find(')') >= 0:  # find返回的是列表索引位置
                                print(3)
                                child.next_sibling.replace_with(str(child.next_sibling.string)[str(child.next_sibling.string).find(')') + 1:])
                                child.previous_sibling.replace_with(str(child.previous_sibling.string)[:str(child.previous_sibling.string).rfind('(')])
                                child.extract()
                                continue
                            for target in list(child.next_siblings):
                                '''print(target.find(')'))与print(target.string.find(')')>=0)的区别，一个是bs4节点的查找函数一个是字符串的查找函数'''
                                if target.name == 'a' or str(target).find(')') >= 0:
                                    break
                                target.extract()
                        if find_count(str(child.next_sibling.string), '(') < find_count(str(child.next_sibling.string), ')'):
                            if str(child.next_sibling).find(')') >= 0:  # find返回的是列表索引位置
                                print(4)
                                child.next_sibling.replace_with(str(child.next_sibling.string)[str(child.next_sibling.string).find(')') + 1:])
                                child.previous_sibling.replace_with(str(child.previous_sibling.string)[:str(child.previous_sibling.string).rfind('(')])
                                child.extract()
                                continue
                            for target in list(child.previous_siblings):
                                if target.name == 'a' or str(target).rfind('(') >= 0:
                                    break
                                target.extract()
                        if find_count(str(child.previous_sibling.string), '[') > find_count(str(child.previous_sibling.string), ']'):
                            print(child.text)
                            print('schema')
                            if str(child.next_sibling).find(']') >= 0:  # find返回的是列表索引位置
                                print(3)
                                child.next_sibling.replace_with(str(child.next_sibling.string)[str(child.next_sibling.string).find(']') + 1:])
                                child.previous_sibling.replace_with(str(child.previous_sibling.string)[:str(child.previous_sibling.string).rfind('[')])
                                child.extract()
                                continue
                            for target in list(child.next_siblings):
                                if target.name == 'a' or str(target).find(']') >= 0:
                                    break
                                target.extract()

                        if find_count(str(child.next_sibling.string), '[') < find_count(str(child.next_sibling.string), ']'):
                            print(child.text)
                            print('schema')
                            if str(child.next_sibling).find(']') >= 0:  # find返回的是列表索引位置
                                print(4)
                                child.next_sibling.replace_with(str(child.next_sibling.string)[str(child.next_sibling.string).find(']') + 1:])
                                child.previous_sibling.replace_with(str(child.previous_sibling.string)[:str(child.previous_sibling.string).rfind('[')])
                                child.extract()
                                continue
                            for target in list(child.previous_siblings):
                                if target.name == 'a' or str(target).rfind('[') >= 0:
                                    break
                                target.extract()

                        if find_count(str(child.previous_sibling.string), '(') == find_count(str(child.previous_sibling.string),')') or find_count(str(child.next_sibling.string), '(') == find_count(str(child.next_sibling.string), ')'):      #判别条件方宽松一些
                            print(2)
                            if re.match('[fF]ig', child.get_text()):
                                if isinstance(child.next_sibling, NavigableString):
                                    child.next_sibling.replace_with('Figure ' + str(child.next_sibling.string))
                                    child.extract()
                                    continue
                                elif isinstance(child.previous_sibling, NavigableString):
                                    child.previous_sibling.replace_with(str(child.previous_sibling.string)+' Fig')
                                    child.extract()
                                    continue
                            if re.match('[tT]ab', child.get_text()):
                                if isinstance(child.next_sibling, NavigableString):
                                    child.next_sibling.replace_with('Table' + str(child.next_sibling.string))
                                    child.extract()
                                    continue
                                elif isinstance(child.previous_sibling, NavigableString):
                                    child.previous_sibling.replace_with(str(child.previous_sibling.string)+' Table')
                                    child.extract()
                                    continue
                except Exception as e:
                    print(str(e))
                    print('>>>>>>>>>>>>段首或者段尾为链接节点<<<<<<<<<<')

    #修改rsc段落的格式
    '''最终认为div节点中的span和p做为一个整体段落,关联性极强，同样也更简单一些  测试后发现div节点十分多样，其中超过三个span的也有例如10.1039/b009151k，10.1039/b104388a'''
    #div2span,建议在上述节点删除完后在执行，以使得有统一的规律
    if soup.select('span.c_heading_indent'):
        div_list = [tag.parent for tag in soup.select('span.c_heading_indent') if tag.parent.name == 'div']
        for div in div_list:
            print([child.name for child in div.contents])
            #child_name_list = [child.name for child in div.contents]
            text = div.text
            div.clear()        #用clear而不用contents、children加上extract方法时因为总有一个节点删除不了
            div.append(text)
            div['class'] = 'new_class'
            div.name = 'span'
            div.append(soup.new_tag('br'))

    print('<<<<<<<<<>>>>>>>>>')
    # print([tag.get('class') for tag in soup.select('span.new_class')])
    spec = soup.find_all("span", "new_class")
    # print(spec)
    print(len(spec))
    for i in range(len(spec) - 1, -1, -1):
        print(i)
        print(spec[i].previous_sibling.name == 'span')
        print(spec[i].previous_sibling.get('class') == 'new_class')
        if spec[i].previous_sibling.name == 'span' and spec[i].previous_sibling.get('class') == 'new_class':
            spec[i].name = 'p'
            del spec[i]['class']


    #合并节点，三级标题或者四级标题与之后的sapn节点合并   这一步应该放在不在使用h3或者h4节点之后     有h4节点就不需要h3节点即h4的优先级比h3高
    '''h4节点合并 h3节点合并    要让BeautifulSoup4 (bs4)忽略HTML标记之间的空格和换行符'''
    '''第一个办法找到某个tag，将下面的子节点之间的换行符用re.sub()删除，第二种用content方法删除'\n'节点,第三种跳过空格等空节点，查找span节点'''
    '''之前的代码仅修改了h2部分节点'''
    if h4:
        print(len(h4))
        print('有h4节点')
        for i in range(len(h4)):
            print(h4[0].next_sibling)
            if h4[0].next_sibling and h4[0].next_sibling.name == 'span':
                print(h4[0].next_sibling.contents[0])
    elif h3:
        print(len(h3))
        for i in range(len(h3)):
            if h3[i].next_sibling.name == 'span':            #不能用find_next_sibling('span')，可能会导致跨过该h3节点指导的范围
                if isinstance(h3[i].next_sibling.contents[0], NavigableString):
                    #print(h3[i].find_next_sibling('span').contents[0].replace("\n", " "))
                    h3[i].next_sibling.contents[0].replace_with(h3[i].text + ' . ' + str(h3[i].next_sibling.contents[0].string))
                elif h3[i].next_sibling.contents[0].name == 'a':      #链接节点
                    h3[i].next_sibling.contents[0].replace_with(h3[i].text + ' . ' + str(h3[i].next_sibling.contents[0].text))
                elif isinstance(h3[i].next_sibling.contents[0], Tag):
                    # print(h3[i].text)
                    # print(type(h3[i].next_sibling))
                    print('>>>>>>>>>>>>修改错误<<<<<<<<<<')
            else:
                print(h3[i].next_sibling.name)
                print(h3[i].find_next_sibling())
                print(type(h3[i].next_sibling))
                print([i.name for i in h3[i].find_next_siblings()])
                print('>>>>>>>>>>>>h3节点后未跟span节点错误<<<<<<<<<<')

    with open('zui1'+path, 'wb+') as f:
        f.write(str(soup.prettify()).encode())



#'Leveraging Composition-Based Material Descriptors for Machine Learning Optimization'
    # h2 = soup.select('h2')
    # h3 = soup.select('h3')
    # print(len(h2))
    # print(len(h3))
    # if not h2:
    #     print('h2 is empty')
    # if not h3:
    #     print('h3 is empty')
    #
    # #因为有循环条件要以h2标签收束，故在之前去除节点时， 其实也不需要因为最后一个H2节点可以只查找兄弟节点，先写出规范的
    # paras,number = [],0
    # for children in h2:
    #     number = 0
    #     # print(list(children.next_siblings))
    #     # print(len(list(children.next_siblings)))
    #     # list_children = [tag.name for tag in children.next_silbings]
    #     # print(list_children)
    #
    #     for tag in list(children.next_siblings):
    #         if tag.name == 'h2':
    #             break
    #         if tag.name == 'span':
    #             paras.append(tag.get_text())
    #             number += 1
    #         if tag.name == 'p':
    #             paras.append(tag.get_text())
    #             number += 1
    #     print(paras)
    #     print(number)
    #     print('>>>>>>>>><<<<<<<<<<<')


def find_count(str,char):
    count = 0
    for element in str:
        if element == char:
            count += 1
    return count


if __name__ == '__main__':
    # dic_error = dict()
    # for i in range(9130,len(urls)): #248,393,422,974,2053,3100，3358，3980，4530，5648，6700,7710,7970,8360,8880    len(urls)
    #     #print(urls[i])
    #     url_response = get_resonse(urls[i])
    #     soup = BeautifulSoup(url_response.text, 'html.parser')
    #     #print(soup.prettify())
    #     print(dois[i])
    #     if soup.select('div #About') or soup.select('#maincontent'):        #需要付费  因为少了个空格才一直报错，名字和属性名        记得换headers头
    #         print( 1 )
    #         dic_error[i] = dois[i]
    #     else:
    #         print(0)
    #         savehtml(url_response,'DOI_10.1039_'+urls[i][urls[i].rfind('/')+1:urls[i].rfind('?')] + '_' + str(years[i]))
    #     # if i%9 == 0:
    #     #     time.sleep(2)
    #     with open('result.csv','a',newline="", )as f:           #写改为追加的方式；‘ab+’以二进制的形式写入
    #         writer = csv.writer(f)
    #         for i, j in zip(list(dic_error.keys()), list(dic_error.values())):  # 为什么不是紧凑的数据格式
    #             data = ','.join(j)
    #             writer.writerow([i] + [j])

    #test('DOI_10.1039_D1TC01048D_2021.html')                      #有一个问题，h2 abstract藏在div class = ‘abstract’下     可以在rsc原文验证
    #test('DOI_10.1039_b007079n_2001.html')
    #test('DOI_10.1039_c1ce05287j_2011.html')
    #test('DOI_10.1039_b006142p_2001.html')
    #test('DOI_10.1039_b9nj00361d_2010.html')
    #test('DOI_10.1039_b104388a_2001.html')
    #test('DOI_10.1039_D0CE00317D_2020.html')
    #test('DOI_10.1039_b305356c_2003.html')
    #test('DOI_10.1039_C6QI00477F_2017.html')
    #test('DOI_10.1039_b108206j_2001.html')
    #test('DOI_10.1039_b915001c_2010.html')
    #test('DOI_10.1039_b915440j_2010.html')
    #test('DOI_10.1039_c0dt00195c_2010.html')
    preprocess()
    #orignaltext_clean()

#10.1039_b007868i  特例compoud A and compound B...1,2
#10.1039/c0nj00260g  易混肴
#10.1039/c0jm04387g
