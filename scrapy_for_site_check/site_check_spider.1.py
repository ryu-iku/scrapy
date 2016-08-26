 # -*- coding: utf-8 -*-
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector

import scrapy
import re
import csv

class SiteCheckSpider(scrapy.Spider):
    name = 'sitecheck'
    # start_urls = [i.strip() for i in open('data/crawl_list_01.csv').readlines()]
    start_urls = [
        "http://www.lensfree.jp/",
        "http://www.rakuten.ne.jp/gold/aionline-japan/",
        "http://www.katocoffee.net/"
        ]

    def parse(self, response):
        if response.status>299:
            yield {
                'type': "access_failed",
                'link': response.url,
                'response': response.status
            }
        else:
            res_text=" ".join(response.css('body').extract())
            if (res_text.find(u"支払")>-1) and (res_text.find(u"返品")>-1):
                yield {
                    'type': "job_done",
                    'link': response.url,
                    'title': response.css('title').extract_first()
                }
                
            else:
                for href in response.css('a::attr(href)'):
                    full_url = response.urljoin(href.extract())
                    yield scrapy.Request(full_url, callback=self.parse_question)
                
                # next_url = HtmlXPathSelector(response).select("//a[contains(text(),u'支払')]/@href")
                # if next_url:
                #     yield scrapy.Request(next_url, callback=self.parse_question)
                

    def parse_question(self, response):
        res_text=" ".join(response.css('body').extract())
        if (res_text.find(u"支払")>-1) and (res_text.find(u"返品")>-1):
            return {
                'type': "job_done",
                'link': response.url,
                'title': response.css('title').extract_first()
            }