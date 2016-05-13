#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   XueWeiHan
#   E-mail  :   595666367@qq.com
#   Date    :   16/4/23 上午10:40
#   Desc    :   爬代理
from bs4 import BeautifulSoup

from spider import Spider, Content
#from model.models import Ip


def get_ip_info(html_response):
    """ 清理内容得到IP信息 """
    ips_list = []
    soup = BeautifulSoup(html_response.body, "html.parser")
    ip_list_table = soup.find(id='ip_list')
    for ip_info in ip_list_table.find_all('tr'):
        ip_detail = ip_info.find_all('td')
        if ip_detail:
            # 注意：为什么我用list和str方法？否则就是bs4对象！！！
            ips_list.append(dict(ip=str(list(ip_detail)[1].string),
                                 port=str(list(ip_detail)[2].string)))
    return ips_list

s = Spider('http://www.xicidaili.com/nn/')
response = s.get()
ips = get_ip_info(response)


# 默认存到运行运行脚本的目录，文件名：data.txt
Content().save_to_file(ips)

# 存到数据库
#t = Content(Ip)
# for ip_data in ips:
#     t.save(ip_data)
