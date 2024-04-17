from habanero import Crossref
import pandas as pd
import csv
cr = Crossref()

#domain = 'https://pubs.rsc.org/en/content/articlehtml/'
domain = 'https://pubs-rsc-org-s--ccmu.jitui.me/en/content/articlehtml/'
df = pd.read_csv('count_publisher1039.csv',header=0)
list1 = list(df['doi'])
list2 = []
dic = dict()      #有异常的doi

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
# # 获取文献的发表年份,使用crossref中的works()函数来获取文献信息,从文献信息中获取发表年份
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
#         list2.append('error')
#         continue

# 新增一列
# print(len(list2))
# print(list2)
# df.insert(3, 'year', list2)
# df.to_csv('count_year_publiser.csv', index=False)
# print(dict)

#根据上述获得的年份拼接出固定的url链接
def get_list_urls(self, entry_url):
    base_url = entry_url[:entry_url.rfind('/') + 1]
    response = requests.get(entry_url, headers=self.headers)
    response.encoding = 'gb2312'
    soup = BeautifulSoup(response.text, 'html.parser')
    option_list = soup.select('select[name=sldd] option')
    return [base_url + option.attrs['value'] for option in option_list]

if __name__ == '__main__':
    df = pd.read_csv('count_year_publiser1039.csv', header=0)
    #https: // pubs.rsc.org / en / content / articlehtml / 2012 / ce / c1ce06015e?page = search
    tral_url = '?page=search'
    list3 = list(df['doi'])
    list5 = [list3[i][10:12] for i in range(len((list3)))]
    years = list(df['year'])
    list4 = [domain + years[i] + '/' + list5[i] + '/' + list3[i][8:] + tral_url for i in range(len(years))]
    print(list4)
    df.insert(4, 'url', list4)
    df.insert(5, 'core', list5)
    df.to_csv('count_year_url_publiser1039-.csv', index=False)


# from habanero import Crossref
# import pandas as pd
# cr = Crossref()
#
# # 获取文献的发表年份
# doi = '10.1039/a700682i'
#
# # 使用crossref中的works()函数来获取文献信息
# article = cr.works(ids=doi)
#
# # 从文献信息中获取发表年份
# year = article['message']['issued']['date-parts'][0][0]
#
# print(year)


