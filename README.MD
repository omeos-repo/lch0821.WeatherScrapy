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
scrapy crawl tq
```
结果在`output`目录下。

## 2 项目开发
### 2.1 Scrapy
1. 初始化项目
```sh
scrapy startproject tianqi
cd tianqi
scrapy genspider tq weather.com.cn
```

2. 修改`items.py`
```py
class TianqiItem(scrapy.Item):
    code = scrapy.Field()
    province = scrapy.Field()
    city = scrapy.Field()
    district = scrapy.Field()
    time = scrapy.Field()
    temp = scrapy.Field()
    humi = scrapy.Field()
    maxtemp = scrapy.Field()
    mintemp = scrapy.Field()
    aqi = humi = scrapy.Field()
    wind = scrapy.Field()
    rain = scrapy.Field()
    rain24h = scrapy.Field()
    weather = scrapy.Field()
```

3. 编写爬虫代码：`spiders/city.py`
4. 增加PIPELINE：`pipelines.py`
```py
class JsonWriterPipeline:
    def open_spider(self, spider):
        self.file = open('../output/tianqi.jl', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(ItemAdapter(item).asdict(), ensure_ascii=False) + "\n"
        self.file.write(line)

        return item

```

5. 修改配置：`settings.py`
```py
ITEM_PIPELINES = {
   'tianqi.pipelines.JsonWriterPipeline': 300,
}
```

### 2.2 TDengine
#### 2.2.1 安装
1. 服务端
参考[文档](https://www.taosdata.com/cn/documentation/getting-started#install)安装（如果deb包无法安装可改用代码包）。
2. 客户端
服务端的机器上自带有CLI客户端。另外本项目使用Python客户端是[crown](https://github.com/machine-w/crown)。

#### 2.2.2 数据建模
1. 天气数据
```py
    code = scrapy.Field()
    province = scrapy.Field()
    city = scrapy.Field()
    district = scrapy.Field()
    time = scrapy.Field()
    temp = scrapy.Field()
    humi = scrapy.Field()
    maxtemp = scrapy.Field()
    mintemp = scrapy.Field()
    aqi = scrapy.Field()
    windd = scrapy.Field()
    winds = scrapy.Field()
    rain = scrapy.Field()
    rain24h = scrapy.Field()
    forecast = scrapy.Field()
```

2. 模型
* 超级表：一个超级表，是所有城市天气的集合
* 表：以每个县区为一张表，以`T`+`code`为表名
* 时间戳：`time`
* 采集量：`temp`（温度）、`humi`（湿度）、`maxtemp`（最大温度）、`mintemp`（最小温度）、`aqi`（空气质量）、`windd`（风向）、`winds`（风力）、`rain`（下雨）、`rain24h`（未来24小时下雨）、`forecast`（天气）
* 标签：`code`（编码）、`province`（省）、`city`（市）、`district`（区/县）

3. SQL
```sql
CREATE DATABASE tq KEEP 36500;  -- 保存100年
USE tq;                         -- 切换数据库
CREATE TABLE weather(ts TIMESTAMP, temp INT, humi INT, maxtemp INT, mintemp INT, aqi INT, windd INT, winds INT, rain INT, rain24h INT, forecast INT) TAGS(code BINARY(10), province NCHAR(5), city NCHAR(10), district NCHAR(10));

-- 样例
-- {"code": "101010300", "province": "北京", "city": "北京", "district": "朝阳", "time": "2021-07-02 15:30:00", "temp": 29, "humi": 51, "maxTemp": 999, "minTemp": 999, "aqi": 50, "windD": 4, "windS": 2, "rain": 0, "rain24h": 0, "forecast": 2}
INSERT INTO T101010300 USING weather TAGS("101010300", "北京", "北京", "朝阳") VALUES("2021-07-02 15:30:00", 29, 51, 999, 999, 50, 4, 2, 0, 0, 2);
```

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
