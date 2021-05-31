import re
from bs4 import BeautifulSoup
html_doc = """
<body><p class="my_par">
<a id="link1" href="/my_link1">Link 1</a>
<a id="link2" href="/my_link2">Link 2</a>
<a id="link3" href="/my_link3">Link 3</a>
<a id="link4" href="/my_link4">Link 4</a>
</p></body>
"""
soup = BeautifulSoup(html_doc, 'html.parser')
link2_tag = soup.find(id="link2")
print(link2_tag.get('href'))

#尋找 上一層(即與自己同輩分的其他檔案)
"""
p_tag = link2_tag.find_parents("p")
print(p_tag)
"""

#尋找 上一層 在自己上方的(下方的不找) 若 siblings 則上方全找
"""
link_tag = link2_tag.find_previous_sibling("a")
print(link_tag)
"""
#尋找 上一層 在自己下方的(上方的不找) 
link_tag = link2_tag.find_next_siblings("a")
print(link_tag)













