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


class Rank(BaseModel):
    language = CharField(max_length=150)
    position = IntegerField()
    rating = CharField(max_length=150)
    rating_int = IntegerField()
    fetch_date = DateField(default=date.today)
    create_time = DateTimeField(default=datetime.now)


class Content(BaseModel):
    title = CharField(max_length=255)
    description = TextField()
    chart_str = TextField()
    fetch_date = DateField(default=date.today)
    create_time = DateTimeField(default=datetime.now)
    

class Hall(BaseModel):
    year = IntegerField()
    language = CharField()
    fetch_date = DateField(default=date.today)
    create_time = DateTimeField(default=datetime.now)
