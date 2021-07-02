import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from ..items import WeatherItem


class TianqiSpider(scrapy.Spider):
    name = 'tianqi'
    allowed_domains = ['weather.com.cn']
    start_urls = ['http://www.weather.com.cn/weather1dn/101120101.shtml']  # TODO: Get urls from file

    def __init__(self):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        self.browser = webdriver.Chrome(options=options)

    def close(self):
        self.browser.close()

    def parse(self, response):
        item = WeatherItem()

        selector = response.xpath('//div[@class="todayLeft"]')
        item['time'] = selector.xpath('//span[@id="time"]//text()').extract()[0]
        item['temp'] = selector.xpath('//span[@id="temp"]//text()').extract()[0]
        item['maxTemp'] = selector.xpath('//span[@id="maxTemp"]//text()').extract()[0]
        item['minTemp'] = selector.xpath('//span[@id="minTemp"]//text()').extract()[0]
        item['aqi'] = selector.xpath('//span[@id="aqi"]//a//text()').extract()[0]
        item['wind'] = selector.xpath('//span[@id="wind"]//text()').extract()[0]
        item['humi'] = selector.xpath('//span[@id="humidity"]//text()').extract()[0]

        self.logger.info(f"Weather: {item}")

        yield item
