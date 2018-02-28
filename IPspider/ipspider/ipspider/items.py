# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class IpspiderItem(scrapy.Item):
    name = scrapy.Field()
    created = scrapy.Field()
    updated = scrapy.Field()
    downloadLink = scrapy.Field()
    category = scrapy.Field()
    language = scrapy.Field()
    license = scrapy.Field()
