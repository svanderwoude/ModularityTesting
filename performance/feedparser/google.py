import feedparser
import re


browser = feedparser.parse('https://google.com')
feed = browser.feed.summary

mainform = re.search('<input .+?>', feed).group()
print(mainform)
