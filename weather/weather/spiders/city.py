import scrapy

from ..items import CityItem


class CitySpider(scrapy.Spider):
    name = 'city'
    allowed_domains = ['weather.com.cn']
    start_urls = ['http://flash.weather.com.cn/wmaps/xml/china.xml']

    def parse(self, response):
        for province in response.xpath('//city'):
            item = CityItem()
            item['province'] = province.xpath('./@quName').extract()[0]
            province_url = province.xpath('./@pyName').extract()[0]
            item['url'] = f"https://flash.weather.com.cn/wmaps/xml/{province_url}.xml"

            self.logger.info(f"parse: {item}")
            yield response.follow(url=item['url'], callback=self.parse_province, meta={'item': item})

    def parse_province(self, response):
        item = response.meta['item']
        for city in response.xpath('//city'):
            item['city'] = city.xpath('./@cityname').extract()[0]
            city_url = city.xpath('./@pyName').extract()[0]
            item['url'] = f"https://flash.weather.com.cn/wmaps/xml/{city_url}.xml"

            self.logger.info(f"parse_province: {item}")
            yield response.follow(url=item['url'], callback=self.parse_city, meta={'item': item})

    def parse_city(self, response):
        item = response.meta['item']
        for district in response.xpath('//city'):
            item['district'] = district.xpath('./@cityname').extract()[0]
            district_url = district.xpath('./@url').extract()[0]
            item['url'] = f"http://www.weather.com.cn/weather1dn/{district_url}.shtml"

            self.logger.info(f"parse_city: {item}")
            yield item
