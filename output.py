import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import pandas_profiling
from mytool import biliconfig
config = biliconfig()

HOST = config.host
USER = config.user
PASSWORD = config.password
PORT = config.port
engine = create_engine('mysql+pymysql://'+USER+':' +
                       PASSWORD+'@'+HOST+':'+str(PORT)+'/bili')
sql = 'SELECT * FROM all_up_info'
df = pd.read_sql_query(sql, engine)
df.fillna(np.nan, inplace=True)
df['大会员'].replace(np.nan, '无', inplace=True)
df['最多投稿分区'] = df.apply(
    lambda x: x.iloc[13: 36].astype('float64').idxmax(), axis=1)
df['十万粉丝'] = df.apply(lambda x: '十万粉以上' if x.粉丝数 > 100000 else '以下', axis=1)

df.drop(df.columns[13:36], axis=1, inplace=True)
# 导出报告
porfile = pandas_profiling.ProfileReport(df)
filepath = './关系报告.html'
porfile.to_file(filepath)
# 导出csv
path = './B站UP主数据.csv'
df.to_csv(path, index=False)
