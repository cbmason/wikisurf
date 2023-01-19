# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WikiPage(scrapy.Item):
    name = scrapy.Field()   # Name of page
    path = scrapy.Field()   # How we got here
    level = scrapy.Field()  # How many jumps, redundant with path
    links = scrapy.Field()  # List of linked pages

