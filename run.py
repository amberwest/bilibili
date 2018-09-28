# -*- coding:utf-8 -*-
# Time: 2018/9/15 18:24
"""
入口函数，终端运行：python3 run.py url即可下载视频及保存相关信息
"""
import time

from video import VideoDownload
from db.inserts import insert


def run(url):
    # 1、抓取视频信息
    res = VideoDownload.get_vedio_info(url)
    if res and res.json()['data']:
        info = res.json()
        print(info)
        cid = info['data']['cid']

        # TODO: 2、判断视频是否已存在
        video_exist = True
        if video_exist:
            # 2.1 存在则更新信息表和弹幕表
            danmu = VideoDownload.get_danmu(cid)
            insert(info, danmu)


if __name__ == '__main__':
    for i in range(2800010, 38518492):
        time.sleep(0.5)
        video_url = f'https://www.bilibili.com/video/av{i}'
        print(video_url)
        run(video_url)