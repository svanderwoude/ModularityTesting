from cola.core.opener import MechanizeOpener
import re


for i in range(100):
    browser = MechanizeOpener().open('https://google.com')
    mainform = re.search('<input .+?>', browser).group()

    print(mainform)
