# -*- coding:utf-8 -*-
# Time: 2018/9/20 15:06
from contextlib import contextmanager

from db import Base, Session
from models import Video, VideoInfo, Danmu

@contextmanager
def session_scope(Session):
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def save_video(data, info):
    video = Video(title=data['title'],
                  path=data['path'],
                  info_id=info.id,
                  )

    with session_scope(Session) as session:
        session.add(video)


def save_videoinfo(data, danmu):
    stat = data['data']['stat']
    data = data['data']
    info = VideoInfo(title=data['title'],
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
                     # v_type='',  # av3456789前的av，这个怎么设计好呢，麻烦
                     tname=data['tname'],
                     owner_id=data['owner']['mid'],
                     owner_face=data['owner']['face'],
                     owner_name=data['owner']['name'],
                     danmaku_id=data['cid'],
                     pubdate=data['pubdate']
                     )

    with session_scope(Session) as session:
        session.add(info)


def save_danmu(data, info):
    res = []
    for item in data:
        danmu = Danmu(danmu=item['txt'],
                      info_id=info.id)
        res.append(danmu)
    with session_scope(Session) as session:
        session.bulk_save_object(res)


