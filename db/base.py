# -*- coding:utf-8 -*-
# Time: 2018/9/16 14:19

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from setting import *

# 创建基类，在model文件中再创建table
Base = declarative_base()

# 创建engine实例
engine_string = 'mysql+pymysql://{user}:{pwd}@{host}/{db}?charset={charset}'.format(
    user=MYSQL_USER,
    pwd=MYSQL_PASSWORD,
    host=MYSQL_HOST,
    db=MYSQL_DB,
    charset=MYSQL_CHARSET
)

engine = create_engine(engine_string,
                       pool_size=1,
                       max_overflow=10,
                       echo=True,
                       encoding='utf-8',
                       pool_recycle=200000,
                       )

# 创建会话类
Session = sessionmaker(bind=engine)
# # 如果还不需要创建实例，可以后面再使用
# Sesison = sessionmaker()
# Sesison.configure(bind=engine)

# # 创建会话对象，需要使用的时候再创建实例
# session = Session()
