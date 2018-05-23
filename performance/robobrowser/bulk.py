from robobrowser import RoboBrowser


for i in range(100):
    browser = RoboBrowser()
    browser.open('https://google.com')

    mainform = browser.select('input')[0]
    print(mainform)
