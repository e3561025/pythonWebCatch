import requests
import urllib
import re
from bs4 import BeautifulSoup as bs
html_doc = """
<html><head><title>Hello World</title></head>

<body><h2>Test Header</h2>
<title>Hello World</title>
<p>This is a test.</p>
<a id="link1" href="/my_link1">Link 1</a>
<a id="link2" href="/my_link2">Link 2</a>
<a id="link1" href="/my_link">Link 3</a>
<p>Hello, <b class="boldtext">Bold Text</b></p>
</body></html>
"""
soup = bs(html_doc,'html.parser')

#尋找html的 <a 超連結標籤
"""  
a_tags = soup.find_all('a')
for tag in a_tags:
    print(tag.string)
    print(tag.get('href'))
"""

#尋找 <title 標題 標籤
"""title = soup.title
print(title.string)
#a_tags = soup.html.find_all('title',recursive=True)
#a_tags = soup.find_all('title')
"""
#尋找 id 
"""
link2_tag = soup.find(id='link2')
print(link2_tag)
"""

#多重尋找 
"""
a_tag = soup.find_all('a',href='/my_link1')
print(a_tag)

## ^/my_link 的 ^ 意思是 開頭完全符合my_link 如: smy_link就不行
## my_link\d 的 \d 意思是 字尾後面還有數字
links = soup.find_all(href=re.compile("^/my_link\d"))
print(links)
link = soup.find_all(href=re.compile("^/my_link\d"), id="link1")
print(link)
"""














