# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


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
    aqi = scrapy.Field()
    windd = scrapy.Field()
    winds = scrapy.Field()
    rain = scrapy.Field()
    rain24h = scrapy.Field()
    forecast = scrapy.Field()
