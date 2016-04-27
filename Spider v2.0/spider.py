#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   XueWeiHan
#   E-mail  :   595666367@qq.com
#   Date    :   16/3/31 下午4:21
#   Desc    :   爬虫
from tornado.httpclient import HTTPRequest, AsyncHTTPClient, HTTPClient

#from model import db
#from config import configs
from client_config import CLIENT_CONFIG

# 连接数据库
#db.create_engine(**configs['db'])


class Spider(object):
    """
    爬
    """
    def __init__(self, url, **kwargs):
        self.request = HTTPRequest(url, **dict(CLIENT_CONFIG, **kwargs))

    def get(self, **kwargs):
        ## TODO 下一步用写异步的爬虫提高效率
        return HTTPClient().fetch(self.request, **kwargs)

    def post(self):
        self.request.method = "POST"
        return HTTPClient().fetch(self.request)


class Content(object):
    """
    存储内容到数据库
    """
    def __init__(self, model=None):
        self.model = model

    def save(self, kwargs):
        if self.model:
            data = self.model(**kwargs)
            data.insert()
        else:
            print 'no model'

    @staticmethod
    def save_to_file(all_content, str_split=':', path='./data.txt'):
        """
        把数据存到文件中
        :param all_content: 需要是list类型
        :param str_split: 分割符号
        :param path: 文件位置，默认为当前脚本运行的位置，文件名：data.txt
        """
        with open(path, 'w') as fb:
            print '开始写入文件'
            for content in all_content:
                content_str = ''
                for k, v in content.items():
                    content_str += v + str_split
                fb.write(content_str+'\n')
            print '写入文件完成'
