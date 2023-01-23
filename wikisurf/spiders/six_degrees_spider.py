import re
import scrapy
from scrapy.exceptions import CloseSpider

from wikisurf.items import WikiPageMetadata
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Spider
from scrapy import Request

WIKI_BASE_URL = r"https://en.wikipedia.org/wiki/"


class SixDegreesSpider(Spider):
    """
    Spider that breadth-first-searches wikipedia for a target page.  Will run up to 6 levels deep, but stops once
    the target is found.  "Start_url" and "Target" must be passed in on the command line
    """

    name = 'six_degrees'
    allowed_domains = ['en.wikipedia.org']
    wiki_extractor = LinkExtractor(allow=re.escape('wiki/'),
                                   deny=[re.escape(r'#cite'), re.escape(r'Help'), re.escape(r'#'),
                                         re.escape(r'category:'), re.escape(r'template:'),  re.escape(r'wikipedia:'),
                                         re.escape(r'special:'), re.escape(r'portal:'), re.escape(r'talk:'),
                                         re.escape(r'File:'), re.escape(r'?')],
                                   unique=True, allow_domains=r'en.wikipedia.org',
                                   restrict_css=['p'])
    custom_settings = {
        'DEPTH_LIMIT': 5,               # 6 degrees = 5 + 1 for reading children
        'DEPTH_STATS_VERBOSE': True,    # nice stats
        'DEPTH_PRIORITY': 1,            # 1 = breadth-first search
        'ITEM_PIPELINES': {
            'wikisurf.pipelines.SixDegreesPipeline': 100
        }
    }

    def __init__(self, *args, **kwargs):
        super(SixDegreesSpider, self).__init__(*args, **kwargs)
        self.start_urls = [self.create_url(kwargs.get('start_url'))]
        self.start_name = self.extract_name(kwargs.get('start_url'))
        self.target = self.extract_name(kwargs.get('target'))
        self.finished = False

    @staticmethod
    def extract_name(url) -> str:
        if isinstance(url, scrapy.http.TextResponse):
            return url.url.replace(WIKI_BASE_URL, '')
        elif isinstance(url, str):
            return url.replace(WIKI_BASE_URL, '')
        else:
            badtype = type(url)
            raise TypeError(f'extract_name called with {badtype}')

    def create_url(self, name) -> str:
        # extract just in case we pass this a url
        normalized_name = self.extract_name(name)
        url = WIKI_BASE_URL + normalized_name
        return url

    def parse(self, response: scrapy.http.TextResponse, **kwargs):
        # Do nothing if we're done
        if self.finished:
            raise CloseSpider('Finished searching')

        # Create the item
        item = WikiPageMetadata()
        item['name'] = self.extract_name(response)
        if response.request.headers.get('Referer'):
            item['parent'] = self.extract_name(str(response.request.headers.get('Referer'), 'utf-8'))
        else:
            item['parent'] = None
        if response.meta['depth']:
            item['depth'] = response.meta['depth']
        else:
            item['depth'] = 0
        if item['name'] == self.target:
            self.finished = True
        link_list = self.wiki_extractor.extract_links(response)
        curated_link_list = []
        for link in link_list:
            link_name = self.extract_name(link.url)
            curated_link_list.append(self.extract_name(link.url))
            if link_name == self.target:
                found_item = WikiPageMetadata()
                found_item['name'] = link_name
                found_item['parent'] = item['name']
                found_item['depth'] = item['depth'] + 1
                found_item['children'] = []
                yield found_item
                self.finished = True
            item['children'] = curated_link_list

            # Build the next crawler requests as long as we're not done
            if item['depth'] <= 6 and not self.finished:
                yield response.follow(link, self.parse, meta={'depth': item['depth'] + 1, 'parent': item['name']})

        yield item

    # Override this function so we can pass in a start instead of having to hard-code it
    def start_requests(self):
        for s in self.start_urls:
            yield Request(s, self.parse, meta={'depth': 0, 'parent': None}, dont_filter=False)
            item = WikiPageMetadata()
            item['name'] = self.extract_name(s)
            item['parent'] = None
            item['depth'] = 0
