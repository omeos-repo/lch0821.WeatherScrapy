# 中国天气网爬虫
[toc]

## 1 快速开始
### 1.1 配置环境
1. 安装`Python3`
2. 安装`scrapy`
```sh
pip install scrapy
```
也可以直接通过`requirement`文件安装：
```sh
pip install -r requirements.txt
```

### 1.2 运行
```sh
scrapy crawl city
```
结果在`output`目录下。

### 2 项目开发
1. 初始化项目
```sh
scrapy startproject weather
scrapy genspider city weather.com.cn
```

2. 修改`items.py`
3. 编写爬虫代码：`spiders/city.py`
4. 增加PIPELINE：`pipelines.py`
5. 修改配置：`settings.py`

## 3 Debug
### `response.follow`不执行`callback`
1. 回调函数未完成
```py
    def parse(self, response):
        for item in response.xpath('//city'):
            items = CityItem()
            # ...
            yield response.follow(url=items['url'], callback=self.parse_page, meta={'items': items})

    def parse_page(self, response):
        items = response.meta['items']
        # 这种情况下不执行，需要添加返回
        # yield ...
```

2. `allowed_domains`配置错误
```ini
allowed_domains = ['www.weather.com.cn']
# flash.weather.com.cn 域名无法访问，所以不会执行，改为：
allowed_domains = ['weather.com.cn']
```

## 4 参考
* [Scrapy 2.5 documentation](https://docs.scrapy.org/en/latest/index.html)
* [Scrapy with selenium](https://github.com/clemfromspace/scrapy-selenium)
* [http://flash.weather.com.cn/wmaps/xml/china.xml](http://flash.weather.com.cn/wmaps/xml/china.xml)
* [https://flash.weather.com.cn/wmaps/xml/qiqihaer.xml](https://flash.weather.com.cn/wmaps/xml/qiqihaer.xml)
* [http://www.weather.com.cn/weather1dn/101280905.shtml](http://www.weather.com.cn/weather1dn/101280905.shtml)
