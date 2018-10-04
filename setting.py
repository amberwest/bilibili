# -*- coding:utf-8 -*-
# Time: 2018/9/13 09:41
import logging
import os

# mysql数据库链接参数
MYSQL_HOST = 'localhost'
MYSQL_PORT= '3306'
MYSQL_PASSWORD = 'bili'
MYSQL_USER = 'bili'
MYSQL_DB = 'bili'
MYSQL_CHARSET = 'utf8mb4'

ECHO=False

# 反爬时休息时间
SLEEP_TIME = 60

# 根目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 设置日志记录器
LOGGER = 'video'
LOGGER_LEVEL = logging.DEBUG