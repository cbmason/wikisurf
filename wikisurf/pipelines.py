# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from wikisurf.items import WikiPageMetadata
from wikisurf.spiders import six_degrees_spider
from collections import deque


class SixDegreesPipeline:

    def __init__(self):
        self.master_dict = None

    def process_item(self, item: WikiPageMetadata, spider: six_degrees_spider):
        if item['name'] not in self.master_dict.keys():
            self.master_dict[item['name']] = item
        return item

    def open_spider(self, spider: six_degrees_spider):
        self.master_dict = dict()

    def close_spider(self, spider: six_degrees_spider):
        if spider.target in self.master_dict:
            cur = self.master_dict[spider.target]
            path = deque()
            while 'parent' in cur and cur['parent'] is not None and cur['name'] is not spider.start_name:
                path.appendleft(cur['name'])
                cur = self.master_dict[cur['parent']]
            path.appendleft(cur['name']) # append the root
            print("*************************")
            print("****** Path Found! ******")
            print("*************************")
            i = 1
            for p in path:
                print(f'{i}: {p}')
                i += 1
        else:
            print(f"No connection from {spider.start_name} to {spider.target} was found!")
