import scrapy

from ..constants import WIKI_BASE_URL
from ..items import WikiPageMetadata
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.link import Link
from scrapy import Request


class SixDegreesSpider(CrawlSpider):
    """
    Spider that breadth-first-searches wikipedia for a target page.  Will run up to 6 levels deep, but stops once
    the target is found.  Assumes that the title of a wiki article is equal to the URL relative path
    """

    name = 'six_degrees'
    allowed_domains = ['wikipedia.org']

    wiki_extractor = LinkExtractor(allow=r'wiki/', deny=[r'#cite_note', r'Help:'])
    wiki_rule = Rule(wiki_extractor, callback='parse_item', follow=True)

    rules = (
        wiki_rule
    )

    def __init__(self, start_url: str = f'{WIKI_BASE_URL}sonic', target: str = f'{WIKI_BASE_URL}blue'):
        self.start_urls = [start_url]
        self.target = target
        self.finished = False
        # TODO: this is a class variable, but scrapy is multithreaded, need to make sure we don't have contention
        #       issues.  We should be OK because if scrapy is configured correctly, it won't
        self.theMap = dict(str, WikiPageMetadata)

    @staticmethod
    def extract_name(self, response: scrapy.http.TextResponse) -> str:
        return response.url.replace(WIKI_BASE_URL, '').lower()

    def parse_item(self, response: scrapy.http.TextResponse) -> WikiPage:
        if self.finished:
            return None
        item = WikiPage()
        #item['name'] = response.css('.mw-page-title-main::text').get() # TODO: just do everything on URLs
        item['name'] = self.extract_name(response)
        link_list = self.wiki_extractor.extract_links()
        curated_link_list = []
        for link in link_list:
            curated_link_list.append(self.extract_name(link.url))
        item['links'] = curated_link_list
        return item

    def parse_start_url(self, response, **kwargs):
        pass

    def parse(self, response, **kwargs):
        pass

    # Override this function so we can pass in a start instead of having to hard-code it
    def start_requests(self):
        for s in self.start_urls:
            yield Request(s, dont_filter=False)
