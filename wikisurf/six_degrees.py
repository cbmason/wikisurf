"""
Gathers the start and target pages, then builds and runs the spider
"""

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spiders.six_degrees_spider import SixDegreesSpider


def run():
    # derp
    # Ask for start
    # Ask for end
    # Make sure those both exist
    # Build spider
    # Run spider
    # Process spider results
    process = CrawlerProcess(settings={
        "FEEDS": {
            "items.json": {"format": "json"}
        }
    })
    spider = SixDegreesSpider()
    process.crawl(spider)
    process.start()


if __name__ == "__main__":
    run()
