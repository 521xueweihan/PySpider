#!/usr/bin/env python
# -*- coding:utf-8 -*-
#   
#   Author  :   XueWeiHan
#   Date    :   17/8/30 下午4:40
#   Desc    :   配置
from huey import RedisHuey

huey = RedisHuey()

DATABASE_URL = 'mysql://root:@127.0.0.1:3306/github?charset=utf8mb4'