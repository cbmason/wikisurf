# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WikiPageMetadata(scrapy.Item):
    name = scrapy.Field()       # Name of page
    parent = scrapy.Field()     # Where this was linked from
    children = scrapy.Field()   # What we're linking to
    depth = scrapy.Field()      # How far removed we are from the start

