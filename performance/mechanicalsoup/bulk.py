import mechanicalsoup


for i in range(100):
    browser = mechanicalsoup.StatefulBrowser()
    browser.open('https://google.com')

    mainform = browser.get_current_page().find_all('input')[0]
    print(mainform)
