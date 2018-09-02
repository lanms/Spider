# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import datetime
import pymongo


class LianjiaspiderPipeline(object):
    def process_item(self, item, spider):
        # 添加时间
        item['create_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%m')
        return item


class LianjiaMongo(object):

    def __init__(self):

        conn = pymongo.MongoClient(host='127.0.0.1', port=27017)
        self.database = conn.lianjia

    def process_item(self, item, spider):
        try:
            # 表名  拼接 city 和 类型  二手房 成交 租房 新房
            collection = self.database[item['city'] + '_' + item['type']]
            collection.update(
                {'house_code': item['house_code']},
                {'$set': dict(item)},
                upsert=True
            )
        except:
            pass
        return item