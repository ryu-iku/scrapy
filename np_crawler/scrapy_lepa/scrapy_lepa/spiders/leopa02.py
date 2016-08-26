# -*- coding: utf-8 -*-
from scrapy.loader.processors import MapCompose, Join
from scrapy.loader import ItemLoader
from scrapy_lepa.items import ScrapyLeoItem
import datetime
import urlparse
import socket
import scrapy

class Leopa02Spider(scrapy.Spider):
    name = "leopa02"

    # Start on a property page
    start_urls = [i.strip() for i in open('data/data_list_page_07152352_r_14man.csv').readlines()]
    # start_urls = [
    #     "http://www.leopalace21.com/app/searchCondition/detail/r/0000055990102.html",
    #     "http://www.leopalace21.com/app/searchCondition/detail/m/0000055990102.html",
    #     "http://www.leopalace21.com/app/searchCondition/detail/m/0000055845103.html"
    #     ]
    
    def parse(self, response):

        # Create the loader using the response
        l = ItemLoader(item=ScrapyLeoItem(), response=response)
        
        # Load fields using XPath expressions
        
        # page_url
        l.add_value('page_url', response.url)

        # rental_or_monthly
        if response.url[-20]=="r":
            l.add_value('rental_or_monthly', 'rental')
        else:
            l.add_value('rental_or_monthly', 'monthly')

        # leo_or_par
        if response.url[-18]==0:
            l.add_value('leo_or_par', 'leo')
        else:
            l.add_value('leo_or_par', 'par')

        # address
        if len(response.xpath('.//td[@colspan="2"][2]/text()'))==1:
            l.add_xpath('address','.//td[@colspan="2"][2]/text()')
        else:
             l.add_xpath('address','//*[@id="inquiry-form"]/div[1]/div/table/tbody/tr/td[2]/text()')

        # mail_box
        l.add_xpath('mail_box','.//ul[2]/li[8]/span/@class',MapCompose(lambda i: i.replace('sprite ico ','')))
        
        return l.load_item()