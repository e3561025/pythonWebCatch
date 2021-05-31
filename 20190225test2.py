import requests
import urllib
import re
from bs4 import BeautifulSoup as bs

data_soup=bs('<div data-foo="value">foo!</div>','html.parser')
data_soup.find_all(attrs={"data-foo":'value'})
print(data_soup)

div_tag = data_soup.find_all('div')
print(div_tag)
