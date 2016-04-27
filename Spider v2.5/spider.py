#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 
#   Author  :   XueWeiHan
#   E-mail  :   595666367@qq.com
#   Date    :   16/3/31 下午4:21
#   Desc    :   爬虫 v2.5
from bs4 import BeautifulSoup
from tornado.httpclient import HTTPRequest, HTTPClient, HTTPError
from tornado.curl_httpclient import CurlAsyncHTTPClient
from tornado import gen
from tornado.ioloop import IOLoop

try:
    from model import db
    from model import models
    from config import configs
    NO_DB = 1
    # 连接数据库
    db.create_engine(**configs['db'])
except ImportError:
    # NO_DB表示不用数据库
    NO_DB = 0
    print "Can't use db"
from client_config import CLIENT_CONFIG

# 测试用的访问目标（github API）
TEST = 'https://api.github.com/search/users?q=tom+repos:%3E42+followers:%3E1000'

# 测试代理是否可用的URL
TEST_PROXY = 'http://icanhazip.com'

# 获取代理的目标网站
URL = 'http://www.xicidaili.com/nn/'  # 高匿ip
#URL = 'http://www.xicidaili.com/nt/'  # 透明ip


class Spider(object):
    """
    爬
    """
    def __init__(self, url, **kwargs):
        self.request = HTTPRequest(url, **kwargs)

    @gen.coroutine
    def async_get(self, **kwargs):
        """ 异步get """
        ## 注意：只有CurlAsyncHTTPClient支持代理，所以这里用它
        response = yield CurlAsyncHTTPClient().fetch(self.request, **kwargs)
        raise gen.Return(response)

    def get(self, **kwargs):
        """ 同步get """
        return HTTPClient().fetch(self.request, **kwargs)

    def post(self):
        """ post暂时没用，先占坑 """
        self.request.method = "POST"
        return HTTPClient().fetch(self.request)


class Content(object):
    """
    存储(持久化)相关操作
    """
    def __init__(self, model=None):
        self.model = model

    def save(self, save_dict=None):
        """ 存到数据库 """
        if self.model:
            if save_dict:
                data = self.model(**save_dict)
                data.insert()
            else:
                print 'no save_dict'
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


class Proxy(object):
    """
    获取代理ips
    """
    def __init__(self, url, **kwargs):
        self.response = Spider(url, **kwargs).get()

    @gen.coroutine
    def test_proxy(self):
        """ 返回经测试可用的代理 """
        # flag用于计数
        flag = 1
        all_ips = self.ips_info()
        print '初始化爬到{}个代理，下面开始测试这些代理的可用性：'.format(len(all_ips))
        success_proxy = []
        for ip_info in all_ips:
            try:
                s = Spider(TEST_PROXY, headers=CLIENT_CONFIG['headers'],
                           proxy_host=ip_info['proxy_host'], request_timeout=5,
                           proxy_port=int(ip_info['proxy_port']))

                yield s.async_get()
            except Exception:
                print '第{}个，失败。'.format(flag)
                continue
            else:
                print '第{}个：成功！'.format(flag)
                success_proxy.append(ip_info)
            finally:
                flag += 1

        # 返回测试过，可用的代理
        print '经测试：{}个可用，可用率：{}%'.format(len(success_proxy),
                                         len(success_proxy)/len(all_ips))
        raise gen.Return(success_proxy)

    def ips_info(self):
        """ 清理内容得到IP信息 """
        ips_list = []
        html_body = self.response.body
        soup = BeautifulSoup(html_body, "html.parser")
        ip_list_table = soup.find(id='ip_list')
        for fi_ip_info in ip_list_table.find_all('tr'):
            ip_detail = fi_ip_info.find_all('td')
            if ip_detail:
                # 注意：为什么我用list和str方法？否则就是bs4对象！！！
                ips_list.append(dict(proxy_host=str(list(ip_detail)[2].string),
                                     proxy_port=str(list(ip_detail)[3].string)))
        return ips_list


@gen.coroutine
def get_proxy_ips():
    """ 获取代理ips，并存储 """
    try:
        proxy = Proxy(url=URL, headers=CLIENT_CONFIG['headers'])
        ips_list = yield proxy.test_proxy()
    except HTTPError as e:
        print 'Try again! Error info:{}'.format(e)
    else:
        if NO_DB:
            # 存到数据库中
            t = Content(models.Proxy)
            for ip_data in ips_list:
                t.save(ip_data)
        # 默认存到运行运行脚本的目录，文件名：data.txt
        t = Content()
        t.save_to_file(ips_list)
    raise gen.Return(ips_list)


@gen.coroutine
def main():
    """ 使用代理的异步爬虫 """
    flag = 1
    ips_list = yield get_proxy_ips()
    for ip in ips_list:
        while 1:
            print 'Use proxy ip {}:{}'.format(ip['proxy_host'], ip['proxy_port'])
            try:
                # 这里就是异步的代理爬虫，利用代理获取目标网站的信息
                s = Spider(TEST, headers=CLIENT_CONFIG['headers'],
                           proxy_host=ip['proxy_host'], request_timeout=10,
                           proxy_port=int(ip['proxy_port']))

                # response爬虫返回的response对象，response.body就是内容
                response = yield s.async_get()
                print 'NO:{}: status {}'.format(flag, response.code)
            except HTTPError, e:
                print '换代理，错误信息：{}'.format(e)
                break
            else:
                flag += 1

if __name__ == '__main__':
    IOLoop().run_sync(main)