from pyecharts.globals import ThemeType
from mytool import biliconfig
from user import User
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from pyecharts.charts import Pie, Page, Bar
from pyecharts import options as opts
config = biliconfig()

HOST = config.host
USER = config.user
PASSWORD = config.password
PORT = config.port


def get_data(uid):
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
    # 用户关注的dataframe
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


def create_bar(df: pd.DataFrame) -> Bar:
    ups = df['用户名'].to_list()
    views = df['播放数'].to_list()
    fans = df['粉丝数'].to_list()
    likes = df['获赞数'].to_list()
    reads = df['阅读数'].to_list()
    bar = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
        .add_xaxis(ups)
        .add_yaxis('播放量', views)
        .add_yaxis('粉丝数', fans)
        .add_yaxis('获赞数', likes)
        .add_yaxis('阅读数', reads)
        .set_global_opts(
            title_opts=opts.TitleOpts(title="基础数据统计"),
            xaxis_opts=opts.AxisOpts(
                axislabel_opts=opts.LabelOpts(rotate=-45)),
            datazoom_opts=opts.DataZoomOpts(),
        )
    )
    return bar


def create_bar_1(df: pd.DataFrame) -> Bar:
    ups = df['用户名'].to_list()
    df['比例'] = df.apply(lambda x: x.粉丝数/((x.播放数)/(x.总投稿数+1)), axis=1)
    fansEff = df['比例'].to_list()
    bar = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
        .add_xaxis(ups)
        .add_yaxis('活跃度', fansEff)
        .set_global_opts(
            title_opts=opts.TitleOpts(title="粉丝活跃度"),
            xaxis_opts=opts.AxisOpts(
                axislabel_opts=opts.LabelOpts(rotate=-45)),
            datazoom_opts=opts.DataZoomOpts(),
        )
    )
    return bar


def out_table_html(uid):
    df = get_data(uid)
    page = Page(layout=Page.SimplePageLayout)
    page.add(
        create_pie(df),
        create_bar(df),
        create_bar_1(df),
    )
    page.render("{}的关注分析.html".format(uid))


# if __name__ == "__main__":
#     out_table_html(5239084)
