# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WsmCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    content = scrapy.Field()
    publish_year = scrapy.Field()
    category = scrapy.Field()
    size = scrapy.Field()
    finished = scrapy.Field()
    cover_url = scrapy.Field()

    def __repr__(self):
        """为了不在命令行中显示爬到的内容，故做此重载
           如果需要显示，则将其注释即可
        """
        return ''
