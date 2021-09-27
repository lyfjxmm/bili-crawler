import pandas as pd
from sqlalchemy import create_engine
import pandas_profiling


engine = create_engine('mysql+pymysql://root:123123@localhost:3306/bili')
sql = 'SELECT * FROM all_up_info'
df = pd.read_sql_query(sql, engine)

# 导出报告
porfile = pandas_profiling.ProfileReport(df)
filepath = './关系报告.html'
porfile.to_file(filepath)
# 导出csv
path = './数据/B站UP主数据.csv'
df.to_csv(path, index=False)
