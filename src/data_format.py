# -*- coding:utf-8 -*-
import json
from flask import make_response, request


class ResMsg(object):
    """
    构建服务响应的返回值
    """

    def __init__(self, success=True, msg='ok', data=None):
        self._success = success
        self._msg = msg
        self._data = data

    def update(self, success=None, msg=None, data=None):
        if success is not None:
            self._success = success
        if msg is not None:
            self._msg = msg

        if data is not None:
            self._data = data

    @property
    def data(self):
        body = self.__dict__
        body['success'] = body.pop('_success')
        body['data'] = body.pop('_data')
        if body['success']:
            body.pop('_msg')
        else:
            body['msg'] = body.pop('_msg')
        callback = request.args.get('callback', None)
        if callback:
            res = callback + "(" + json.dumps(body) + ")"
            content_type = 'application/javascript'
        else:
            res = body
            content_type = 'application/json'
        response = make_response(res)
        response.headers['Content_Type'] = content_type
        return response

    @property
    def get_success(self):
        return self.__dict__['_success']
