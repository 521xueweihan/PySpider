#!/usr/bin/env python
# -*- coding:utf-8 -*-
#   
#   Author  :   XueWeiHan
#   Date    :   17/8/30 下午4:48
#   Desc    :   入口

# main.py
from gevent import monkey
monkey.patch_all()

from config import huey  # import our "huey" object
from tasks import sub, count  # import our task


if __name__ == '__main__':
    huey.flush()
    for i in range(100):
        sub()
