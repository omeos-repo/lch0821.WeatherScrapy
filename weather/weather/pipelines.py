# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


from .spiders.city import CitySpider
from .spiders.tianqi import TianqiSpider


class WeatherPipeline:
    def process_item(self, item, spider):
        return item


class JsonWriterPipeline:
    def open_spider(self, spider):
        if isinstance(spider, CitySpider):
            self.urls_seen = []
            self.file = open('output/cities.jl', 'w')
        elif isinstance(spider, TianqiSpider):
            self.file = open('output/tianqi.jl', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        if isinstance(spider, CitySpider):
            if item['url'] in self.urls_seen:
                return item
            self.urls_seen.append(item['url'])
            line = json.dumps(ItemAdapter(item).asdict(), ensure_ascii=False) + "\n"
            self.file.write(line)
        elif isinstance(spider, TianqiSpider):
            # TODO: Write data to DB
            line = json.dumps(ItemAdapter(item).asdict(), ensure_ascii=False) + "\n"
            self.file.write(line)

        return item
