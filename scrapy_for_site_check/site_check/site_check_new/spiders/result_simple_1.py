# -*- coding: utf-8 -*-
from scrapy.loader.processors import MapCompose, Join
from scrapy.loader import ItemLoader
import datetime
import urlparse
import socket
import scrapy
from scrapy.http import Request


class ResultAllTestSpider(scrapy.Spider):
    # Crawlerの名前をresult_simple_1に設定し、コマンド「scrapy crawl result_simple_1 ...」で実行
    name = 'result_simple_1'
    
    # crawlerの始めるurlリストを決める
    start_urls = [i.strip() for i in open('data/clean02_otherthanover100_08082009.csv').readlines()]

    def parse(self, response):
        # ページを開いた後、現在ページのURLをprintする
        print "start scrapy!!"+response.url
        
        # ページ内のリンクpathを訪問できるように加工する
        urls=response.xpath('.//@href').extract()
        
        # 各URLとそのページ内のリンクをアウトプットとして出す
        for url in urls:
            url=urlparse.urljoin(response.url, url)
            yield {
                'start_url': response.url,
                'next_url': url
            }