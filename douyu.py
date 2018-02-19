# _*_ coding:utf-8 _*_
import time
import pymongo
from lxml import etree
from selenium import webdriver
"""
    作用：爬取斗鱼直播所有直播间的直播类型以及直播间观看人数
"""
# 连接Mongodb数据库
host = '127.0.0.1'
port = 27017
dbname = 'Douyu'
sheetname = '2018021900douyu'
client = pymongo.MongoClient(host=host,port=port)
mydb = client[dbname]
mysheet = mydb[sheetname]

def start_parse():
    # 打开浏览器
    driver = webdriver.PhantomJS()
    url = 'https://www.douyu.com/directory/all'
    # 发送请求
    driver.get(url)
    # 创建set集合，用于Id的去重
    ids = set()
    # 计数
    num = 0
    while True:
        # 获取页面的源码
        source = driver.page_source
        # 将源码转化为HTML，主要是应用xpath
        html = etree.HTML(source)
        # 找到根节点
        for each in html.xpath('//a[@class="play-list-link"]'):
            # 找到每个直播间的href
            href = each.xpath('./@href')
            lurl = 'https://www.douyu.com'
            source_link = lurl + href[0]
            print source_link
            # 获取每个直播间的ID，为href的最后值
            Id = href[0].split('/')[-1]

            # 获取标题
            title = each.xpath('.//h3[@class="ellipsis"]/text()')
            # 获取直播类型
            types = each.xpath('.//span[@class="tag ellipsis"]/text()')
            if len(types) > 0:
                if len(types[0].split(' ')) > 1:
                    type = types[0].split(' ')[-2]
                else:
                    type = types[0].split(' ')[-1]
            else:
                type = '未知'
            # 获取直播人员的名字
            anchor = each.xpath('.//span[@class="dy-name ellipsis fl"]/text()')
            print anchor[0]
            # 获取观看直播的数量
            numbers = each.xpath('.//span[@class="dy-num fr"]/text()')
            if len(numbers) > 0:
                number = numbers[0]
                if number.isdigit():
                    pass
                else:
                    print number
                    number = (float(number.replace(u'万','')) * 10000 )
            else:
                number = 0
            print '*' * 50


            # 判断Id是否在ids集合里，如果不在我们将它添加到集合中，并将数据存到数据库
            if Id not in ids:
                print '0'
                ids.add(Id)
                data = {

                    'source_link': source_link,
                    'anchor': anchor[0],
                    'id': Id,
                    'title': title[0].strip(),
                    'type': type,
                    'number': number

                }
                mysheet.insert(data)
            else:
                print '1'
        # 判断在源码中是否找到"shark-pager-disable-next"如果没找到将显示-1，如果找到了将直接退出程序
        if source.find("shark-pager-disable-next") != -1:
            break
        # 睡眠3秒，是为了降低对服务器的压力，同时也是为了防止过快导致异常
        time.sleep(3)
        driver.find_element_by_class_name('shark-pager-next').click()
    # 统计有多少人在直播
    for each in ids:
        num += 1
    print num
    # 退出浏览器
    driver.quit()
start_parse()