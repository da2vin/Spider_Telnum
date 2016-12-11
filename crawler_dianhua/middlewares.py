#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf8')

class ProxyMiddleWare(object):
    def process_request(self, request, spider):
        request.meta['proxy'] = "http://localhost:8888"