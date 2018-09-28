# -*- coding:utf-8 -*-
# Time: 2018/9/20 15:06

from db.base import Session
from db.models import Video, VideoInfo, Danmu
from utils import session_scope


def insert(info, danmu, video=None):
    """持久化到mysql"""
    # 信息表
    stat = info['data']['stat']
    data = info['data']
    i = VideoInfo(title=data['title'],
                     pic=data['pic'],
                     danmaku=stat['danmaku'],
                     dislike=stat['dislike'],
                     like=stat['like'],
                     view=stat['view'],
                     reply=stat['reply'],
                     share=stat['share'],
                     coin=stat['coin'],
                     favorite=stat['favorite'],
                     aid=stat['aid'],
                     tname=data['tname'],
                     owner_id=data['owner']['mid'],
                     owner_face=data['owner']['face'],
                     owner_name=data['owner']['name'],
                     danmaku_id=data['cid'],
                     pubdate=data['pubdate']
                     )

    # 弹幕表
    res = []
    for item in danmu:
        d = Danmu(danmu=item['txt'],
                  info=i)
        res.append(d)

    if video:
        # 视频表
        v = Video(title=video['title'],
                  path=video['path'],
                  url=video['url'],
                  info=i,
                      )

        with session_scope(Session) as session:
            session.add(i)
            session.add_all(res)
            session.add(v)
    with session_scope(Session) as session:
        session.add(i)
        session.add_all(res)

