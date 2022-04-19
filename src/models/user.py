# -*- coding:utf-8 -*-
from . import db, Base


class User(db.Model, Base):
    __tablename__ = 'users'
    name = db.Column(db.VARCHAR(50), nullable=False)
    email = db.Column(db.VARCHAR(100), nullable=False)
    is_active = db.Column(db.Integer, nullable=False, default=0)

    @classmethod
    def get_users(cls):
        data_list = list()
        result = db.session.query(cls).all()
        for item in result:
            user_info = cls.to_dict(item)
            data_list.append(user_info)
        return data_list
