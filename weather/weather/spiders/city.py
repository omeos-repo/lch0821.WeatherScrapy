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
            province_py = province.xpath('./@pyName').extract()[0]
            next_url = f"https://flash.weather.com.cn/wmaps/xml/{province_py}.xml"

            self.logger.info(f"parse: {item['province']}: {next_url}")
            yield response.follow(url=next_url, callback=self.parse_province, meta={'item': item})

    def parse_province(self, response):
        province = response.meta['item']['province']
        for city in response.xpath('//city'):
            item = CityItem()
            item['province'] = province
            item['city'] = city.xpath('./@cityname').extract()[0]
            city_url = city.xpath('./@url').extract()[0]
            item['url'] = f"http://www.weather.com.cn/weather1dn/{city_url}.shtml"

            city_py = city.xpath('./@pyName').extract()[0]
            next_url = f"https://flash.weather.com.cn/wmaps/xml/{city_py}.xml"

            self.logger.info(f"parse_province: {item}")
            yield response.follow(url=next_url, callback=self.parse_city, meta={'item': item})

    def parse_city(self, response):
        city_item = response.meta['item']
        city_item['district'] = city_item['city']  # 市区，用城市填充，方便后续查询
        yield city_item

        province = city_item['province']
        city = city_item['city']
        for district in response.xpath('//city'):
            item = CityItem()
            item['province'] = province
            item['city'] = city
            item['district'] = district.xpath('./@cityname').extract()[0]
            district_url = district.xpath('./@url').extract()[0]
            item['url'] = f"http://www.weather.com.cn/weather1dn/{district_url}.shtml"

            self.logger.info(f"parse_city: {item}")
            yield item
