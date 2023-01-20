# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

# TODO we're not using scrapy items, we're doing everything in a giant custom dictionary
#      Might need to do this on the spider close callback though, or we could have contention
# class WikiPage(scrapy.Item):
#     name = scrapy.Field()   # Name of page
#     links = scrapy.Field()  # List of linked pages


class WikiPageMetadata:

    def __init__(self, parent: str, children: list(), depth: int = 0):
        self.parent = parent
        self.children = children
        self.depth = depth

