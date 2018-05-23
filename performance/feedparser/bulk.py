import feedparser
import re


for i in range(100):
    browser = feedparser.parse('https://google.com')
    feed = browser.feed.summary

    mainform = re.search('<input .+?>', feed).group()
    print(mainform)
