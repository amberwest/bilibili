# -*- coding:utf-8 -*-
# Time: 2018/9/7 11:02

import json

import re

import os

import time
import urllib3
from scrapy import Selector

from utils import create_folder, concatenate, get_page, parse_url
from setting import BASE_DIR

urllib3.disable_warnings()

class VideoDownload(object):
    """
    初始化时传入视频url即可下载视频，默认存储在当前目录下的video文件夹，也可以自己传入新的目录
    """

    @classmethod
    def get_vedio_info(cls, url):
        """获取视频相关信息,aid，cid，点赞数等等"""
        aid = re.sub('[a-z]+', '', parse_url(url))
        url = "https://api.bilibili.com/x/web-interface/view"
        para = {
            'aid': aid,
        }
        res = get_page(url, params=para)
        info = res.json()
        return info

    @classmethod
    def get_danmu(cls, cid):
        """获取视频对应的弹幕信息"""
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
        return danmu

    # TODO: 目前只能抓取类似'https://www.bilibili.com/video/av28518492'的链接
    @classmethod
    def download_video(cls, page_url, title, dest='video'):
        """从视频页面获取到视频链接进行下载"""
        res = get_page(page_url, **{'verify': False})

        # 从网页源码获取视频链接
        origin_txt = re.findall(r'<script>window.__playinfo__=(\{.*?\})</script>', res.text, re.S)[0]
        origin_json = json.loads(origin_txt, encoding='utf-8')
        urls = origin_json['durl']

        # 下载视频
        size = 0
        chunk = 1024
        content_size = sum([i['size'] for i in urls])
        print('文件大小： %0.2fMB' % (content_size / chunk / 1024))

        # 创建存放视频临时文件夹
        create_folder(os.path.join(BASE_DIR, title))

        start = time.time()

        # 循环下载视频
        for i, data in enumerate(urls):
            url = data['url']
            header = {
                'Origin': 'https://www.bilibili.com',
                'Referer': page_url,
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
        dest = os.path.join(BASE_DIR, dest)
        video_save_path = concatenate(path=title, dest=dest)

        video = {
            'title': title,
            'url': page_url,
            'path': video_save_path
        }
        return video
