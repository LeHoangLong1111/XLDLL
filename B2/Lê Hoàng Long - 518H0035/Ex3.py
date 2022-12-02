##with scrapy

import scrapy

class Crawler(scrapy.Item):
    date = scrapy.Field()
    Content = scrapy.Field()