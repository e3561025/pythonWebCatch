import requests
from bs4 import BeautifulSoup 
import re
doc="""
<body>
<b class="boldest">Extremely bold</b>
<b class="bold">Extre bold</b>
</body
"""
soup = BeautifulSoup(doc,'html.parser')
tag = soup.b
print(tag.name)
tag.name='user'

print(tag)