#!/usr/bin/env python
# -*- coding:utf-8 -*-
#   
#   Author  :   XueWeiHan
#   Date    :   17/7/19 下午3:19
#   Desc    :   github 爬虫
# API https://developer.github.com/v3/
# User https://api.github.com/users/521xueweihan
#
from gevent import monkey
monkey.patch_all()


import re
import time
from gevent.pool import Pool
from functools import wraps
from datetime import datetime

import redis
import requests
from requests.exceptions import ProxyError, ConnectionError, Timeout
from peewee import DoesNotExist, IntegrityError

from github_model import User, Proxy

# for debug to disable insecureWarning
requests.packages.urllib3.disable_warnings()

conn = redis.Redis(host='127.0.0.1', port=6379)

class LimitError(Exception):
    pass


def save_users_info(info):
    pass
  
  
def save_users(ids, names):
    conn.rpush('user.id', *ids)
    conn.rpush('user.name', *names)


def get_all_user_id():
    return conn.lrange('user.id', 0, conn.llen('user.id'))
    
    
def get_all_user_name():
    return conn.lrange('user.name', 0, conn.llen('user.name'))
    

def fetch_proxies():
    with open('/Users/xueweihan/Documents/github_project/proxyspider/proxy_list.txt', 'r+') as fb:
        for line in fb.readlines()[1:]:
            try:
                Proxy.create(url=line.split('  ')[0])
            except IntegrityError:
                continue


def get_proxy():
    try:
        proxy_obj = Proxy.get(Proxy.status == 1,
                              (Proxy.reset_time.is_null()) |
                              (Proxy.reset_time < datetime.now()))
        proxy_url = proxy_obj.url
    except DoesNotExist:
        proxy_url = None
    return proxy_url


def make_params(url, proxy_url):
    params = {
        'url': url,
        'verify': False,
        'timeout': 20,
    }
    if not check_per_page(url):
        params['params'] = {'per_page': 100}
    if not proxy_url:
        return params
    proxies_dict = {}
    proxy_url = "http://{}".format(proxy_url)
    proxies_dict['http'] = proxy_url
    proxies_dict['https'] = proxy_url
    params['proxies'] = proxies_dict
    return params


def proxy(fn):
    @wraps(fn)
    def wrap(*args):
        while 1:
            proxy_url = get_proxy()
            try:
                return fn(*args, proxy_url=proxy_url)
            except (ProxyError, Timeout, ConnectionError):
                print 'ProxyError'
                Proxy.update(status=0, update_time=datetime.now()).where(Proxy.url == proxy_url).execute()
            except LimitError as e:
                Proxy.update(reset_time=datetime.fromtimestamp((int(time.time()) + 60*60)), update_time=datetime.now()).where(Proxy.url == proxy_url).execute()
            except Exception as e:
                print 'unknow error'
                Proxy.update(status=0, update_time=datetime.now()).where(Proxy.url == proxy_url).execute()

    return wrap


@proxy
def get_data(url, proxy_url=''):
    params = make_params(url, proxy_url)
    response = requests.get(**params)
    print proxy_url, response.status_code, response.url
    if response.status_code == 403:
        reset_datetime = check_limit(response.headers)
        if reset_datetime:
            if proxy_url is None:
                sleep_seconds = (reset_datetime - datetime.now()).total_seconds()
                print 'sleep:', sleep_seconds
                time.sleep(sleep_seconds)
            else:
                print 'reset_second: ', reset_datetime
                Proxy.update(reset_time=reset_datetime,
                             update_time=datetime.now())\
                     .where(Proxy.url == proxy_url).execute()
                raise LimitError
    elif response.status_code == 200:
        return response


def check_per_page(url):
    urlparse_obj = requests.utils.urlparse(url)
    if 'per_page' in urlparse_obj.query:
        return True
    else:
        return False


def check_limit(headers):
    """
    :return: datetime
    """
    remaining = int(headers.get('X-RateLimit-Remaining'))
    if not remaining:
        reset_time = datetime.fromtimestamp(int(headers.get('X-RateLimit-Reset')))
        return reset_time
    return None


def next_page_url(headers):
    link_params = headers.get('Link')
    pattern = re.compile(
        r'<https://api\.github\.com/.*>; rel="next"')
    if not link_params:
        return None
    else:
        s = re.search(pattern, link_params)
        if not s:
            return None
        else:
            return s.group().split(';')[0][1:-1]


def fetch_user(url):
    response = get_data(url)

    ids = []
    names = []
    for item in response.json()['items']:
        ids.append(item.get('id'))
        names.append(item.get('login'))
    save_users(ids, names)
    return next_page_url(response.headers)


def fetch_all_user():
    url = 'https://api.github.com/search/users?q=location:china&sort=followers'
    next_url = fetch_user(url)
    while next_url:
        next_url = fetch_user(next_url)
        
        
def fetch_user_info(name):
    url = 'https://api.github.com/users/{}'.format(name)
    response = get_data(url)
    json_data = response.json()
    
    result_dict = {
        'uuid': json_data.get('id'),
        'name': json_data.get('login'),
        'nickname': json_data.get('name') or json_data.get('login'),
        'avatar_url': json_data.get('avatar_url'),
        'html_url': json_data.get('html_url'),
        'public_repos': int(json_data.get('public_repos', 0)),
        'followers': int(json_data.get('followers', 0)),
        'location': json_data.get('location'),
        'email': json_data.get('email'),
    }
    User.get_or_create(**result_dict)
    
    
    
# fetch_proxies()
# fetch_all_user()
#

# all user
all_users_name = get_all_user_name()
pool = Pool(20)

username_list = []
for user_name in all_users_name:
    try:
        User.get(User.name==user_name)
    except DoesNotExist:
        username_list.append(user_name)

pool.map(fetch_user_info, username_list)
