# -*- coding:utf-8 -*-
# Time: 2018/9/15 18:24
"""
入口函数，终端运行：python3 run.py url即可下载视频及保存相关信息
"""
from video import VideoDownload
from db.inserts import insert
from db.update import update
from db.base import Session
from db.models import VideoInfo


def run(url):
    session = Session()
    # 1、抓取视频信息
    info = VideoDownload.get_vedio_info(url)
    aid = info['data']['stat']['aid']
    print(info)

    # TODO: 2、判断视频是否已存在
    # video_exist = session.query(VideoInfo).filter(VideoInfo.aid == aid).first()
    video_exist = False
    if video_exist:
        # 2.1 存在则更新信息表和弹幕表
        cid = info['data']['cid']
        danmu = VideoDownload.get_danmu(cid)
        print(danmu)
        # update(info, danmu)

    else:
        # 2.2 不存在则下载视频并保存三个表的信息
        cid = info['data']['cid']
        danmu = VideoDownload.get_danmu(cid)
        title = info['data']['title']
        video = VideoDownload.download_video(url, title)
        print(danmu)
        print(video)
        # insert(info, danmu, video)

if __name__ == '__main__':
    video_url = 'https://www.bilibili.com/video/av28518492'
    run(video_url)