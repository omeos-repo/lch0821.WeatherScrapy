import scrapy
import json

from ..items import TianqiItem


class TqSpider(scrapy.Spider):
    name = 'tq'
    allowed_domains = ['weather.com.cn']
    base_url = 'http://d1.weather.com.cn/sk_2d'
    start_urls = ['https://j.i8tq.com/weather2020/search/city.js']

    def parse(self, response):
        body = response.body.decode(response.encoding)
        body = body.replace("var city_data = ", "")  # 返回里有一串字符，非合法json
        data = json.loads(body)
        provinces = list(data.keys())
        for province in provinces:
            cities = list(data[province].keys())
            for city in cities:
                districts = list(data[province][city].keys())
                for district in districts:
                    print(f"{province}, {city}, {district}")
                    item = TianqiItem()

                    item['code'] = data[province][city][district]['AREAID']
                    item['province'] = province
                    item['city'] = city
                    item['district'] = district

                    next_url = f"{self.base_url}/{item['code']}.html"

                    yield response.follow(url=next_url, callback=self.parse_data, meta={'item': item})

    def parse_data(self, response):
        item = response.meta['item']
        body = response.body.decode(response.encoding)
        body = body.replace("var dataSK=", "")  # 返回里有一串字符，非合法json
        data = json.loads(body)

        # TODO: 全部转成数字，方便存储、查询
        item['time'] = data['time']
        item['temp'] = data['temp']
        item['humi'] = data['sd']
        item['maxTemp'] = 999  # TODO: 暂时缺失，伺机补上
        item['minTemp'] = 999  # TODO: 暂时缺失，伺机补上
        item['aqi'] = data['aqi']
        item['wind'] = data['WD'] + data['WS']
        item['rain'] = data['rain']
        item['rain24h'] = data['rain24h']
        item['weather'] = data['weather']

        self.logger.info(item)
        yield item
