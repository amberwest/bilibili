# -*- coding:utf-8 -*-
import json
from pprint import pprint

import re
import urllib3
import requests
from bs4 import BeautifulSoup as soup

from utils import create_folder

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

def get_danmu():
    # 弹幕,oid在视频相关信息json中是cid字段
    danmu_url = 'https://api.bilibili.com/x/v1/dm/list.so'
    danmu_params = {
        'oid': '49355487'
    }
    res = requests.get(danmu_url, params=danmu_params, headers=headers, verify=False)
    try:
        response = res.content.decode('utf-8')
        print(response)
    except Exception as e:
        print(e)

def get_vedio_info():
    """获取视频相关信息,aid，cid，点赞数等等"""
    url = "https://api.bilibili.com/x/web-interface/view"
    para = {
        'aid': '28518492',  # av后面跟着的ID
    }
    res = requests.get(url, params=para, headers=headers, verify=False)
    title=res.json()['data']['title']
    print(res.json()['data']['cid'])        # 弹幕cid参数
    print(title)
    create_folder(title)

get_vedio_info()