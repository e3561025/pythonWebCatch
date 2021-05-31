import requests
from bs4 import BeautifulSoup as bs
import json
from PIL import Image
import re

class pixivCatch:
    login_url='https://accounts.pixiv.net/login'
    pixiv_url='https://www.pixiv.net/'
    search_url='https://www.pixiv.net/search.php'

    pixiv_id = 'thisismyxxx24@gmail.com'
    password  = '3d1e2aehky2qwfui20vz'

    headers={
        'referer': 'https://www.pixiv.net/',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
    }
    
    r18_mode = False

    #get login post_key (vertufy using)
    def getkey(self):
        self.session = requests.Session()
        text = self.session.get(self.login_url).text
        post_key = re.findall('<input type="hidden" name="post_key" value="(.*?)"',text)[0]
        return post_key

    #login need some data to post and need to persist login => use Session
    def login(self):
        login_data={
            'pixiv_id': self.pixiv_id,
            'password': self.password,
            'post_key': self.getkey(),
            'source': 'pc',
            'ref': 'wwwtop_accounts_index',
            'return_to': 'https://www.pixiv.net/',
            'lang':'zh_tw',
            'captcha' : '',
            'g_recaptcha_response': '',
        }
        self.session.post(self.login_url,data=login_data)


    #start search
    def search(self,search_string):
        params = {
            "word" : search_string,
            "s_mode" : "s_tag",
        }
        if self.r18_mode==False:
            params.update({'mode' : 'safe'})
        else :
            params.update({'mode' : 'r18'})
        self.session.get(self.search_url,params=params)
        


    def __init__(self):
        self.login()