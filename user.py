from mytool import get_url, jsinfo


class User:
    def __init__(self, uid):
        self.uid = uid
        self.name = None
        self.sex = None
        self.level = None
        self.fanMedia = None
        self.vip = None
        self.official = None
        self.following = None
        self.fans = None

    def back_info(self):
        return (self.uid,
                self.name,
                self.sex,
                self.level,
                self.fanMedia,
                self.vip,
                self.official,
                self.following,
                self.fans)

    def basic_info(self):
        infoUrl = 'https://api.bilibili.com/x/space/acc/info?mid={}'.format(
            self.uid)
        followUrl = 'https://api.bilibili.com/x/relation/stat?vmid={}'.format(
            self.uid)
        info = get_url(infoUrl)
        follow = get_url(followUrl)
        self.name = jsinfo(info, '.data.name')[0]
        self.sex = jsinfo(info, '.data.sex')[0]
        self.level = jsinfo(info, '.data.level')[0]
        if jsinfo(info, '..medal_name'):
            self.fanMedia = jsinfo(info, '..medal_name')[0]
        if jsinfo(info, '.data.vip.label.text') != ['']:
            self.vip = jsinfo(info, '.data.vip.label.text')[0]
        if jsinfo(info, '.data.official.title') != ['']:
            self.official = jsinfo(info, '.data.official.title')[0]
        self.following = jsinfo(follow, '.data.following')[0]
        self.fans = jsinfo(follow, '.data.follower')[0]        

    def up_video(self):
        videoAreaDict = {}
        videoArea_url = 'https://api.bilibili.com/x/space/arc/search?mid={}&ps=30&tid=0&pn=1&order=pubdate'.format(
            self.uid)
        videoArea = get_url(videoArea_url)
        areaName = jsinfo(videoArea, '.data.list.tlist..name')
        areaCount = jsinfo(videoArea, '.data.list.tlist..count')
        count = jsinfo(videoArea, '.data.page.count')
        if count == [0]:
            videoAreaDict['投稿总数'] = 0
        else:
            videoAreaDict = dict(zip(areaName, areaCount))
            videoAreaDict['投稿总数'] = count[0]
        upVideoDict = {self.uid: videoAreaDict}
        return upVideoDict

    def follow_config(self, pn, ps):
        url = 'https://api.bilibili.com/x/relation/followings'
        param = {
            'vmid': self.uid,
            'pn': pn,
            'ps': ps
        }
        resp = get_url(url, param)
        uidlist = jsinfo(resp, '..mid')
        return uidlist

    def follow_list(self):
        follow_list = []
        for i in range(1, 6):
            if not self.follow_config(i, 50):
                continue
            else:
                follow_list += self.follow_config(i, 50)
        return follow_list
