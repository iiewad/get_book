# -*- coding: utf-8 -*-

import scrapy
import json

from book.items import BookItem

class Books(scrapy.Spider):
    name = "books"

    def start_requests(self):
        url = 'http://www.136book.com/'

        yield scrapy.Request(url = url, callback=self.parse)

    def parse(self, response):
        book_list = response.css('div#digg_list>ul>li')
        for list in book_list:
            link = list.css('div.book_desc>a::attr(href)').extract_first()
            response.follow(link, callback=self.parse_list)

    def parse_list(self, response):
        item = BookItem()

        content_title = response.css('div.cont_title')
        item['title'] = content_title.css('h1::text').extract_first()
        item['author'] = content_title.css('div.hslice>p.entry-title>a::text').extract_first()
        item['thumb'] = content_title.css('div.hslice>div.thumb>img::attr(src)').extract_first()

        details = response.css('div#book_detail')
        details.remove(details[0]) #删除最新章节
        chapters = details.css('ol>li')

        for c_list in chapters:
            c_link = c_list.css('a::attr(href)').extract_first()
            response.follow(c_link, callback=self.parse_chapter)

    def parse_chapter(self, response):
        item = BookItem()
        item['c_title'] = response.css('h1::text').extract_first()
        item['content'] = response.xpath('//*[@id="content"]/p/text()').extract()

        yield item
