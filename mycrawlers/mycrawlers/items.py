# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MycrawlersItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class ItemPR(scrapy.Item):
	perg = scrapy.Field()
	resp = scrapy.Field()

class ItemGeneric(scrapy.Item):
	title = scrapy.Field()
	content = scrapy.Field()