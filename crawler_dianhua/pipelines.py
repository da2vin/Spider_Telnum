# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import happybase
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class CrawlerDianhuaPipeline(object):
    def process_item(self, item, spider):
        return item


class ConsolePipeline(object):
    def process_item(self, item, spider):
        print json.dumps(dict(item)).decode('unicode-escape')
        return item


class HbasePipline(object):
    def open_spider(self, spider):
        self.connection = happybase.Connection("192.168.2.38", port=9090)
        self.table = self.connection.table('fe_car')

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        dataitem = dict()
        dataitem['attr:mobile'] = item['mobile']
        dataitem['attr:title'] = item['title']
        dataitem['attr:contact_man'] = item['contact_man']
        dataitem['attr:url'] = item['url']
        dataitem['attr:city'] = item['city']
        dataitem['attr:company_name'] = item['company_name']
        dataitem['attr:gather_time'] = item['gather_time']
        dataitem['attr:timeSpan'] = item['timeSpan']
        self.table.put(item['mobile'], dict(dataitem))
        return item


class TextPipline(object):
    def process_item(self, item, spider):
        if item:
            with open('data.txt', 'a') as f:
                f.write(item['city_name'] + ','
                        + item['big_type_name'] + ','
                        + item['type_name'] + ','
                        + item['name'] + ','
                        + item['tel'] + '\n')
            return item
