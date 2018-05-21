from cola.core.opener import MechanizeOpener
import re


browser = MechanizeOpener().open('https://google.com')
mainform = re.search('<input .+?>', browser).group()

print(mainform)
