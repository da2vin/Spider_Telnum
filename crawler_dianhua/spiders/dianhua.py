# -*- coding: utf-8 -*-
import scrapy
import json
import re
from scrapy_redis.spiders import RedisCrawlSpider
import random
from crawler_dianhua.damatuWeb import dmt
import threading
import urllib





class sigl:
    mutex = threading.Lock()
    isdama = False


# class DianhuaSpider(RedisCrawlSpider):
class DianhuaSpider(scrapy.Spider):
    # handle_httpstatus_list = [401]
    name = "dianhua"
    allowed_domains = ["dianhua.cn"]
    start_urls = (
        'http://www.dianhua.cn/meishan/c428/p2',
    )

    # redis_key = 'dianhua:start_urls'

    # def read_captcha(self, response):
    #     sigl.mutex.acquire(20)
    #     result = dmt.decode(response.body, 200).lower()
    #     request = scrapy.Request(
    #             url='http://www.dianhua.cn/auth/code.php?code=' + urllib.quote(result.encode('utf-8', 'replace')),
    #             dont_filter=True,
    #             headers={
    #                 "Referer": response.request.meta["re_url"],
    #             },
    #             priority=999999
    #     )
    #     request.meta["has_dama"] = True
    #     yield request

    def parse(self, response):
        # if 'has_dama' in response.request.meta:
        #     if 'captcha.php' not in response.request.url:
        #         sigl.isdama = False
        #         sigl.mutex.release()
        # if response.status == 401:
        #     if sigl.isdama:
        #         yield scrapy.Request(
        #                 url=response.request.url
        #         )
        #     else:
        #         sigl.isdama = True
        #         request = scrapy.Request(
        #                 url='http://www.dianhua.cn/auth/captcha.php?r=' + str(random.random()),
        #                 callback=self.read_captcha,
        #                 priority=999998
        #         )
        #         request.meta["re_url"] = response.request.url
        #         yield request
        # elif 'captcha.php' in response.request.url:
        #     sigl.mutex.acquire(20)
        #     sigl.isdama = True
        #     result = dmt.decode(response.body, 200).lower()
        #     request = scrapy.Request(
        #             url='http://www.dianhua.cn/auth/code.php?code=' + urllib.quote(result.encode('utf-8', 'replace')),
        #             dont_filter=True,
        #     )
        #     request.meta["re_url"] = response.request.meta["re_url"],
        #     request.meta["has_dama"] = True
        #     yield request
        if 'life' in response.request.url:
            big_type_list = response.css('div.meun_box > div')
            for x in big_type_list:
                big_type_name = x.css('li.m_z2_zt a::text').extract_first()
                type_list = x.css('div.m_b_meun a')
                for t in type_list:
                    type_name = t.css('::text').extract_first()
                    type_href = 'http://www.dianhua.cn' + t.css('::attr(href)').extract_first()

                    request = scrapy.Request(
                            url=type_href,
                    )
                    request.meta["city_name"] = response.request.meta["city_name"]
                    request.meta["type_name"] = type_name
                    request.meta["big_type_name"] = big_type_name
                    yield request
        else:
            if len(response.xpath(u'//a[contains(text(),\'下一页\')]')) > 0:
                url = "http://www.dianhua.cn" + response.xpath(u'//a[contains(text(),\'下一页\')]').css(
                        "::attr(href)").extract_first()
                request = scrapy.Request(
                        url=url,
                )
                request.meta["city_name"] = response.request.meta["city_name"]
                request.meta["type_name"] = response.request.meta["type_name"]
                request.meta["big_type_name"] = response.request.meta["big_type_name"]
                yield request
            list = response.css('div.c_right_body div.c_right_list')
            for l in list:
                data = dict()
                temp = l.css('dt')[0]
                data['name'] = temp.css('h5 a::text').extract_first()
                data['tel'] = temp.css('div.tel_list p::text').extract_first()
                data['city_name'] = response.request.meta['city_name']
                data['type_name'] = response.request.meta['type_name']
                data['big_type_name'] = response.request.meta['big_type_name']
                print json.dumps(data).decode('unicode-escape')
                yield data

    def start_requests(self):
        with open('crawler_dianhua\spiders\city_list', 'r') as f:
            city_text = f.read()
        city_json = json.loads(city_text)
        sc_city = [x for x in dict(city_json).values() if x['pro_id'] == '23']
        for x in sc_city:
            request = scrapy.Request(
                    url='http://www.dianhua.cn/%s/life' % (x['city_en'].lower(),),
                    dont_filter=True,
            )
            request.meta["city_name"] = x["city_name"]
            yield request
