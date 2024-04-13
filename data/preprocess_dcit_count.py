import pandas as pd
df = pd.read_csv('count_year_url_publiser_dict1016.csv', header=0)
print(len(df))
print(df.columns)
count = 0
#eval函数可以将字符串数据还原为原类型
for i in range(len(df)):
    if len(eval(df['name_dicts'][i])) > 0 or len(eval(df['compound_dicts'][i])) > 0 :
        count += 1
print(count)

