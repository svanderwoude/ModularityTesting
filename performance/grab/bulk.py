from grab import Grab


for i in range(100):
    browser = Grab()
    page = browser.go('https://google.com')

    mainform = page.rex_search('<input .+?>').group(0)
    print(mainform)
