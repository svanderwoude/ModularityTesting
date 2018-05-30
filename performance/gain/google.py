from gain import Css, Item, Parser, Spider


class Post(Item):
    i = Css('input')

    async def save(self):
        print(self.i)


class GoogleSpider(Spider):
    start_url = 'https://google.com/'
    concurrency = 1
    headers = {'User-Agent': 'Google Spider'}
    parsers = [Parser('/'),
               Parser('/', Post)]

try:
    GoogleSpider.run()
except:
    pass
