from lxml import etree
from time import sleep
from msedge.selenium_tools import EdgeOptions
from msedge.selenium_tools import Edge
from collections import Counter
import os

# 页面下拉
js = "window.scrollTo(0, document.body.scrollHeight)"
zhuanfalist = []


def downPage(driver):
    driver.execute_script(js)
    sleep(1)
    print('继续加载数据')


def getData(uid):
    if not os.path.exists('B站数据/' + str(uid) + '/dynamic.txt'):
        print('开始获取信息'.center(20, '*'))
        edge_options = EdgeOptions()
        edge_options.use_chromium = True
        edge_options.add_argument('headless')
        driver = Edge(executable_path='./tools/msedgedriver.exe',
                      options=edge_options)
        driver.get('https://space.bilibili.com/' + str(uid) + '/dynamic')
        # 移动到底部,直到没有动态为止
        while 1:
            downPage(driver)
            page_text = driver.page_source
            endText = etree.HTML(page_text).xpath(
                '//*[@class="end-text"]/text()')
            noText = etree.HTML(page_text).xpath(
                '//*[@class="empty-text tc-slate"]/text()')
            if endText or noText:
                break
        # 获取网页源代码，保存到本地
        isUidDirExists = os.path.exists('B站数据/' + str(uid))
        if not isUidDirExists:
            os.makedirs('B站数据/' + str(uid))
        with open('B站数据/' + str(uid) + '/dynamic.txt', 'w', encoding='utf-8') as f:
            f.write(page_text)
        driver.quit()
        print('信息获取完成'.center(20, '*'))
    else:
        print('数据已经存在'.center(20, '*'))


def useLocalData(uid):
    with open('B站数据/' + str(uid) + '/dynamic.txt', 'r', encoding='utf-8') as f:
        txt = f.read()
    return txt


def showDate(date):
    if len(date) < 7:
        date = '2021-' + date
    print(date, end=' : ')


def outTxt(emoji, text):
    if emoji:
        print(text, end='')
        for i in emoji:
            print(i, end='')
        print()
    else:
        print(text)


def dynamicAnalyse(tree):

    info_list = tree.xpath('//*[@class="main-content"]')
    for info in info_list:
        date = info.xpath('div[2]/a/text()')  # 发布日期
        showDate(date[0])
        dynamicType = info.xpath('div[3]/div/@class')[0]  # 动态类型

        # 纯文本动态
        if dynamicType == 'text p-rel description':
            text = info.xpath(
                'div[3]//*[@class="content-full"]')[0].xpath('string(.)').strip()
            emoji = info.xpath('div[3]/div[1]/div/div/img/@alt')  # b站表情
            forward = info.xpath('div[3]/div[2]/@class')  # 是否含有转发
            isExit = info.xpath('div[3]/div[2]/div/@class')[0]  # 转发的原动态是否删除
            if forward:
                outTxt(emoji, text)
                if isExit == 'deleted' or isExit == 'deleted-text':
                    print('\t\t\t*转发的内容已经被删除')
                else:
                    info_tip = info.xpath(
                        'div[3]//*[@class="up-info-tip"]/text()')[0]
                    upName = info.xpath(
                        'div[3]/div[2]/div/div[1]/a[2]/text()')[0]  # 转发的 原UPid
                    zhuanfalist.append(upName)
                    print(
                        '\t\t\t*转发了 * {name} * {info}* '.format(name=upName, info=info_tip), end='')
                    if '图片' in info_tip:
                        forwardText = info.xpath(
                            'div[3]/div[2]/div/div[2]/div/div[1]')[0].xpath('string(.)').strip()
                    elif '投稿视频' in info_tip:
                        forwardText = info.xpath(
                            'div[3]//*[@class="title"]')[0].xpath('string(.)').strip()
                    elif '文章' in info_tip:
                        forwardText = info.xpath(
                            'div[3]//*[@class="title"]')[0].xpath('string(.)').strip()
                    elif '动态' in info_tip:
                        forwardText = info.xpath(
                            'div[3]/div[2]/div/div[2]/div/div[1]')[0].xpath('string(.)').strip()
                    else:
                        forwardText = '未知'
                    print(forwardText)

        # 带图片的动态，或者是投稿视频
        elif dynamicType == 'post-content':
            isVideo = info.xpath('div[3]/div[1]/div/div/a/div/@class')  # 是否为视频
            isDress = info.xpath('div[3]/div[1]/div/div[2]/@class')

            if isVideo and isVideo[0]:
                videoName = info.xpath(
                    'div[3]//*[@class="title"]')[0].xpath('string(.)').strip()
                print('投稿了:', videoName)

            elif isDress and isDress[0] == 'h5share-container bg-white pointer t-left':
                dressName = info.xpath('div[3]/div[1]/div/div[2]/a/div/div[2]/div[1]/div')[0].xpath(
                    'string(.)').strip()
                text = info.xpath(
                    'div[3]/div[1]/div/div[1]/div/div')[0].xpath('string(.)').strip()
                print(text, '* 小卡片 *:', dressName)
            else:
                text = info.xpath(
                    'div[3]/div[1]/div/div[1]/div/div')[0].xpath('string(.)').strip()
                emoji = info.xpath(
                    'div[3]/div[1]/div/div[1]/div/div/img/@alt')  # b站表情
                outTxt(emoji, text)

        else:
            print('未知的动态类型')


def tagAnalyse(tree):
    # 成分统计
    print('成分分析'.center(20, '*'))
    #  #文本# 出现率TOP5
    keywordlist = tree.xpath('//*[@class="dynamic-link-hover-bg"]/text()')
    taglist = Counter([i for i in keywordlist if '#' in i])
    top5list = taglist.most_common(5)
    print('动态中包含tag Top5：')
    for i in top5list:
        print('\t{tag}总共出现：{time}次'.format(tag=i[0], time=i[1]))
    # 最常转发UP主
    top5Zfup = Counter(zhuanfalist).most_common(5)
    print('最常转发up主Top5')
    for i in top5Zfup:
        print('\t{tag}总共出现：{time}次'.format(tag=i[0], time=i[1]))
    # 看看抽奖
    drawlist = [i for i in keywordlist if 'u200b互动抽奖' in repr(i)]
    print('一共参与互动抽奖:', len(drawlist), '次')


if __name__ == '__main__':
    uid = 11502545
    getData(uid)
    tree = etree.HTML(useLocalData(uid))
    dynamicAnalyse(tree)

    # 看看成分
    tagAnalyse(tree)
