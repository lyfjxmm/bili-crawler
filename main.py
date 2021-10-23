from user import User
from bilisql import SQLOperating
from user import User
from rich.progress import track
from time import sleep
from mytool import dict_to_tuple
from views import BrowsDriver


def get_upinfo(uidlist):
    upInfoList = []
    for i in track(uidlist, description='获取up主基础信息中'):
        sleep(1)
        up = User(i)
        up.basic_info()
        upInfoList.append(up.back_info())
    return upInfoList


def insert_user_follow_uid(biliuser, bilisql=SQLOperating()):
    # 获取关注列表
    followList = biliuser.follow_list()
    # 不在数据库中的uid列表
    isNotExis = list(set(followList)-set(bilisql.show_uid_list()))
    # 导入数据
    bilisql.insert_up_basicinfo(get_upinfo(isNotExis))


def insert_videoinfo(bilisql=SQLOperating()):
    uidlist = bilisql.show_uid_no_video()
    insertSQLvideolist = []
    for i in track(uidlist, description='获取投稿分区信息中'):
        up = User(i)
        videodict = up.up_video()
        insertSQLvideolist.append(dict_to_tuple(videodict))
        sleep(1)
    bilisql.insert_up_video_area(insertSQLvideolist)

# ２个方法，第一个方法，利用selenium打开页面获取信息，速度相当快
# def insert_view(bilisql=SQLOperating()):
#     uidlist = bilisql.show_uid_no_views()
#     driver = BrowsDriver()
#     driver.login_bili()
#     views = driver.open_up_space(uidlist)
#     bilisql.insert_up_views(views)
# 第二个方法，利用API获取返回信息，太快可能被ban，目前1s间隔
def insert_view(bilisql=SQLOperating()):
    uidlist = bilisql.show_uid_no_views()
    driver = BrowsDriver()
    driver.login_bili()
    driver.get_cookie()
    driver.close_driver()
    views = driver.get_view_info(uidlist)
    bilisql.insert_up_views(views)


if __name__ == '__main__':
    # 创建数据库，表
    biliSql = SQLOperating()
    biliSql.create_database()
    biliSql.create_upinfo_table()
    # 主程序 设置B站uid，将关注的up导入数据库
    biliuser = User(15810)
    insert_user_follow_uid(biliuser)
    # 更新数据
    insert_videoinfo()  # 更新投稿分区
    insert_view() # 更新播放，点赞，阅读数
