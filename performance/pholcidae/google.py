from io import StringIO

from lxml import etree

from pholcidae2 import Pholcidae


class MyWikiSpider(Pholcidae):
    def crawl(self, data):
        tree = etree.parse(StringIO(data['body']), self.html_parser)
        inputs = tree.xpath(".//input")

        print(inputs[0])


settings = {
    'protocol': 'https://',
    'domain': 'www.google.com',
    'start_page': '/',
    'exclude_links': ['(.*)'],
    'threads': 1,
}

spider = MyWikiSpider()
spider.extend(settings)
spider.html_parser = etree.HTMLParser()
spider.start()