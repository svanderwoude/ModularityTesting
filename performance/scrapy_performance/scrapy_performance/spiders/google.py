# -*- coding: utf-8 -*-
import scrapy


class GoogleSpider(scrapy.Spider):
    name = 'google'
    allowed_domains = ['https://google.com']
    start_urls = (
        'https://google.com/',
    )

    def parse(self, response):
        mainform = response.css('input').extract_first()
        print(mainform)
