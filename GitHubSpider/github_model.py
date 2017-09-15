#!/usr/bin/env python
# -*- coding:utf-8 -*-
#   
#   Author  :   XueWeiHan
#   Date    :   17/8/30 下午5:33
#   Desc    :   Model
from datetime import datetime, date

from peewee import Model
from playhouse.db_url import connect
from peewee import CharField, TextField, DateTimeField, IntegerField, DateField

from config import DATABASE_URL

database = connect(DATABASE_URL)


class BaseModel(Model):
    class Meta:
        database = database


class User(BaseModel):
    uuid = CharField(max_length=150)
    name = CharField(max_length=255)
    nickname = CharField(max_length=255)
    avatar_url = CharField(max_length=255)
    html_url = CharField(max_length=255)
    public_repos = IntegerField()
    followers = IntegerField()
    stars_count = IntegerField(default=0)
    location = CharField(max_length=255)
    email = CharField(max_length=255, null=True)
    create_time = DateTimeField(default=datetime.now)
    update_time = DateTimeField(default=datetime.now)


class Proxy(BaseModel):
    url = CharField(max_length=150, unique=True)
    status = IntegerField(default=1)
    create_time = DateTimeField(default=datetime.now)
    update_time = DateTimeField(default=datetime.now)
    reset_time = DateTimeField(null=True, default=None)
    
database.create_tables([User, Proxy], safe=True)