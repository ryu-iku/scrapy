# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class ScrapyLeoItem(Item):
    page_url=Field()
    rental_or_monthly=Field()
    leo_or_par=Field()
    address=Field()
    mail_box=Field()