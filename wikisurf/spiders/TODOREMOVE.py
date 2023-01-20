import scrapy
import datetime
import os

from ..items import WikiPage
from scrapy.loader import ItemLoader


class DummySpider(scrapy.spiders.CrawlSpider):
    name = "six_degrees"

    def __init__(self, start_url: str = 'https://en.wikipedia.org/wiki/Mario', log_name: str = 'wikisurf_log'):
        self.start_urls = [start_url]
        # TODO: replace with real logging mechanism
        if not os.path.exists('./logs'):
            print("Logs directory doesn't exist, creating...")
            os.mkdir('logs')
        full_log_name = f'./logs/{log_name}_{datetime.datetime.now()}.log'
        with open(full_log_name, 'w') as logfile:
            logfile.write("**** LOG START ****")
            self.log_name = full_log_name

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response: scrapy.http.TextResponse, **kwargs):
        page = response.url.split("/")[-2]
        filename = f'{page}.html'
        if self.log_name:
            with open(self.log_name, 'wb+') as log:
                log.write(bytes(f"Visited {filename}", 'utf-8'))
                log.write(response.body)
        il = ItemLoader(item=WikiPage(), selector=p)






