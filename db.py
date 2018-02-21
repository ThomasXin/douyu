# _*_ coding:utf-8 _*_

import pymongo
import time
from lxml import etree

from selenium import webdriver
host = 'localhost'
port = 27017
client = pymongo.MongoClient(host=host, port=port)
dbname = 'Douyu'
sheetname = 'douyu'
# sinatvsheet = 'douyusinatv'
mydb = client[dbname]
mysheet = mydb[sheetname]
# mysinatv = mydb[sinatvsheet]
driver = webdriver.PhantomJS()
number = 0
for i in mysheet.find():
    link = i['source_link']
    print link
    number += 1
    # mysheet.update({'_id': i['_id']}, {'$set': {'state': -1, 'times': 0}})
# print number
    driver.get(link)
    source = driver.page_source

    if source.find('time-v-con') == -1:
        html = etree.HTML(source)
        for each in html.xpath('//div[@class="relate-text fl"]'):
            titles = each.xpath('.//h2/text()')
            if len(titles) > 0:

                title = titles[0]
                # print title.encode('utf-8')
                data = {

                    'source_link': i['source_link'],
                    'id': i['id'],
                    'title': title,
                    'type': i['type'],
                    'state': 0,
                    'times': 0,
                }
                mysheet.update({'_id': i['_id']}, {'$set': {'state': 0, 'title': title}})
    else:
        mysheet.update({'_id': i['_id']}, {'$set': {'times': i['times'] + 1}})
#     time.sleep(1)
    # print driver.find_element_by_class_name('time-v-con')