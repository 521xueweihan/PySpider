#!/usr/bin/env python
# -*- coding:utf-8 -*-
#   
#   Author  :   XueWeiHan
#   Date    :   17/8/30 下午5:58
#   Desc    :   base spider
import os
import logging

import requests


class BaseSpider(object):
    spider_name = 'base'
    
    def __init__(self):
        logging.getLogger("requests").setLevel(logging.WARNING)
        logging.getLogger("urllib3").setLevel(logging.WARNING)
        logging.basicConfig(
            level=logging.INFO,
            filename=os.path.join(os.path.dirname(__file__),
                                  '{name}.txt'.format(name=self.spider_name)),
            filemode='a',
            format='%(name)s %(asctime)s %(filename)s[line:%(lineno)d] '
                   '%(levelname)s %(message)s')
        self.logger = logging.getLogger(self.spider_name)  # 设置log名称
    
    def get_data(self, url):
        try:
            response = requests.get(url, timeout=20)
            return response
        except Exception as e:
            self.logger.error(u"获取 {url} 数据失败：{e}".format(url=url, e=e))
            return None
