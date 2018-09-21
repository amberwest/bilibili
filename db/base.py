# -*- coding:utf-8 -*-
# Time: 2018/9/16 14:19

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from setting import *

# 创建基类，在model文件中再创建table
Base = declarative_base()

engine_string = 'mysql+pymysql://{user}:{pwd}@{host}/{db}?charset={charset}'.format(
    user=MYSQL_USER,
    pwd=MYSQL_PASSWORD,
    host=MYSQL_HOST,
    db=MYSQL_DB,
    charset=MYSQL_CHARSET
)

# 创建engine实例
engine = create_engine(engine_string,
                       pool_size=1,
                       max_overflow=10,
                       echo=True,
                       encoding='utf-8',
                       pool_recycle=200000,
                       )

# 创建会话类
Session = sessionmaker(bind=engine)
