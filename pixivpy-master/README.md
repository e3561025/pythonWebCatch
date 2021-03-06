PixivPy [![Build Status](https://travis-ci.org/upbit/pixivpy.svg)](https://travis-ci.org/upbit/pixivpy)
======
_Pixiv API for Python (with Auth supported)_

* [2019/04/27] Support hosts proxy for AppAPI, which can use behind the Great Wall (See [example_api_proxy.py](https://github.com/upbit/pixivpy/blob/master/example_api_proxy.py))
* [2017/04/18] Fix encoder BUG for `illust_bookmark_add()/illust_bookmark_delete()` params (thanks [naplings](https://github.com/naplings))
* [2017/01/05] Add `PixivAPI().works()` liked API `illust_detail()` for App-API (thanks [Mapaler](https://github.com/Mapaler)), release v3.3
* [2016/12/17] Fixed encoding BUG for Public-API, see #26 (thanks [Xdynix](https://github.com/Xdynix))
* [2016/07/27] Now `AppPixivAPI()` can call **without auth** (thanks [zzycami](https://github.com/zzycami)), check [demo.py](https://github.com/upbit/pixivpy/blob/b83578e066ddcba86295676d931ff3313d138b22/demo.py#L268)
* [2016/07/20] New **App-API** (Experimental) for `PixivIOSApp/6.0.9`
* [2016/07/11] Add new [iOS 6.x API](https://github.com/upbit/pixivpy/wiki#6x-api) reference to Wiki
* [2015/12/02] Add write API for favorite an user / illust, release v3.1
* [2015/08/11] Remove SPAI and release v3.0 (pixivpy3) (Public-API with Search API)
* [2015/05/16] As Pixiv **deprecated** SAPI in recent days, push new Public-API **ranking_all**
* [2014/10/07] New framework, **SAPI / Public-API** supported (requests needed)

Use pip for installing:

~~~
pip install pixivpy --upgrade
~~~

Requirements: [requests](https://pypi.python.org/pypi/requests)

### Projects base on pixivpy

1. [Xdynix/PixivPixie](https://github.com/Xdynix/PixivPixie): User-friendly Pixiv API based on PixivPy

### Example:

~~~python
from pixivpy3 import *

api = AppPixivAPI()
# api.login("username", "password")   # Not required

# get origin url
json_result = api.illust_detail(59580629)
illust = json_result.illust
print(">>> origin url: %s" % illust.image_urls['large'])

# get ranking: 1-30
# mode: [day, week, month, day_male, day_female, week_original, week_rookie, day_manga]
json_result = api.illust_ranking('day')
for illust in json_result.illusts:
    print(" p1 [%s] %s" % (illust.title, illust.image_urls.medium))

# next page: 31-60
next_qs = api.parse_qs(json_result.next_url)
json_result = api.illust_ranking(**next_qs)
for illust in json_result.illusts:
    print(" p2 [%s] %s" % (illust.title, illust.image_urls.medium))
~~~

### [Sniffer - App API](https://github.com/upbit/pixivpy/wiki#6x-api)
### [Sniffer - Public API](https://github.com/upbit/pixivpy/wiki/sniffer)

### [Using AppPixivAPI() to download illusts (without auth)](https://github.com/upbit/pixivpy/blob/master/download_illusts.py#L24)
### [Using API proxy behind the Great Wall](https://github.com/upbit/pixivpy/blob/master/example_api_proxy.py#L33) See detail in [Issue#73](https://github.com/upbit/pixivpy/issues/73)

1. Upgrade pixivpy >= **v3.2.0**: `pip install pixivpy --upgrade`
2. Call `api.download()` like the below:

~~~python
aapi = AppPixivAPI()
json_result = aapi.illust_ranking()
for illust in json_result.illusts[:3]:
    aapi.download(illust.image_urls.large)
~~~

### [Migrate pixivpy2 to pixivpy3](https://github.com/upbit/pixivpy/blob/master/demo.py#L15-L25)

1. Replace `api.papi.*` to `api.*`
2. Change deprecated SPAI call to Public-API call

~~~python
print(">>> new ranking_all(mode='daily', page=1, per_page=50)")
#rank_list = api.sapi.ranking("all", 'day', 1)
rank_list = api.ranking_all('daily', 1, 50)
print(rank_list)

# more fields about response: https://github.com/upbit/pixivpy/wiki/sniffer
ranking = rank_list.response[0]
for img in ranking.works:
	#print img.work
	print("[%s/%s(id=%s)] %s" % (img.work.user.name, img.work.title, img.work.id, img.work.image_urls.px_480mw))
~~~

### About

1. Blog: [Pixiv Public-API (OAuth)??????](http://blog.imaou.com/opensource/2014/10/09/pixiv_api_for_ios_update.html)

If you have any questions, please feel free to contact me: rmusique@gmail.com

Find Pixiv API in **Objective-C**? You might also like [**PixivAPI_iOS**](https://github.com/upbit/PixivAPI_iOS)

## API functions

### App-API (6.0 - app-api.pixiv.net)

~~~python
class AppPixivAPI(BasePixivAPI):

    # ?????????????????????
    def parse_qs(self, next_url):

    # ???????????? (????????????)
    def user_detail(self, user_id):

    # ?????????????????? (????????????)
    def user_illusts(self, user_id, type='illust'):

    # ???????????????????????? (????????????)
    def user_bookmarks_illust(self, user_id, restrict='public'):

    # ?????????????????????
    # restrict: [public, private]
    def illust_follow(self, restrict='public'):

    # ???????????? (??????????????????PAPI.works)
    def illust_detail(self, illust_id):

    # ?????????????????? (????????????)
    def illust_related(self, illust_id):

    # ???????????? (Home - Main) (????????????)
    # content_type: [illust, manga]
    def illust_recommended(self, content_type='illust'):

    # ????????????
    # mode: [day, week, month, day_male, day_female, week_original, week_rookie, day_manga]
    # date: '2016-08-01'
    # mode(r18???????????????): [day_r18, day_male_r18, day_female_r18, week_r18, week_r18g]
    def illust_ranking(self, mode='day', date=None, offset=None):

    # ???????????? (Search - tags) (????????????)
    def trending_tags_illust(self):

    # ?????? (Search) (????????????)
    # search_target - ????????????
    #   partial_match_for_tags  - ??????????????????
    #   exact_match_for_tags    - ??????????????????
    #   title_and_caption       - ???????????????
    # sort: [date_desc, date_asc]
    # duration: [within_last_day, within_last_week, within_last_month]
    def search_illust(self, word, search_target='partial_match_for_tags', sort='date_desc', duration=None):

    # ?????????????????? (????????????)
    def illust_bookmark_detail(self, illust_id):

    # ????????????
    def illust_bookmark_add(self, illust_id, restrict='public', tags=None):

    # ????????????
    def illust_bookmark_delete(self, illust_id):

    # ????????????????????????
    def user_bookmark_tags_illust(self, restrict='public', offset=None):

    # Following???????????? (????????????)
    def user_following(self, user_id, restrict='public', offset=None):

    # Followers???????????? (????????????)
    def user_follower(self, user_id, filter='for_ios', offset=None):

    # ???P??? (????????????)
    def user_mypixiv(self, user_id, offset=None):

    # ??????????????? (????????????)
    def user_list(self, user_id, filter='for_ios', offset=None):

    # ??????ugoira??????
    def ugoira_metadata(self, illust_id):
~~~

[Usage](https://github.com/upbit/pixivpy/blob/master/demo.py#L42):

~~~python
aapi = AppPixivAPI()

# ????????????
json_result = aapi.illust_recommended()
print(json_result)
illust = json_result.illusts[0]
print(">>> %s, origin url: %s" % (illust.title, illust.image_urls['large']))

# ??????????????????
json_result = aapi.illust_related(57065990)
print(json_result)
illust = json_result.illusts[0]
print(">>> %s, origin url: %s" % (illust.title, illust.image_urls['large']))

# ??????????????????-????????? (.parse_qs(next_url) ??????)
next_qs = aapi.parse_qs(json_result.next_url)
json_result = aapi.illust_related(**next_qs)
print(json_result)
illust = json_result.illusts[0]
print(">>> %s, origin url: %s" % (illust.title, illust.image_urls['large']))

# ????????????
json_result = aapi.user_detail(660788)
print(json_result)
user = json_result.user
print("%s(@%s) region=%s" % (user.name, user.account, json_result.profile.region))

# ??????????????????
json_result = aapi.user_illusts(660788)
print(json_result)
illust = json_result.illusts[0]
print(">>> %s, origin url: %s" % (illust.title, illust.image_urls['large']))

# ??????????????????
json_result = aapi.user_bookmarks_illust(2088434)
print(json_result)
illust = json_result.illusts[0]
print(">>> %s, origin url: %s" % (illust.title, illust.image_urls['large']))

# 2016-07-15 ????????????????????????
json_result = aapi.illust_ranking('week', date='2016-07-15')
print(json_result)
illust = json_result.illusts[0]
print(">>> %s, origin url: %s" % (illust.title, illust.image_urls['large']))

# ????????????????????? (??????login)
json_result = aapi.illust_follow(req_auth=True)
print(json_result)
illust = json_result.illusts[0]
print(">>> %s, origin url: %s" % (illust.title, illust.image_urls['large']))

# ?????? "??????" ??????
json_result = aapi.search_illust('??????', search_target='partial_match_for_tags')
print(json_result)
illust = json_result.illusts[0]
print(">>> %s, origin url: %s" % (illust.title, illust.image_urls['large']))
~~~

### Public-API

[PAPI](https://github.com/upbit/pixivpy/blob/master/pixivpy3/api.py).*

~~~python
class PixivAPI(BasePixivAPI):

	# ????????????
	def works(self, illust_id):

	# ????????????
	def users(self, author_id):

	# ????????????
	def me_feeds(self, show_r18=1):

	# ???????????????
	def me_favorite_works(self,page=1,per_page=50,image_sizes=['px_128x128', 'px_480mw', 'large']):

	# ????????????
	# publicity:  public, private
	def me_favorite_works_add(self, work_id, publicity='public'):

	# ????????????
	def me_favorite_works_delete(self, ids):

	# ????????????
	# publicity:  public, private
	def me_favorite_users_follow(self, user_id, publicity='public'):

	# ????????????
	# publicity:  public, private
	def users_works(self, author_id, page=1, per_page=30, publicity='public'):

	# ????????????
	# publicity:  public, private
	def users_favorite_works(self, author_id, page=1, per_page=30, publicity='public'):

	# ?????????/???????????????
	# mode:
	#   daily - ??????
	#   weekly - ??????
	#   monthly - ??????
	#   male - ????????????
	#   female - ????????????
	#   original - ??????
	#   rookie - Rookie
	#   daily_r18 - R18??????
	#   weekly_r18 - R18??????
	#   male_r18
	#   female_r18
	#   r18g
	# page: 1-n
	# date: '2015-04-01' (??????????????????)
	def ranking_all(self, mode='daily', page=1, per_page=50, date=None):

	# ??????
	# query: ???????????????
	# page: 1-n
	# mode:
	#   text - ??????/??????
	#   tag - ???????????????
	#   exact_tag - ????????????
	#   caption - ??????
	# period (only applies to asc order):  
	#   all - ??????
	#   day - ????????????
	#   week - ????????????
	#   month - ????????????
	# order:
	#   desc - ?????????
	#   asc - ?????????
	def search_works(self, query, page=1, per_page=30, mode='text',
		period='all', order='desc', sort='date'):

~~~

[Usage](https://github.com/upbit/pixivpy/blob/master/demo.py#L42):

~~~python
# ???????????? PAPI.works
json_result = api.works(46363414)
print(json_result)
illust = json_result.response[0]
print( ">>> %s, origin url: %s" % (illust.caption, illust.image_urls['large']))

# ???????????? PAPI.users
json_result = api.users(1184799)
print(json_result)
user = json_result.response[0]
print(user.profile.introduction)

# ???????????? PAPI.me_feeds
json_result = api.me_feeds(show_r18=0)
print(json_result)
ref_work = json_result.response[0].ref_work
print(ref_work.title)

# ??????????????????(private) PAPI.me_favorite_works
json_result = api.me_favorite_works(publicity='private')
print(json_result)
illust = json_result.response[0].work
print("[%s] %s: %s" % (illust.user.name, illust.title, illust.image_urls.px_480mw))

# ??????????????????[New -> Follow] PAPI.me_following_works
json_result = api.me_following_works()
print(json_result)
illust = json_result.response[0]
print(">>> %s, origin url: %s" % (illust.caption, illust.image_urls['large']))

# ?????????????????? PAPI.me_following
json_result = api.me_following()
print(json_result)
user = json_result.response[0]
print(user.name)

# ???????????? PAPI.users_works
json_result = api.users_works(1184799)
print(json_result)
illust = json_result.response[0]
print(">>> %s, origin url: %s" % (illust.caption, illust.image_urls['large']))

# ???????????? PAPI.users_favorite_works
json_result = api.users_favorite_works(1184799)
print(json_result)
illust = json_result.response[0].work
print(">>> %s origin url: %s" % (illust.caption, illust.image_urls['large']))

# ??????????????? PAPI.me_favorite_works
json_result = api.me_favorite_works()
print(json_result)
ids = json_result.response[0].id

# ???????????? PAPI.me_favorite_works_add
json_result = api.me_favorite_works_add(46363414)
print(json_result)

# ???????????? PAPI.me_favorite_works_delete
json_result = api.me_favorite_works_delete(ids)
print(json_result)

# ???????????? PAPI.me_favorite_users_follow
json_result = api.me_favorite_users_follow(1184799)
print(json_result)

# ????????? PAPI.ranking(illust)
json_result = api.ranking('illust', 'weekly', 1)
print(json_result)
illust = json_result.response[0].works[0].work
print(">>> %s origin url: %s" % (illust.title, illust.image_urls['large']))

# ??????????????? PAPI.ranking(all, 2015-05-01)
json_result = api.ranking(ranking_type='all', mode='daily', page=1, date='2015-05-01')
print(json_result)
illust = json_result.response[0].works[0].work
print(">>> %s origin url: %s" % (illust.title, illust.image_urls['large']))

# ??????(text)/??????(exact_tag)?????? PAPI.search_works
#json_result = api.search_works("????????? ??????", page=1, mode='text')
json_result = api.search_works("?????????", page=1, mode='exact_tag')
print(json_result)
illust = json_result.response[0]
print(">>> %s origin url: %s" % (illust.title, illust.image_urls['large']))

# ??????????????????[New -> Everyone] PAPI.latest_works
json_result = api.latest_works()
print(json_result)
illust = json_result.response[0]
print(">>> %s url: %s" % (illust.title, illust.image_urls.px_480mw))
~~~

## License

Feel free to use, reuse and abuse the code in this project.
