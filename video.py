# -*- coding:utf-8 -*-
# Time: 2018/9/7 11:02

import json

import re

import requests
import sys

import time
import urllib3

from utils import create_folder, concatenate

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
        self.dest = dest
        self.title = ''

    def get_vedio_info(self):
        """获取视频相关信息,aid，cid，点赞数等等"""
        url = "https://api.bilibili.com/x/web-interface/view"
        para = {
            'aid': str(self.aid),  # av后面跟着的ID
        }
        res = requests.get(url, params=para, headers=self.headers, verify=False)
        self.title = res.json()['data']['title']
        # 创建文件夹
        create_folder(self.title)

    def download_video(self):
        """从视频页面获取到视频链接进行下载"""
        # video_url = 'https://www.bilibili.com/video/av28518492'

        self.get_vedio_info()
        video_url = 'https://www.bilibili.com/video/av{}'.format(str(self.aid))
        res = requests.get(video_url, headers=self.headers, verify=False)
        origin_txt = re.findall(r'<script>window.__playinfo__=(\{.*?\})</script>', res.text, re.S)[0]
        origin_json = json.loads(origin_txt, encoding='utf-8')
        urls = origin_json['durl']

        size = 0
        chunk = 1024
        content_size = sum([i['size'] for i in urls])
        print('file size is %0.2f MB' % (content_size / chunk / 1024))

        start = time.time()
        # 循环下载视频
        for i, data in enumerate(urls):
            url = data['url']
            header = {
                'Origin': 'https://www.bilibili.com',
                'Referer': video_url,
            }
            self.headers.update(header)
            try:
                response = requests.get(url, headers=self.headers, verify=False, stream=True)
                video_path = self.title + '/' + '{}.mp4'.format(i)
                # 下载视频
                with open(video_path, 'wb') as file:
                    for item in response.iter_content(chunk):
                        file.write(item)
                        file.flush()
                        size += len(item)
                        print('\r' + '[下载进度]：%s %0.2f%%' % ('>' * int(size * 50 / content_size), float(size / content_size) * 100), end='')

            except Exception as e:
                print(e)
        stop = time.time()
        print('\n' + '视频下载完成，耗时%.2f秒' % (stop-start))
        # 合并视频
        concatenate(path=self.title, dest=self.dest)

if __name__ == '__main__':
    # aid = sys.argv[1], '28518492', '17882115'
    for aid in ['28518492']:
        bili = BiliDownload(aid)
        bili.download_video()