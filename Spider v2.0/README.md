# PySpider v2.0

## 爬取代理ip
起因：我这次是准备爬取‘高匿的ip’，做一个ip库，方便后面的爬虫。这是因为，很多网站或者api接口，都设置了‘访问间隔时间’（一个ip有访问次数的限制，超过次数就需要进入‘冷却CD’）。所以，用我的真实ip，无法高效、快速的爬取内容。

因为工作中使用tornado框架，它带一个很好用的HTTPClient的库，所以这次我就直接用它来完成，爬代理ip的工作。

## 运行
- 安装依赖的库：`pip install -r requirements.txt`
- `python get_proxy.py`

## TODO
升级成异步的爬虫。
