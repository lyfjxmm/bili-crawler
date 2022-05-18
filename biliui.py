from ast import Not
import os
import subprocess
import re
import configparser
import fenxiuser
import fenxiall
from xml.dom import UserDataHandler
import bilidynamic
from lxml import etree
from qrlogin import Qrlogin
from io import BytesIO
from threading import Thread
from tkinter import *
from tkinter import ttk, filedialog
from matplotlib import image
from userinfo import insert_videoinfo, insert_view, insert_user_follow_uid
from mytool import biliconfig
from bilisql import SQLOperating
from user import User
from PIL import Image, ImageTk
config = biliconfig()


HOST = config.host
USER = config.user
PWD = config.password
PORT = config.port
BILINAME = config.biliname
BILIPWD = config.bilipwd


class photo(Thread):
    def __init__(self, frame):
        Thread.__init__(self)
        self.frame = frame

    def run(self):

        qr = Qrlogin()
        status = qr.is_cookie_exist()
        if not status:
            qr.show_QRcode_img(self.frame)
            qr.login()


class BiliGui:
    def __init__(self):
        self.root = Tk()

        self.root.geometry('400x400+750+300')
        s = ttk.Style()
        s.theme_use('vista')
        # 添加组件
        self.add_notebook()  # 3个标签页
        # 用户界面
        self.get_data_page()
        # 设置界面
        self.config_page()
        self.QR_page()
        self.addBtn()

        self.root.resizable(0, 0)
        self.root.title('B站数据操作界面')
        self.root.mainloop()
# 添加3个标签页

    def add_tab_page(self, title):
        tab = Frame(self.notebook)
        self.notebook.add(tab, text=title)
        return tab

    def add_notebook(self):
        self.notebook = ttk.Notebook(self.root,
                                     width=self.root.winfo_screenwidth(),
                                     height=self.root.winfo_screenheight(), )
        self.tab1 = self.add_tab_page('  所有数据  ')
        self.tab2 = self.add_tab_page('  特定用户  ')
        self.tab3 = self.add_tab_page('  设置  ')
        self.tab4 = self.add_tab_page('  扫码登录  ')
        self.notebook.pack()

    def QR_page(self):
        self.qrFrame = ttk.LabelFrame(
            self.tab4, text='请打开APP端扫码二维码登录', labelanchor='nw')
        self.qrFrame.place(relx=0.02, rely=0.01, relwidth=0.96, relheight=0.8)

        # qrcode = Image.open(qrlogin.get_QRcode())
        # qrcode = ImageTk.PhotoImage(qrcode.resize((256, 256), Image.ANTIALIAS))
        # qrimage = Label(self.qrFrame, image=qrcode)
        # qrimage.image = qrcode
        # qrimage.pack()


# 获取数据页的具体设置


    def get_data_page(self):
        self.userFrame = ttk.LabelFrame(
            self.tab2, text='选定uid用户', labelanchor='nw')
        self.userFrame.place(relx=0.02, rely=0.01,
                             relwidth=0.96, relheight=0.5)
        Label(self.userFrame, text='uid', anchor='w', font=('宋体', 9), width=60,
              height=1,).place(relx=0.02, rely=0, relwidth=0.2)
        self.biliuid = Entry(self.userFrame,
                             width=20, bd=0,
                             relief='solid',
                             highlightcolor='#3AB7FF',
                             highlightthickness=1,
                             highlightbackground='#9096A2')
        self.biliuid.place(relx=0.15, rely=0,
                           relwidth=0.8, relheight=0.15)


