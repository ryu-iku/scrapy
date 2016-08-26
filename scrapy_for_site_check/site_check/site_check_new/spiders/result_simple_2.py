# -*- coding: utf-8 -*-
from scrapy.loader.processors import MapCompose, Join
from scrapy.loader import ItemLoader
import datetime
import urlparse
import socket
import scrapy
from scrapy.http import Request


class ResultAllTestSpider(scrapy.Spider):
    # Crawlerの名前をresult_simple_1に設定し、コマンド「scrapy crawl result_simple_2 ...」で実行
    name = 'result_simple_2'
    start_urls = [i.strip() for i in open('data/clean02_otherthanover100_08082009_r.csv').readlines()]

    def parse(self, response):
        print "start scrapy!!"+response.url
        
        # NP後払い関連のURL
        target_urls=[
            "www.netprotections.com/atobarai",
            "www.netprotections.com/wiz/atobarai",
            "np-atobarai.jp/about",
            "np-atobarai.jp/about/index_wiz",
            "www.np-atobarai.jp/about/index_wiz",
            "link.rakuten.co.jp/0/001/362/",
            "link.rakuten.co.jp/0/006/480/",
            "link.rakuten.co.jp/1/005/549/",
            "link.rakuten.co.jp/0/044/177/",
            "link.rakuten.co.jp/0/044/178/",
            "www.netprotections.com/y/atobarai",
            "www.netprotections.com/y/wiz",
            "np-atobarai.jp/about/mall",
            "np-atobarai.jp/about",
            "np-atobarai.jp/about/mall_wiz",
            ]
        
        # NP後払い関連のキーワード
        target_word01=u'NP後払'
        target_word02=u'後払'
        
        # 出力用の変数comment
        comment=""
        
        print response.url  # 現在ページのURLをprintする
        
        # Crawler対象ページのテキストを変数res_textに保存する
        res_text=""
        if response.xpath('//body').extract():
            res_text=" ".join(response.xpath('//body').extract())
        
        # res_textの中、NP後払い関連のURL存在するかを確認する
        for target_url in target_urls:
            if res_text.find(target_url)>-1:
                comment="np_url"
                print "comment: "+comment
                print response.url
                print target_url
        
        # res_textの中、NP後払い関連のURLが存在しない場合、NP後払い関連のキーワード存在するかを確認する
        if comment=="":
            if res_text.find(target_word01)>-1:
                comment="np_word01"
                print "comment: "+comment
                print response.url
                
            elif res_text.find(target_word02)>-1:
                comment="np_word02"
                print "comment: "+comment
                print response.url
        
        # 有効の結果を出力する
        if comment!="":
            # yield {'link': full_url}
            print "got it!!!"+response.url
            return {
                'link': response.url,
                'comment': comment,
                'title': response.xpath('//title/text()').extract(),
            }