# -*- coding:utf-8 -*-
from flask_restful import Resource
from src.urls import base_api
from src.data_format import ResMsg
from src.models.user import User


@base_api.resource("/")
class Index(Resource):
    def get(self):
        res = ResMsg()
        user_list = User.get_users()
        res.update(data={'user_list': user_list})
        return res.data
