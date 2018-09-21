# -*- coding:utf-8 -*-

import urllib3

urllib3.disable_warnings()

headers = {
    'Host': 'api.bilibili.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
}

url = 'https://api.bilibili.com/x/web-interface/dynamic/total?callback=dynamic_total&jsonp=jsonp'
# 粉丝列表
follower_url = 'https://api.bilibili.com/x/relation/followers?vmid=7714&pn=1&ps=20&order=desc&jsonp=jsonp&callback=__jp6'
# 关注者列表
following_url = 'https://api.bilibili.com/x/relation/followings?vmid=11456569&pn=2&ps=20&order=desc&jsonp=jsonp&callback=__jp5'
