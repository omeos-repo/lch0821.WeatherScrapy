# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import json
from crown import TdEngineDatabase


class TianqiPipeline:
    def process_item(self, item, spider):
        return item


class JsonWriterPipeline:
    def open_spider(self, spider):
        self.file = open('../output/tianqi.jl', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(ItemAdapter(item).asdict(), ensure_ascii=False) + "\n"
        self.file.write(line)

        return item


class TDenginePipeline:
    def open_spider(self, spider):
        dbname = 'tq'
        host = 'localhost'
        port = 6041
        self.db = TdEngineDatabase(dbname, host=host, port=port)
        self.db.connect()
        self.items = []

    def close_spider(self, spider):
        self.insert_items()

    def process_item(self, item, spider):
        self.items.append(item)
        if len(self.items) >= 100:
            self.insert_items()

        return item

    def insert_items(self):
        self.db.raw_sql("use tq;")
        sql = "INSERT INTO"
        for item in self.items:
            sql = sql + f''' T{item['code']} USING weather TAGS("{item['code']}", "{item['province']}", "{item['city']}", "{item['district']}") VALUES("{item['time']}", {item['temp']}, {item['humi']}, {item['maxtemp']}, {item['mintemp']}, {item['aqi']}, {item['windd']}, {item['winds']}, {item['rain']}, {item['rain24h']}, {item['forecast']})'''
        self.db.raw_sql(sql)
        self.items = []
