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
<p>Hello, <b class="boldtext">Bold Text</b></p>
</body></html>
"""
soup = bs(html_doc,'html.parser')

"""
b_tag = soup.find_all("b", class_="boldtext")
print(b_tag)
"""
b_tag = soup.find_all(class_=re.compile("^bold"))
print(b_tag)

css_soup = bs('<p class="body strikeout"></p>', 'html.parser')
p_tag = css_soup.select("p.strikeout.body")
print(p_tag)
