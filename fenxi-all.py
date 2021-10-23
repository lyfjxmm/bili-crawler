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


def create_pie(df) -> Pie:
    fans = df['十万粉丝'].value_counts().to_dict()
    vip = df['大会员'].value_counts().to_dict()
    area = df['最多投稿分区'].value_counts().to_dict()

    pie = (
        Pie(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
        .add(
            "",
            [list(z) for z in zip(fans.keys(), fans.values())],
            radius=["20%", "50%"],
            center=["16%", "50%"],
            rosetype="radius",
            label_opts=opts.LabelOpts(is_show=False),)
        .add(
            "",
            [list(z) for z in zip(vip.keys(), vip.values())],
            radius=["20%", "50%"],
            center=["48%", "50%"],
            rosetype="radius",)
        .add(
            "",
            [list(z) for z in zip(area.keys(), area.values())],
            radius=["20%", "50%"],
            center=["80%", "50%"],
            rosetype="radius",)
        .set_global_opts(title_opts=opts.TitleOpts(title="粉丝量，大会员，最常投稿分区"))
    )
    return pie


def out_table_html():
    df = get_data()
    # df = user_following_df(15810, df)
    page = Page(layout=Page.SimplePageLayout)
    page.add(
        create_pie(df),
    )
    page.render("分析数据.html")


if __name__ == "__main__":
    out_table_html()
