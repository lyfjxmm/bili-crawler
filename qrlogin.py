import qrcode
from threading import Thread
import time
import requests
from io import BytesIO
import http.cookiejar as cookielib
from PIL import Image
import os
from tkinter import *
from PIL import Image, ImageTk
requests.packages.urllib3.disable_warnings()

headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.56",
           'Referer': "https://www.bilibili.com/"}
headerss = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.56",  'Host': 'passport.bilibili.com',
            'Referer': "https://passport.bilibili.com/login"}


class showpng(Thread):
    def __init__(self, data, frame):
        Thread.__init__(self)
        self.data = data
        self.frame = frame

    def run(self):
        qrimg = Image.open(BytesIO(self.data))
        qrimg1 = ImageTk.PhotoImage(
            qrimg.resize((256, 256), Image.ANTIALIAS))
        qrimage = Label(self.frame, image=qrimg1)
        qrimage.image = qrimg1
        qrimage.pack()


class Qrlogin:
    def __init__(self):
        self.session = None
        self.status = None
        self.oauthKey = None

    def islogin(self, session):
        try:
            session.cookies.load(ignore_discard=True)
        except Exception:
            pass
        loginurl = session.get(
            "https://api.bilibili.com/x/web-interface/nav", verify=False, headers=headers).json()
        if loginurl['code'] == 0:
            print('Cookies值有效，', loginurl['data']['uname'], '，已登录！')
            return session, True
        else:
            print('Cookies值已经失效，请重新扫码登录！')
            return session, False

    def is_cookie_exist(self):
        if not os.path.exists('bzcookies.txt'):
            with open("bzcookies.txt", 'w') as f:
                f.write("")
        self.session = requests.session()
        self.session.cookies = cookielib.LWPCookieJar(filename='bzcookies.txt')
        self.session, self.status = self.islogin(self.session)
        return self.status

    def show_QRcode_img(self, frame):
        self.session = requests.session()
        self.session.cookies = cookielib.LWPCookieJar(filename='bzcookies.txt')
        getlogin = self.session.get(
            'https://passport.bilibili.com/qrcode/getLoginUrl', headers=headers).json()
        loginurl = requests.get(
            getlogin['data']['url'], headers=headers).url
        self.oauthKey = getlogin['data']['oauthKey']
        # print('oauthKey', self.oauthKey)
        # print('session', self.session)
        print('cookie3---', self.session.cookies)
        qr = qrcode.QRCode()
        qr.add_data(loginurl)
        img = qr.make_image()
        a = BytesIO()
        img.save(a, 'png')
        png = a.getvalue()
        a.close()
        t = showpng(png, frame)
        t.start()

    def login(self):
        tokenurl = 'https://passport.bilibili.com/qrcode/getLoginInfo'
        # print('oauthKey', self.oauthKey)
        # print('session', self.session)
        print('cookie4---', self.session.cookies)
        print('cookie4---', self.session.cookies.filename)
        while 1:
            qrcodedata = self.session.post(tokenurl, data={
                'oauthKey': self.oauthKey, 'gourl': 'https://www.bilibili.com/'}, headers=headerss).json()
            print(qrcodedata)
            if '-4' in str(qrcodedata['data']):
                print('二维码未失效，请扫码！')
            elif '-5' in str(qrcodedata['data']):
                print('已扫码，请确认！')
            elif '-2' in str(qrcodedata['data']):
                print('二维码已失效，请重新运行！')
            elif 'True' in str(qrcodedata['status']):
                print('已确认，登入成功！')
                self.session.get(
                    qrcodedata['data']['url'], headers=headers)
                break
            else:
                print('其他：', qrcodedata)
            time.sleep(2)
        self.session.cookies.save()
        return self.session
