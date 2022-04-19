# -*- coding:utf-8 -*-
import datetime
from src import db


class Base(object):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    # 创建时间
    create_time = db.Column(db.DateTime, default=datetime.datetime.now, nullable=False)
    # 更新时间
    update_time = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, nullable=False)

    def __init__(self):
        self.__table__ = None

    def to_dict(self, not_key_list=[]):
        result = {}
        for key in self.__mapper__.c.keys():
            if key in not_key_list:
                pass
            else:
                result[key] = getattr(self, key)
        return result
