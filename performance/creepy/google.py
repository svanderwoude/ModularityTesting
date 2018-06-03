from creepy import Crawler
import re


class GoogleCrawler(Crawler):
    def process_document(self, doc):
        mainform = re.search('<input .+?>', doc.text).group()
        print(mainform)

c = GoogleCrawler()
c.set_max_depth(1)
c.crawl('https://www.google.com/')