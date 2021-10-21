import configparser
from requests import get
from jsonpath import jsonpath


def get_url(url, mode=None):
    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0Win64x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/93.0.4577.82 Safari/537.36 Edg/93.0.961.52 '
    }
    if mode is None:
        json = get(url=url, headers=header).json()
        return json
    else:
        json = get(url, params=mode, headers=header).json()
        return json


def jsinfo(info, rule):
    return jsonpath(info, '${}'.format(rule))


def dict_to_tuple(videodict):
    tempList = [None for _ in range(25)]
    area_dict = {'投稿总数': 0, '动画': 1, '番剧': 2, '国创': 3, '音乐': 4, '舞蹈': 5, '游戏': 6,
                 '知识': 7, '科技': 8, '生活': 9, '美食': 10, '动物圈': 11, '鬼畜': 12, '时尚': 13,
                 '资讯': 14, '娱乐': 15, '影视': 16, 'TV剧': 17, '放映厅': 18, '纪录片': 19, '运动': 20,
                 '汽车': 21, '电视剧': 22, '电影': 23}
    for i in videodict:
        tempList[24] = i
        for j in videodict[i]:
            tempList[area_dict[j]] = videodict[i][j]
    return tuple(tempList)


class biliconfig:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read(
            './config.ini', encoding='utf-8')

        self.host = self.config.get('MySQL', 'host')
        self.user = self.config.get('MySQL', 'user')
        self.password = self.config.get('MySQL', 'password')
        self.port = self.config.getint('MySQL', 'port')

        self.biliname = self.config.get('Bili', 'username')
        self.bilipwd = self.config.get('Bili', 'password')
