import re
from bs4 import BeautifulSoup as bs

links_html = """
<a id="link1" href="/my_link1">Link One</a>
<a id="link2" href="/my_link2">Link Two</a>
<a id="link3" href="/my_link3">Link Three</a>
"""

#對 string 屬性進行 re.compile
soup = bs(links_html,'html.parser')
link=soup.find_all('a',string='Link One')
link2=soup.find_all('a',string=re.compile("^Link"))
print(link2)