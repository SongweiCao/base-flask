# -*- coding:utf-8 -*-
import os
import redis
import socket
from apscheduler.jobstores.redis import RedisJobStore  # 根据应用程序的需求来，创建定时任务时使用
from secrets import token_hex


class Config:
    NAME = ''  # 应用程序名

    # MYSQL
    DB_HOST = 'localhost'  # 数据库地址
    DB_PORT = '3306'  # 数据库端口
    DB_DATABASE = 'test'  # 数据库名
    DB_USERNAME = 'root'  # 用户名
    DB_PASSWORD = 'wangyi1234'  # 密码

    # redis
    REDIS_HOST = 'localhost'  # redis数据库地址
    REDIS_PORT = '6379'  # redis数据库端口
    REDIS_PASSWORD = ''  # redis数据库密码
    REDIS_DB = '0'  # redis数据库名

    # SQLALCHEMY CONF
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '2a3612de8fc1bcbb1da187ac9278f452'  # 随机生成一个32为的密钥

    # msg
    SIGN_ERROR_MSG = '签名错误，请检查您的参数和签名'
    URL_NOT_FOUND_MSG = 'URL NOT FOUND'
    SYSTEM_ERROR_MSG = '系统错误，请稍候再试'

    POPO_RECEIVERS = []

    # Redis Lock EX & Prefix
    HEALTH_CHECK_INTERVAL = 30
    SOCKET_CONNECT_TIMEOUT = 5
    SOCKET_KEEPALIVE = True
    SOCKET_KEEPALIVE_OPTIONS = {
        socket.TCP_KEEPIDLE: 120,
        socket.TCP_KEEPCNT: 3,
        socket.TCP_KEEPINTVL: 5,
    }

    REDIS_LOCK_PREFIX = 'wanhongLock-'  # redis锁，根据需求进设置
    REDIS_LOCK_EX = 30  # 锁失效的时间， 根据需求来设置

    REDIS_URL = 'redis://:{}@{}:{}/{}'.format(REDIS_PASSWORD, REDIS_HOST, REDIS_PORT, REDIS_DB)
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{username}:{password}@{host}:{port}/{db}?charset=utf8'.format(
        username=DB_USERNAME, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT, db=DB_DATABASE)

    POOL = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=REDIS_DB)
    SCHEDULER_JOBSTORES = {
        'redis': RedisJobStore(connection_pool=POOL, health_check_interval=HEALTH_CHECK_INTERVAL,
                               socket_connect_timeout=SOCKET_CONNECT_TIMEOUT, socket_keepalive=SOCKET_KEEPALIVE,
                               socket_keepalive_options=SOCKET_KEEPALIVE_OPTIONS)
    }
    SCHEDULER_EXECUTORS = {
        'default': {
            'type': 'threadpool',
            'max_workers': 20,
        }
    }
    SCHEDULER_JOB_DEFAULTS = {
        'coalesce': True,
        'max_instances': 1000,
        'misfire_grace_time': 60 * 3
    }
    SCHEDULER_API_ENABLED = True


config = Config()


class RedisLock:
    """
    reids 锁，根据需求进行设置
    """

    def __init__(self):
        self.r = redis.Redis(connection_pool=config.POOL)

    def judge_redis_lock(self, lock_key=None):
        if lock_key:
            res = self.r.set(name=config.REDIS_LOCK_PREFIX + lock_key, value=1, ex=config.REDIS_LOCK_EX, nx=True)
            if res:
                return True
            return False
        return False
