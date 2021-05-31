#注:python版本为2.7,python3运行会报错
import requests
import re
import os

#使用代理
proxies = {
    'https': 'socks5h://127.0.0.1:1080',
    'http': 'socks5h://127.0.0.1:1080'
}

login_url  = 'https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index'
pixiv_id = '你的账号'
password  = '你的密码'

#headers中的Referer是不可或缺的，缺少了你将什么图片都获取不到
login_url_headers = {
    'Referer': 'https://www.pixiv.net/member_illust.php?mode=medium&illust_id=64503210',
}

while(True):
    try:
        session = requests.Session()
        response = session.get(login_url, proxies=proxies,timeout=5)

        #获取post_key
        post_key=re.findall('<input type="hidden" name="post_key" value="(.*?)"',response.content,re.S)[0]
        print(post_key)

        #构造表单
        login_data = {
            'pixiv_id': pixiv_id,
            'password': password,
            'post_key': post_key,
            'source': 'pc',
            'ref': 'wwwtop_accounts_index',
            'return_to': 'https://www.pixiv.net/'
        }

        #提交表单
        session_url  = 'https://accounts.pixiv.net/api/login?lang=zh'     
        response = session.post(session_url, data = login_data,proxies=proxies)

        #获取动态加载的内容(链接是抓包获得的)
        htmlAjax = session.get('https://www.pixiv.net/ajax/illust/64538123/recommend/init?limit=18',
                            proxies=proxies).content
       #获取图片地址，获取的不是高清大图的链接，不过稍微构造一下就好了
        url_img=re.findall('"imageUrl":"(.*?)",',htmlAjax,re.S)
        url_front='https://i.pximg.net'
        url_behind='master1200.jpg'
        for i in range(len(url_img)):
            url_img[i]=url_img[i].replace('\\','')
            url_img[i]=url_front+url_img[i][32:-14]+url_behind
            print(url_img[i])

        #创建pic文件夹，用来存放图片
        path='/home/user/getPixiv/pic'#/home/user/getPixiv是你当前目录的绝对地址
        if not os.path.exists(path):
            os.makedirs(path)

        #获取图片
        for i in range(len(url_img)):
            img=session.get(url_img[i],proxies=proxies,headers=login_url_headers)
            print('----------------------downloading img'+url_img[i]+'------------------------------')
            fp=open('pic/'+str(i)+'.jpg','wb')
            fp.write(img.content)
            fp.close()
            print('----------------------succeed!----------------------------------------')
        break
    except:
        print("timeout")
        time.sleep(5)
        continue
