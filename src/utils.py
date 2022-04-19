# -*- coding:utf-8 -*-
import os
import uuid
import redis
import decimal
import logging
import datetime
from logging.handlers import RotatingFileHandler
from flask.json import JSONEncoder as BaseJSONEncoder


class Redis(object):

    @staticmethod
    def get_redis(conf):
        cache = redis.StrictRedis(**conf)
        return cache


def connect_redis(**conf):
    from redis import StrictRedis
    return StrictRedis(**conf)


def setup_log(filename):
    if not os.path.exists(os.path.join(os.path.split(os.path.realpath(__file__))[0], 'logs')):
        os.mkdir(os.path.join(os.path.split(os.path.realpath(__file__))[0], 'logs'))

        # 设置日志的登记
        logging.basicConfig(level=logging.DEBUG)
        # 创建日志记录器， 设置日志的保存路径和每个日志的大小和日志的总大小
        file_log_handler = RotatingFileHandler(
            os.path.join(os.path.split(os.path.realpath(__file__))[0], 'logs/{}.log'.format(filename)),
            maxBytes=1024 * 1024 * 100, backupCount=100)
        # 创建日志记录格式，日志等级，输出日志的文件名 行数 日志信息
        formatter = logging.Formatter(
            "%(asctime)s [%(threadName)s:%(thread)d] [%(pathname)s:%(lineno)d] [%(module)s:%(funcName)s] [%(levelname)s] - %(message)s")
        # 为日志记录器设置记录格式
        file_log_handler.setFormatter(formatter)
        # 为全局的日志工具对象（flask app使用的）加载日志记录器
        logging.getLogger().addHandler(file_log_handler)


class JSONEncoder(BaseJSONEncoder):
    """
    重写default方法， 支持更多的转换方法
    """

    def default(self, o):
        """
        如果有其他的需求直接在下面添加
        :param o:
        :return:
        """
        if isinstance(o, datetime.datetime):
            # 格式化时间
            return o.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(o, datetime.date):
            # 格式化日期
            return o.strftime("%Y-%m-%d")
        if isinstance(o, decimal.Decimal):
            # 格式化高精度数字
            return str(o)
        if isinstance(o, uuid.UUID):
            # 格式化uuid
            return str(o)
        if isinstance(o, bytes):
            # 格式化字节数据
            return o.decode('utf-8')
        return super(JSONEncoder, self).default(o)
