# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from items import WikiPageMetadata
from spiders import six_degrees_spider
from collections import deque


class SixDegreesPipeline:

    def __init__(self):
        self.target = None
        self.master_dict = None

    def process_item(self, item: WikiPageMetadata):
        if item['name'] not in self.master_dict:
            self.master_dict[item['name']] = item
        return item

    def open_spider(self):
        self.master_dict = dict(str, WikiPageMetadata)

    def close_spider(self, spider: six_degrees_spider):
        if spider.target in self.master_dict:
            cur = self.master_dict[spider.target]
            path = deque()
            while 'parent' in cur and cur['name'] is not spider.start_name:
                path.appendleft(cur['name'])
                cur = self.master_dict[cur['parent']]
            print("Path Found!")
            for i in path:
                print(i)
        else:
            print(f"No connection from {spider.start_name} to {spider.target} was found!")
