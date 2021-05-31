import requests
import re
import os
from bs4 import BeautifulSoup as bs
import http.cookiejar
import http.cookies

login_url  = 'https://accounts.pixiv.net/login?lang=zh_tw&source=pc&view_type=page&ref=wwwtop_accounts_index'
pixiv_id = 'thisismyxxx24@gmail.com'
password  = '3d1e2aehky2qwfui20vz'
url='https://www.pixiv.net/'
session = requests.Session()
response = session.get(login_url)
post_key = re.findall('<input type="hidden" name="post_key" value="(.*?)"',response.text)[0]
print(post_key)
login_url_headers = {
    'referer': 'https://www.pixiv.net/',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
    'Connection' : 'Keep-Alive',

}
login_data = {
    'pixiv_id': pixiv_id,
    'password': password,
    'post_key': post_key,
    'source': 'pc',
    'ref': 'wwwtop_accounts_index',
    'return_to': 'https://www.pixiv.net/',
    'lang':'zh_tw',
    'captcha' : '',
    'g_recaptcha_response': '',
}
test_headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
    'Connection' : 'Keep-Alive',
}
ck = http.cookiejar.CookieJar()
session_url  = 'https://accounts.pixiv.net/login'   
test_url='https://www.pixiv.net/search.php?s_mode=s_tag&word=cat'
response = session.post(session_url,data = login_data)
test = requests.get('https://www.pixiv.net/member_illust.php?mode=medium&illust_id=74801490',headers=login_url_headers)
test2 = requests.get('https://i.pximg.net/img-original/img/2019/05/19/16/14/26/74801490_p0.jpg',headers = login_url_headers)
print(test2.content)
# htmlAjax = session.get(test_url,headers = login_url_headers)
# text = htmlAjax.text
#soup = bs(response.text,'html.parser')

#print(soup.prettify())
with open('xx.jpg','wb') as f:
    f.write(test2.content)
session.close()