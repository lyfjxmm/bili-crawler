from typing import final
import pymysql
import re
from mytool import biliconfig
config=biliconfig()

HOST = config.host
USER = config.user
PASSWORD = config.password
PORT = config.port

class SQLOperating:    
    def __init__(self):
        self.conn = pymysql.connect(
            host=HOST, user=USER, password=PASSWORD, port=PORT)
        self.cursor = self.conn.cursor()

    def get_conn(self):
        self.conn = pymysql.connect(
            host=HOST, user=USER, password=PASSWORD, port=PORT, db='bili')
        self.cursor = self.conn.cursor()

    def close_conn(self):
        self.cursor.close()
        self.conn.close()

    def create_database(self):
        try:
            self.cursor.execute('show databases')
            data = self.cursor.fetchall()
            listdata = list(data)
            result = ('bili',) in listdata
            if not result:
                sql = "CREATE DATABASE IF NOT EXISTS bili"
                self.cursor.execute(sql)
        except Exception as e:
            print('出错:', e)
        finally:
            self.close_conn()

    def create_upinfo_table(self):
        try:
            self.get_conn()
            sql = "show tables"
            self.cursor.execute(sql)
            tables = [self.cursor.fetchall()]
            table_list = re.findall('(\'.*?\')', str(tables))
            table_list = [re.sub("'", '', each) for each in table_list]
            if 'all_up_info' in table_list:
                pass
            else:
                sql = '''
                    CREATE TABLE `all_up_info`  (
                    `uid` int NOT NULL,
                    `用户名` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
                    `性别` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
                    `等级` int NULL DEFAULT NULL,
                    `粉丝牌` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
                    `大会员` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
                    `认证` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
                    `关注数` int NULL DEFAULT NULL,
                    `粉丝数` int NULL DEFAULT NULL,
                    `获赞数` int NULL DEFAULT NULL,
                    `播放数` int NULL DEFAULT NULL,
                    `阅读数` int NULL DEFAULT NULL,
                    `总投稿数` int NULL DEFAULT NULL,
                    `动画` int NULL DEFAULT NULL,
                    `番剧` int NULL DEFAULT NULL,
                    `国创` int NULL DEFAULT NULL,
                    `音乐` int NULL DEFAULT NULL,
                    `舞蹈` int NULL DEFAULT NULL,
                    `游戏` int NULL DEFAULT NULL,
                    `知识` int NULL DEFAULT NULL,
                    `科技` int NULL DEFAULT NULL,
                    `生活` int NULL DEFAULT NULL,
                    `美食` int NULL DEFAULT NULL,
                    `动物圈` int NULL DEFAULT NULL,
                    `鬼畜` int NULL DEFAULT NULL,
                    `时尚` int NULL DEFAULT NULL,
                    `资讯` int NULL DEFAULT NULL,
                    `娱乐` int NULL DEFAULT NULL,
                    `影视` int NULL DEFAULT NULL,
                    `TV剧` int NULL DEFAULT NULL,
                    `放映厅` int NULL DEFAULT NULL,
                    `纪录片` int NULL DEFAULT NULL,
                    `运动` int NULL DEFAULT NULL,
                    `汽车` int NULL DEFAULT NULL,
                    `电视剧` int NULL DEFAULT NULL,
                    `电影` int NULL DEFAULT NULL,
                    PRIMARY KEY (`uid`) USING BTREE
                    ) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;
                '''
                self.cursor.execute(sql)
        except Exception as e:
            print('出错:', e)
        finally:
            self.close_conn()

    def show_uid_list(self):
        try:
            self.get_conn()
            sql = 'SELECT uid FROM `bili`.`all_up_info`'
            self.cursor.execute(sql)
            uidlist = list(self.cursor.fetchall())
            uidlist = [int(re.sub(r"[\(\),]", "", str(each)))
                       for each in uidlist]
        except Exception as e:
            print('出错:', e)
        finally:
            self.close_conn()
            return uidlist

    def show_uid_no_video(self):
        try:
            self.get_conn()
            sql = 'SELECT uid FROM `bili`.`all_up_info` WHERE `总投稿数` is null'
            self.cursor.execute(sql)
            uidlist = list(self.cursor.fetchall())
            uidlist = [int(re.sub(r"[\(\),]", "", str(each)))
                       for each in uidlist]
        except Exception as e:
            print('出错:', e)
        finally:
            self.close_conn()
            return uidlist

    def show_uid_no_views(self):
        try:
            self.get_conn()
            sql = 'SELECT uid FROM `bili`.`all_up_info` WHERE `播放数` is null'
            self.cursor.execute(sql)
            uidlist = list(self.cursor.fetchall())
            uidlist = [int(re.sub(r"[\(\),]", "", str(each)))
                       for each in uidlist]
        except Exception as e:
            print('出错:', e)
        finally:
            self.close_conn()
            return uidlist

    def insert_up_basicinfo(self, infolist):
        self.get_conn()
        sql = 'INSERT INTO `bili`.`all_up_info` ' \
              '(`uid`,`用户名`,`性别`,`等级`,`粉丝牌`,`大会员`,`认证`,`关注数`,`粉丝数`) ' \
              'VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        try:
            self.cursor.executemany(sql, infolist)
            self.conn.commit()
        except Exception as e:
            print('导入数据库失败:', e)
            self.conn.rollback()
        finally:
            self.close_conn()
            return

    def insert_up_video_area(self, videoarealist):
        self.get_conn()
        sql = 'UPDATE `bili`.`all_up_info` SET `总投稿数`=%s,`动画`=%s,`番剧`=%s,`国创`=%s,`音乐`=%s,`舞蹈`=%s,`游戏`=%s,`知识`=%s,' \
              '`科技`=%s,`生活`=%s,`美食`=%s,`动物圈`=%s,`鬼畜`=%s,`时尚`=%s,`资讯`=%s,`娱乐`=%s,`影视`=%s,`TV剧`=%s,`放映厅`=%s,`纪录片`=%s,' \
              '`运动`=%s,`汽车`=%s,`电视剧`=%s,`电影`=%s WHERE uid=%s '
        try:
            self.cursor.executemany(sql, videoarealist)
            self.conn.commit()
        except Exception as e:
            print('导入数据库失败:', e)
            self.conn.rollback()
        finally:
            self.close_conn()
            return None

    def insert_up_views(self, upview):
        self.get_conn()
        sql = 'UPDATE `bili`.`all_up_info` SET `播放数`=%s,`获赞数`=%s,`阅读数`=%s WHERE uid=%s '
        try:
            self.cursor.executemany(sql, upview)
            self.conn.commit()
        except Exception as e:
            print('导入数据库失败:', e)
            self.conn.rollback()
        finally:
            self.close_conn()
            return
