from lxml import etree
from time import sleep
from matplotlib.pyplot import draw
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
            noMoreText = etree.HTML(page_text).xpath(
                '//*[@class="bili-dyn-list-no-more"]/text()'
            )
            if endText or noText or noMoreText:
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
    date = date.replace(' ', '')
    date = date.replace('·', ' : ')
    if date[0] != '2':
        date = '2022-' + date

    print(date, end=' : ')


def dynamicAnalyse(tree):

    info_list = tree.xpath('//*[@class="bili-dyn-item__main"]')  # 动态列表

    for info in info_list:

        date = info.xpath('div[2]/div[2]/text()')[0].replace('\n', '')  # 发布日期
        showDate(date)
        dynType = info.xpath('div[3]/div/div/@class')  # 动态内容列表
        for t in dynType:
            if t == 'bili-dyn-content__orig':
                if info.xpath('div[3]/div[1]/div/div[1]/div/div[1]') != []:
                    print(info.xpath(
                        'div[3]/div[1]/div/div[1]/div/div[1]')[0].xpath('string(.)').strip().replace('\n', ''), end='')
                elif '文章' in date:
                    print(info.xpath(
                        'div[3]/div[1]/div/div/a/div[2]/div[1]/text()')[0], end='')
                pass
            elif t == 'bili-dyn-content__forw__desc':
                print(info.xpath(
                    'div[3]/div/div[1]/div/div')[0].xpath('string(.)').strip(), end='')
                pass
            elif t == 'bili-dyn-content__orig reference':
                print('\t  *  转发了  ', end='')
                if info.xpath('div[3]/div/div[2]/div[1]/div/div[1]/span/text()') != []:
                    upName = info.xpath(
                        'div[3]/div/div[2]/div[1]/div/div[1]/span/text()')[0]
                    upName = upName.replace(' ', '')
                    upName = upName.replace('\n', '')
                    zhuanfalist.append(upName)
                    print(' * ' + upName+' * ', end='')
                else:
                    print('原动态已被删除', end='')
                if info.xpath('div[3]/div/div[2]/div[2]/div/div[1]') != []:
                    print(info.xpath('div[3]/div/div[2]/div[2]/div/div[1]')
                          [0].xpath('string(.)').replace('\n', '').strip(), end='')
                pass
            else:
                pass
            if '视频' in date:
                print(info.xpath(
                    'div[3]/div[1]/div/div/a/div[2]/div[1]')[0].xpath('string(.)').strip(), end='')
        print()


def tagAnalyse(tree):
    # 成分统计
    print('成分分析'.center(20, '*'))
    #  #文本# 出现率TOP5
    keywordlist = tree.xpath('//*[@class="bili-rich-text-topic"]/text()')
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
    drawList = len(tree.xpath('//*[@data-type="lottery"]'))
    print('一共参与动态抽奖'+str(drawList)+'次')


# if __name__ == '__main__':
#     uid = 5239084
#     getData(uid)
#     tree = etree.HTML(useLocalData(uid))
#     dynamicAnalyse(tree)

#     # 看看成分
#     tagAnalyse(tree)
