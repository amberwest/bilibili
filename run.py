# -*- coding:utf-8 -*-
# Time: 2018/9/15 18:24
"""
入口函数，终端运行：python3 run.py url即可下载视频及保存相关信息
"""
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

from video import VideoDownload
from db.inserts import insert
from db.update import update

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
            update(info, danmu)
        else:
            # 2.2 不存在则添加信息表、弹幕表，同时下载视频
            danmu = VideoDownload.get_danmu(cid)
            video = VideoDownload.download_video(url)
            insert(info, danmu, video)


def insert_info_and_danmu(url, m, n):
    """使用线程池抓取视频信息和弹幕"""
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(VideoDownload.get_vedio_info, url.format(aid)) for aid in
                   range(m, n)]
        for future in as_completed(futures):
            info = future.result()  # return None or a requests Response
            if info and info.json()['data']:
                print(info.json())
                cid = info.json()['data'].get('cid')
                if cid:
                    danmu = VideoDownload.get_danmu(cid)
                    print(danmu)
                    insert(info.json(), danmu)

# if __name__ == '__main__':
#     video_url = 'https://www.bilibili.com/video/av{}'
#     for i in range(1042060, 1100000, 500):
#         insert_info_and_danmu(video_url, i, i+500)

