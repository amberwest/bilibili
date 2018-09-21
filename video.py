# -*- coding:utf-8 -*-
# Time: 2018/9/7 11:02

import json

import re

import requests
import sys
import os

import time
import urllib3
from scrapy import Selector

from utils import create_folder, concatenate, get_page, parse_url
from setting import BASE_DIR

urllib3.disable_warnings()

class BiliDownload(object):
    """
    初始化时传入视频id即可下载视频，默认存储在当前目录下的video文件夹，也可以自己传入新的目录
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    }
    def __init__(self, aid, dest='video'):
        self.aid = aid
        self.dest = os.path.join(BASE_DIR, dest)
        self.info = ''

    def get_vedio_info(self):
        """获取视频相关信息,aid，cid，点赞数等等"""
        url = "https://api.bilibili.com/x/web-interface/view"
        para = {
            'aid': str(self.aid),
        }
        res = get_page(url, params=para)
        self.info = res.json()
        title = self.info['data']['title']
        # 创建文件夹
        create_folder(os.path.join(BASE_DIR, title))

    def get_danmu(self):
        # 弹幕,oid在视频相关信息json中是cid字段
        cid = self.info['data']['cid']
        danmu_url = 'https://api.bilibili.com/x/v1/dm/list.so?oid={}'.format(cid)

        res = get_page(danmu_url)
        danmu = []
        try:
            response = res.content.decode('utf-8')
            selector = Selector(text=response)
            for d in selector.css('d'):
                txt = d.css('::text').extract_first()
                danmu.append({'txt': txt})
        except Exception as e:
            print(e)

    def download_video(self):
        """从视频页面获取到视频链接进行下载"""
        # video_url = 'https://www.bilibili.com/video/av28518492'

        self.get_vedio_info()
        title = self.info['data']['title']

        video_url = 'https://www.bilibili.com/video/av{}'.format(str(self.aid))
        res = get_page(video_url, header=self.headers, **{'verify':False})

        # 从网页源码获取视频链接
        origin_txt = re.findall(r'<script>window.__playinfo__=(\{.*?\})</script>', res.text, re.S)[0]
        origin_json = json.loads(origin_txt, encoding='utf-8')
        urls = origin_json['durl']

        size = 0
        chunk = 1024
        content_size = sum([i['size'] for i in urls])
        print('文件大小： %0.2fMB' % (content_size / chunk / 1024))

        start = time.time()

        # 循环下载视频
        for i, data in enumerate(urls):
            url = data['url']
            header = {
                'Origin': 'https://www.bilibili.com', 'Referer': video_url,
            }
            try:
                # 请求视频链接
                response = get_page(url, header=header, **{
                    'verify': False, 'stream': True
                })
                video_path = title + '/' + '{}.mp4'.format(i)
                # 下载视频
                with open(video_path, 'wb') as file:
                    for item in response.iter_content(chunk):
                        file.write(item)
                        file.flush()
                        size += len(item)
                        print('\r' + '[下载进度]：%s %0.2f%%' % (
                            '>' * int(size * 50 / content_size), float(size / content_size) * 100), end='')

            except Exception as e:
                print(e)
        stop = time.time()
        print('\n' + '视频下载完成，耗时%.2f秒' % (stop - start))
        # 合并视频
        concatenate(path=title, dest=self.dest)

if __name__ == '__main__':
    # aid = sys.argv[1] 31705434    25249   28518492 19852845
    aid = '19852845'
    bili = BiliDownload(aid)
    bili.download_video()  # bili.get_vedio_info()  # bili.get_danmu()
