# -*- coding:utf-8 -*-
from flask import Blueprint, request
from flask_restful import Api as Api_
from src.data_format import ResMsg
from src.settings import config

class Api(Api_):
    """
    重写handle_error, 当app.run(debug=False)时生效
    """
    def handle_error(self, e):
        if isinstance(e, Exception):
            from traceback import format_exc
            print(format_exc())
            if request.method.upper() != "GET":
                data = request.get_data()
            else:
                data = ''
            # 消息通知开发人员，按需配置
            return ResMsg(success=False, msg=str(e) or config.SYSTEM_ERROR_MSG).data

base_api_bp = Blueprint('base', __name__, url_prefix='')
base_api = Api(base_api_bp)

from src.views import base
