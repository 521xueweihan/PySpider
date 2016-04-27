# PySpider v2.5
在2.0的基础上，使用2.0获取的代理ip，对这些原始的代理进行可用性测试。之后使用可用的代理，爬取目标URL

## 使用代理的异步爬虫
使用tornado框架中的curl_httpclient，它支持异步和代理

## 运行
- 安装依赖的库：`pip install -r requirements.txt`
- `python spider.py`

## TODO
完善提高可用性和效率
