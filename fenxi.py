from pyecharts.globals import ThemeType
from mytool import biliconfig
from user import User
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from pyecharts.charts import Pie, Page
from pyecharts import options as opts
config = biliconfig()

HOST = config.host
USER = config.user
PASSWORD = config.password
PORT = config.port

# MySQL拿数据


def get_data():
    engine = create_engine('mysql+pymysql://'+USER+':' +
                           PASSWORD+'@'+HOST+':'+str(PORT)+'/bili')
    sql = 'SELECT * FROM all_up_info'
    df = pd.read_sql_query(sql, engine)
    # None替换为NaN
    df.fillna(np.nan, inplace=True)
    df['大会员'].replace(np.nan, '无', inplace=True)
    df['最多投稿分区'] = df.apply(
        lambda x: x.iloc[13: 36].astype('float64').idxmax(), axis=1)
    df['十万粉丝'] = df.apply(lambda x: '十万粉以上' if x.粉丝数 >
                          100000 else '以下', axis=1)

    df.drop(df.columns[13:36], axis=1, inplace=True)
    return df

# 用户关注的dataframe


def user_following_df(uid, df):
    followlist = User(uid).follow_list()
    userDf = df[df['uid'].apply(lambda x: x in followlist)]
    return userDf


# 生成图表
# 生成基础饼图


def create_pie(df, text, title) -> Pie:
    data = df['{}'.format(text)].value_counts().to_dict()
    pie = (
        Pie(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
        .add(
            "", 
            [list(z) for z in zip(data.keys(), data.values())],
            radius=["30%", "75%"],
            # center=["75%", "50%"],
            rosetype="radius",)
        .set_global_opts(title_opts=opts.TitleOpts(title="{}".format(title)))
    )
    return pie


def out_table_html():
    df = get_data()
    # df = user_following_df(15810, df)
    page = Page(layout=Page.SimplePageLayout)
    page.add(
        create_pie(df,'十万粉丝','粉丝量'),
        create_pie(df, '最多投稿分区', 'UP主投稿'),
    )
    page.render("分析数据.html")


if __name__ == "__main__":
    out_table_html()
