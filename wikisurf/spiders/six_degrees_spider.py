import scrapy

from items import WikiPageMetadata
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, Spider
from scrapy.link import Link
from scrapy import Request

WIKI_BASE_URL = r"https://www.wikipedia.org/wiki/"


class SixDegreesSpider(Spider):
    """
    Spider that breadth-first-searches wikipedia for a target page.  Will run up to 6 levels deep, but stops once
    the target is found.  Assumes that the title of a wiki article is equal to the URL relative path
    """

    name = 'six_degrees'
    allowed_domains = ['wikipedia.org']
    wiki_extractor = LinkExtractor(allow=r'wiki/', deny=[r'#cite_note', r'Help:'], unique=True,
                                   allow_domains=r'wikipedia.org')
    wiki_rule = Rule(wiki_extractor, callback='parse_item', follow=True)
    custom_settings = {
        'DEPTH_LIMIT': 6,               # 6 degrees
        'DEPTH_STATS_VERBOSE': True,    # nice stats
        'DEPTH_PRIORITY': 1,            # 1 = breadth-first search
        'ITEM_PIPELINES': {
            'wikisurf.pipelines.SixDegreesPipeline': 300
        }
    }

    def __init__(self, start_url: str = f'{WIKI_BASE_URL}sonic_drive-in', target: str = f'{WIKI_BASE_URL}corn_syrup'):
        self.start_urls = [start_url]
        self.start_name = self.extract_name(start_url)
        self.target = self.extract_name(target)
        self.finished = False

    @staticmethod
    def extract_name(url) -> str:
        if type(url) == scrapy.http.TextResponse:
            return url.url.replace(WIKI_BASE_URL, '').lower()
        elif type(url) == str:
            return url.replace(WIKI_BASE_URL, '').lower()
        else:
            raise TypeError()

    def parse(self, response: scrapy.http.TextResponse, **kwargs):
        # Do nothing if we're done
        if self.finished:
            return None

        # Create the item
        item = WikiPageMetadata()
        item['name'] = self.extract_name(response)
        if response.meta['parent']:
            item['parent'] = response.meta['parent']
        else:
            item['parent'] = None
        if response.meta['depth']:
            item['depth'] = response.meta['depth']
        else:
            item['depth'] = 0
        if item['name'] == self.target:
            self.finished = True
            # TODO: shut down here instead?
            return None
        link_list = self.wiki_extractor.extract_links()
        curated_link_list = []
        for link in link_list:
            curated_link_list.append(self.extract_name(link.url))
            # Build the next crawler requests
            if item['depth'] <= 6:
                yield response.follow(link, self.parse, meta={'depth': item['depth'] + 1, 'parent': item['name']})
        item['children'] = curated_link_list

        yield item

    # Override this function so we can pass in a start instead of having to hard-code it
    def start_requests(self):
        for s in self.start_urls:
            yield Request(s, self.parse, meta={'depth': 1, 'parent': self.extract_name(s)}, dont_filter=False)