# 设置页的具体设置
    # 添加文本标签

    def add_text_Lable(self, frame, label, y):
        Label(frame, text=label, anchor='w', font=('宋体', 9),
              width=60, height=1, ).place(relx=0.02, rely=y, relwidth=0.2, relheight=0.25)

    def config_page(self):
        self.sqlFrame = ttk.LabelFrame(
            self.tab3, text='数据库设置', labelanchor="nw")
        self.sqlFrame.place(relx=0.02, rely=0.01, relwidth=0.96, relheight=0.5)
        self.biliFrame = ttk.LabelFrame(
            self.tab3, text='B站账号设置', labelanchor="nw")
        self.biliFrame.place(relx=0.02, rely=0.51,
                             relwidth=0.96, relheight=0.3)
        self.add_text_Lable(self.sqlFrame, '地址', 0)
        self.add_text_Lable(self.sqlFrame, '端口', 0.25)
        self.add_text_Lable(self.sqlFrame, '用户', 0.50)
        self.add_text_Lable(self.sqlFrame, '密码', 0.75)
        Label(self.biliFrame, text='用户', anchor='w', font=('宋体', 9),
              width=60, height=1, ).place(relx=0.02, rely=0, relwidth=0.2, relheight=0.5)
        Label(self.biliFrame, text='密码', anchor='w', font=('宋体', 9),
              width=60, height=1, ).place(relx=0.02, rely=0.5, relwidth=0.2, relheight=0.5)

        host = StringVar()
        host.set(HOST)
        port = StringVar()
        port.set(PORT)
        root = StringVar()
        root.set(USER)
        pwd = StringVar()
        pwd.set(PWD)
        biliname = StringVar()
        biliname.set(BILINAME)
        bilipwd = StringVar()
        bilipwd.set(BILIPWD)

        self.hostInput = Entry(self.sqlFrame,
                               width=30, bd=0,
                               relief='solid',
                               highlightcolor='#3AB7FF',
                               highlightthickness=1,
                               highlightbackground='#9096A2',
                               textvariable=host)
        self.hostInput.place(relx=0.15, rely=0.05,
                             relwidth=0.8, relheight=0.15)
        self.portInput = Entry(self.sqlFrame,
                               width=30, bd=0,
                               relief='solid',
                               highlightcolor='#3AB7FF',
                               highlightthickness=1,
                               highlightbackground='#9096A2',
                               textvariable=port)
        self.portInput.place(relx=0.15, rely=0.30,
                             relwidth=0.8, relheight=0.15)
        self.rootInput = Entry(self.sqlFrame,
                               width=30, bd=0,
                               relief='solid',
                               highlightcolor='#3AB7FF',
                               highlightthickness=1,
                               highlightbackground='#9096A2',
                               textvariable=root)
        self.rootInput.place(relx=0.15, rely=0.55,
                             relwidth=0.8, relheight=0.15)
        self.pwdInput = Entry(self.sqlFrame,
                              width=30, bd=0,
                              relief='solid',
                              highlightcolor='#3AB7FF',
                              highlightthickness=1,
                              highlightbackground='#9096A2',
                              show="*",
                              textvariable=pwd)
        self.pwdInput.place(relx=0.15, rely=0.80,
                            relwidth=0.8, relheight=0.15)
        self.bilinameInput = Entry(self.biliFrame,
                                   width=30, bd=0,
                                   relief='solid',
                                   highlightcolor='#3AB7FF',
                                   highlightthickness=1,
                                   highlightbackground='#9096A2',
                                   textvariable=biliname)
        self.bilinameInput.place(relx=0.15, rely=0.1,
                                 relwidth=0.8, relheight=0.3)
        self.bilipwdInput = Entry(self.biliFrame,
                                  width=30, bd=0,
                                  relief='solid',
                                  highlightcolor='#3AB7FF',
                                  highlightthickness=1,
                                  highlightbackground='#9096A2',
                                  show="*",
                                  textvariable=bilipwd)
        self.bilipwdInput.place(relx=0.15, rely=0.6,
                                relwidth=0.8, relheight=0.3)
# 添加按钮，赋予按钮事件

    def save_info(self):  # 保存信息按钮
        host = self.hostInput.get()
        port = self.portInput.get()
        root = self.rootInput.get()
        pwd = self.pwdInput.get()
        biliname = self.bilinameInput.get()
        bilipwd = self.bilipwdInput.get()
        config = configparser.ConfigParser()
        config.read('./config.ini')
        config.set('MySQL', 'host', host)
        config.set('MySQL', 'port', port)
        config.set('MySQL', 'user', root)
        config.set('MySQL', 'password', pwd)
        config.set('Bili', 'username', biliname)
        config.set('Bili', 'password', bilipwd)
        with open('./config.ini', 'w')as f:
            config.write(f)

    def qrcode_show(self):  # 获取二维码图片
        # 检测本地是否有
        t = photo(self.qrFrame)
        t.start()

    def create_db(self):
        biliSql = SQLOperating()
        biliSql.create_database()
        biliSql.create_upinfo_table()

    def get_user_follow(self):
        biliuid = self.biliuid.get()
        biliuser = User(biliuid)
        insert_user_follow_uid(biliuser)

    def get_dynamic(self):
        biliuid = int(self.biliuid.get())
        bilidynamic.getData(biliuid)
        tree = etree.HTML(bilidynamic.useLocalData(biliuid))
        bilidynamic.dynamicAnalyse(tree)

        bilidynamic.tagAnalyse(tree)

    def update_user_follow_data(self):
        insert_videoinfo()  # 更新投稿分区
        insert_view()  # 更新播放，点赞，阅读数

    def fenxi_all(self):
        fenxiall.out_table_html()

    def fenxi_user(self):
        biliuid = int(self.biliuid.get())
        fenxiuser.out_table_html(biliuid)

    def addBtn(self):
        ttk.Button(self.tab1, width=8, text='创建数据库',
                   command=self.create_db).place(relx=0.02, rely=0.02, relwidth=0.5)
        ttk.Button(self.tab1, text='导出报告',command=self.fenxi_all).place(relx=0.02, rely=0.1)
        ttk.Button(self.userFrame, text='获取关注', command=self.get_user_follow).place(
            relx=0.02, rely=0.2, relwidth=0.3)
        ttk.Button(self.userFrame, text='获取动态', command=self.get_dynamic).place(
            relx=0.34, rely=0.2, relwidth=0.3)
        ttk.Button(self.userFrame, text='更新数据库', command=self.update_user_follow_data).place(
            relx=0.66, rely=0.2, relwidth=0.3)
        ttk.Button(self.userFrame, text='导出报告',command=self.fenxi_user).place(
            relx=0.02, rely=0.45, relwidth=0.3)
        ttk.Button(self.userFrame, text='导出csv').place(
            relx=0.34, rely=0.45, relwidth=0.3)
        ttk.Button(self.tab3,
                   width=8,
                   text='保存信息',
                   command=self.save_info).place(relx=0.02, rely=0.86, relheight=0.1, relwidth=0.96)
        ttk.Button(self.tab4, width=8, text='获取二维码', command=self.qrcode_show).place(
            relx=0.02, rely=0.86, relheight=0.1, relwidth=0.76)
        ttk.Button(self.tab4, width=8, text='注销', ).place(
            relx=0.78, rely=0.86, relheight=0.1, relwidth=0.20)


if __name__ == '__main__':
    app = BiliGui()
