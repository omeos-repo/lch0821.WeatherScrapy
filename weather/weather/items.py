# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CityItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    province = scrapy.Field()
    city = scrapy.Field()
    district = scrapy.Field()
    url = scrapy.Field()


class WeatherItem(scrapy.Item):
    city = scrapy.Field()
    time = scrapy.Field()
    temp = scrapy.Field()
    humi = scrapy.Field()
    maxTemp = scrapy.Field()
    minTemp = scrapy.Field()
    aqi = humi = scrapy.Field()
    wind = scrapy.Field()
