from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from mytool import jsinfo
from requests import get
from lxml import etree
from rich.progress import track
from time import sleep
import re

ACCOUNT = '17868388536'
PASSWORD = 'jixianmaimeng1'


class BrowsDriver:
    def __init__(self):
        self.username = ACCOUNT
        self.password = PASSWORD
        self.driver = webdriver.Edge(executable_path='./tools/msedgedriver.exe')
        self.url = 'https://space.bilibili.com/'
        self.wait = WebDriverWait(self.driver, 10)
        self.cookie = ''
    
    # 进行一个B的登录
    def login_bili(self):
        self.driver.get(self.url)
        self.wait.until(
            EC.presence_of_element_located((By.ID, 'login-username')))
        self.wait.until(
            EC.presence_of_element_located((By.ID, 'login-passwd')))

        self.driver.find_element_by_id(
            "login-username").send_keys(self.username)
        self.driver.find_element_by_id(
            "login-passwd").send_keys(self.password)
        submit = self.wait.until(EC.element_to_be_clickable(
            (By.CLASS_NAME, 'btn-login')))
        submit.click()
        sleep(7)
    # 得到cookie
    def get_cookie(self):
        cookie_items = self.driver.get_cookies()
        self.cookie = ''
        # 组装cookie字符串
        for item_cookie in cookie_items:
            item_str = item_cookie["name"]+"="+item_cookie["value"]+"; "
            self.cookie += item_str
    # 请求API的方法
    def get_view_info(self, uidlist):
        viewList = []
        header = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0Win64x64) AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/93.0.4577.82 Safari/537.36 Edg/93.0.961.52 ',
            'cookie': self.cookie
        }
        for i in track(uidlist, description='获取播放量信息中'):
            infoUrl = 'https://api.bilibili.com/x/space/upstat?mid={}'.format(
                i)
            viewinfo = get(url=infoUrl, headers=header).json()
            likes = jsinfo(viewinfo, '..likes')
            videoView = jsinfo(viewinfo, '.data.archive.view')
            readView = jsinfo(viewinfo, '.data.article.view')
            upViewInfo = (likes, videoView, readView, i)
            viewList.append(upViewInfo)
            sleep(1)
        return viewList
    # 用selenium，很快啊
    def open_up_space(self, uidlist):
        upViews = []
        for i in track(uidlist, description='获取UP主播放信息中'):
            self.driver.get('https://space.bilibili.com/{}'.format(i))
            self.wait.until(
                EC.presence_of_element_located((By.ID, 'n-bf')))
            self.wait.until(
                EC.presence_of_element_located((By.ID, 'navigator')))
            page_text = self.driver.page_source
            tree = etree.HTML(page_text)
            views = tree.xpath(
                '//*[@id="navigator"]/div/div[1]/div[3]/div/@title')
            views = [re.findall(r'[\d,]+', each)[0] for each in views]
            views = [int(re.sub(r',', '', str(each))) for each in views]
            if len(views) > 3:
                views.pop(0)
            if len(views) < 3:
                print('出错：uid为{}信息获取失败'.format(i))
            else:
                views.append(i)
                upViews.append(tuple(views))
        self.driver.quit()
        return upViews

    def close_driver(self):
        self.driver.quit()
