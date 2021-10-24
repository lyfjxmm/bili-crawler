import os
import subprocess
from threading import Thread
from tkinter import *
from tkinter import ttk, filedialog
import re
from mytool import biliconfig
import configparser
config = biliconfig()


HOST = config.host
USER = config.user
PWD = config.password
PORT = config.port
BILINAME = config.biliname
BILIPWD = config.bilipwd


class BiliGui:
    def __init__(self):
        self.root = Tk()

        self.root.geometry('400x400+750+300')
        s = ttk.Style()
        s.theme_use('vista')
        # 添加组件
        self.add_notebook()  # 3个标签页
        # 设置界面
        self.config_page()
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
        self.notebook.pack()
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
                               width=30,
                               relief='solid',
                               textvariable=host)
        self.hostInput.place(relx=0.15, rely=0.05,
                             relwidth=0.8, relheight=0.15)
        self.portInput = Entry(self.sqlFrame,
                               width=30,
                               relief='solid',
                               textvariable=port)
        self.portInput.place(relx=0.15, rely=0.30,
                             relwidth=0.8, relheight=0.15)
        self.rootInput = Entry(self.sqlFrame,
                               width=30,
                               relief='solid',
                               textvariable=root)
        self.rootInput.place(relx=0.15, rely=0.55,
                             relwidth=0.8, relheight=0.15)
        self.pwdInput = Entry(self.sqlFrame,
                              width=30,
                              relief='solid',
                              show="*",
                              textvariable=pwd)
        self.pwdInput.place(relx=0.15, rely=0.80,
                            relwidth=0.8, relheight=0.15)
        self.bilinameInput = Entry(self.biliFrame,
                                   width=30,
                                   relief='solid',
                                   textvariable=biliname)
        self.bilinameInput.place(relx=0.15, rely=0.1,
                                 relwidth=0.8, relheight=0.3)
        self.bilipwdInput = Entry(self.biliFrame,
                                  width=30,
                                  relief='solid',
                                  show="*",
                                  textvariable=bilipwd)
        self.bilipwdInput.place(relx=0.15, rely=0.6,
                                relwidth=0.8, relheight=0.3)
# 添加按钮，赋予按钮事件

    def save_info(self):
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

    def create_db(self):
        pass

    def addBtn(self):
        ttk.Button(self.tab1, width=8, text='创建数据库',
                   command=self.create_db).place(relx=0.02, rely=0.02, relheight=0.1, relwidth=0.5)
        # 设置的保存按钮
        ttk.Button(self.tab3,
                   width=8,
                   text='保存信息',
                   command=self.save_info).place(relx=0.02, rely=0.86, relheight=0.1, relwidth=0.96)


if __name__ == '__main__':
    app = BiliGui()
