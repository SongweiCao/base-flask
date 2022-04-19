# -*- coding:utf-8 -*-
from flask import request
from flask_cors import CORS
from src import create_app
from src.data_format import ResMsg
from src.libs.extends import record_request_info, check_sign
import logging as logger

app = create_app()
CORS(app, supports_credentials=True, resources=r'/*', allow_headers='content_type, x-timestamp, x-signature')


@app.before_request
def before_request_func():
    request_params = record_request_info()
    # 检查签名不用可删掉
    # check_res = check_sign(request_params)
    # if not check_res.get_success:
    #     return check_res.data


@app.after_request
def add_header(response):
    if response.status_code != 200 and response.status_code != 302:
        data = '{}'
        if request.method.upper() != 'GET':
            data = request.get_data()
        for receiver in app.config['POPO_RECEIVERS']:
            # send_steam(receiver, app.config['ERROR_MSG'].format(app.config['NAME'], request.method, request.url, response.status_code, data,response.data).decode('utf-8'))
            pass
    response.headers['Access-Control-Allow-Headers'] = 'x-timestamp, x-signature'  # 自定义headers按需求修改
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:5050'  # allow origin 按需求修改
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response


@app.errorhandler(404)
def page_not_found(error):
    return ResMsg(success=False, msg=app.config['URL_NOT_FOUND_MSG']).data


@app.errorhandler(Exception)
def error_handler(e):
    from traceback import format_exc
    print(format_exc())
    if request.method.upper() != 'GET':
        data = request.get_data()
    else:
        data = ''
    for receiver in app.config['POPO_RECEIVERS']:
        (receiver,
         app.config['ERROR_MSG'].format(app.config['NAME'], request.method, request.url, 200, data, str(e)).decode(
             'utf-8'))
    return ResMsg(success=False, msg=str(e) or app.config['SYSTEM_ERROR_MSG']).data


application = app
if __name__ == '__main__':
    app.run(host='127.0.0.1', port='5050', debug=True)
