# -*- coding:utf-8 -*-
# Time: 2018/9/13 10:08
from datetime import datetime
from sqlalchemy import Column, String, ForeignKey, Integer, DateTime, Text
from sqlalchemy.orm import relationship
from db.base import Base, engine


class Video(Base):
    """已下载视频的存储信息"""
    __tablename__ = 'video'

    # 数据库id
    id = Column(Integer, primary_key=True)
    # 视频名称
    title = Column(String(100))
    # 视频链接
    url = Column(String(200))
    # 视频保存路径
    path = Column(String(200))
    # 视频添加时间
    time_created = Column(DateTime(), default=datetime.now)
    # 外键，通过视频信息表的id找到aid
    info_id = Column(Integer, ForeignKey('videoinfo.id'))
    # 与视频信息表是一对一，uselist=False, 信息表可以通过video属性访问到视频内容，back_populates需要两边都设置
    info = relationship('VideoInfo', back_populates='video', uselist=False)


class VideoInfo(Base):
    """视频信息表"""
    __tablename__ = 'videoinfo'

    id = Column(Integer, primary_key=True)
    # 视频标题
    title = Column(String(200))
    # 视频封面
    pic = Column(String(200))
    # 弹幕数量
    danmaku = Column(String(30))
    # 不喜欢的数量
    dislike = Column(String(30))
    # 喜欢的数量
    like = Column(String(30))
    # 观看次数
    view = Column(String(30))
    # 回复次数
    reply = Column(String(30))
    # 分享次数
    share = Column(String(30))
    # 投币数
    coin = Column(String(30))
    # 收藏数
    favorite = Column(String(30))
    # 视频id，加上类型的，是视频表的外键
    aid = Column(String(30), nullable=False, unique=True)
    # 视频类型？
    tname = Column(String(50))
    # 视频上传时间
    pubdate = Column(String(20))
    # up主id
    owner_id = Column(String(30))
    # up主昵称
    owner_name = Column(String(100))
    # up主头像
    owner_face = Column(String(200))
    # 弹幕库id，也就是cid字段，是弹幕库表的外键
    danmaku_id = Column(String(30), nullable=False)
    # 添加时间
    time_created = Column(DateTime(), default=datetime.now)
    # 更新时间
    time_updated = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    # 跟video表是一对一关系
    video = relationship('Video', back_populates="info")
    # 跟danmu表是一对多关系
    danmu = relationship('Danmu', back_populates="info")


class Danmu(Base):
    """视频相关的弹幕内容，跟VideoInfo表是多对一的关系"""
    __tablename__ = "danmu"

    id = Column(Integer, primary_key=True)
    # 单条弹幕
    danmu = Column(Text)
    time_created = Column(DateTime(), default=datetime.now)
    time_updated = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    # 跟信息表是多对一的关系，tablename.column_name
    info_id = Column(Integer, ForeignKey('videoinfo.id'))
    info = relationship('VideoInfo', back_populates='danmu')


if __name__ == '__main__':
    # 创建表格
    Base.metadata.create_all(engine)
