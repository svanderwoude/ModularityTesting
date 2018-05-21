from robobrowser import RoboBrowser


browser = RoboBrowser()
browser.open('https://google.com')

mainform = browser.select('input')[0]
print(mainform)
