# # -*- coding: utf-8 -*-
# import scrapy
# from scrapy.crawler import CrawlerProcess


# class GoogleSpider2(scrapy.Spider):
#     name = 'google'
#     allowed_domains = ['https://google.com']
#     start_urls = (
#         'https://google.com/',
#     )

#     def parse(self, response):
#         mainform = response.css('input').extract_first()
#         print(mainform)


# for i in range(100):
#     process = CrawlerProcess({
#         'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
#     })

#     process.crawl(GoogleSpider2)
#     process.start()
