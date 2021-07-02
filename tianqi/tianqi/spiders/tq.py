import re
import json
import scrapy
from datetime import datetime, timedelta

from ..items import TianqiItem


class TqSpider(scrapy.Spider):
    name = 'tq'
    allowed_domains = ['weather.com.cn']
    now = datetime.now()
    base_url = 'http://d1.weather.com.cn/sk_2d'
    start_urls = ['https://j.i8tq.com/weather2020/search/city.js']
    wind_direction = {"无持续风向": 0, "东北风": 1, "东风": 2, "东南风": 3, "南风": 4,
                      "西南风": 5, "西风": 6, "西北风": 7, "北风": 8, "旋转风": 9}

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
        body = re.findall(r'var dataSK.+({.*})', body)[0]  # 返回里有一串字符(var dataSK)，非合法json
        data = json.loads(body)

        year = str(self.now.year)
        month, day = re.findall(r'(\d\d).+(\d\d)', data['date'])[0]
        dt_string = f"{year}-{month}-{day} {data['time']}"  # yyyy-mm-dd hh:mm
        dt = datetime.strptime(dt_string, "%Y-%m-%d %H:%M")

        if dt - self.now > timedelta(days=1):  # 只有当跨年才会出现这种情况
            dt = dt - timedelta(years=1)

        item['time'] = str(dt)
        item['temp'] = int(data['temp'])
        item['humi'] = int(data['sd'].replace("%", ""))
        item['maxTemp'] = 999  # TODO: 暂时缺失，伺机补上
        item['minTemp'] = 999  # TODO: 暂时缺失，伺机补上
        item['aqi'] = int(data['aqi']) if data['aqi'] else 0
        item['windD'] = self.wind_direction.get(data['WD'])
        item['windS'] = int(data['WS'].replace("级", ""))
        item['rain'] = round(float(data['rain']))
        item['rain24h'] = round(float(data['rain24h']))
        item['weather'] = int(re.findall(r'\d+', data['weathercode'])[0])

        yield item


"""
风向编码：
{"无持续风向": 0, "东北风": 1, "东风": 2, "东南风": 3, "南风": 4, "西南风": 5, "西风": 6, "西北风": 7, "北风": 8, "旋转风": 9}

天气气象编码
{
    0: "晴",
    1: "多云",
    2: "阴",
    3: "阵雨",
    4: "雷阵雨",
    5: "雷阵雨伴有冰雹",
    6: "雨夹雪",
    7: "小雨",
    8: "中雨",
    9: "大雨",
    10: "暴雨",
    11: "大暴雨",
    12: "特大暴雨",
    13: "阵雪",
    14: "小雪",
    15: "中雪",
    16: "大雪",
    17: "暴雪",
    18: "雾",
    19: "冻雨",
    20: "沙尘暴",
    21: "小到中雨",
    22: "中到大雨",
    23: "大到暴雨",
    24: "暴雨到大暴雨",
    25: "大暴雨到特大暴雨",
    26: "小到中雪",
    27: "中到大雪",
    28: "大到暴雪",
    29: "浮尘",
    30: "扬沙",
    31: "强沙尘暴",
    53: "霾",
    99: "无",
    32: "浓雾",
    49: "强浓雾",
    54: "中度霾",
    55: "重度霾",
    56: "严重霾",
    57: "大雾",
    58: "特强浓雾",
    97: "雨",
    98: "雪",
    301: "雨",
    302: "雪"
}
"""
