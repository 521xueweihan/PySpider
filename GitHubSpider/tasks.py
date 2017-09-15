#!/usr/bin/env python
# -*- coding:utf-8 -*-
#   
#   Author  :   XueWeiHan
#   Date    :   17/8/30 下午4:47
#   Desc    :
from config import huey # import the huey we instantiated in config.py
from github_spider import get_all_following

# @huey.periodic_task()
# def sub():
#     pass


@huey.task()
def fetch_github():
    pass
