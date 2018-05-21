from grab import Grab


browser = Grab()
page = browser.go('https://google.com')

mainform = page.rex_search('<input .+?>').group(0)
print(mainform)
