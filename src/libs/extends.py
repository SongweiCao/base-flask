# -*- coding:utf-8 -*-
import json
import hashlib
from functools import wraps
from flask import g, request
from flask_restful import reqparse
from werkzeug.exceptions import BadRequest
from werkzeug.datastructures import ImmutableMultiDict
from src import config
from src.data_format import ResMsg
import logging as logger


class DictParseWrap(object):

    def __init__(self, **kwargs):
        self.unparsed_arguments = None
        self.kwargs = kwargs

    def json(self):
        return self.kwargs


class _DictParse():

    def __init__(self, args):
        self.args = args

    def __call__(self, value):
        if isinstance(value, dict):
            value = DictParseWrap(**value)
        req_parse = reqparse.RequestParser()
        for key, item in self.args.items():
            req_parse.add_argument(key, type=item['type'], required=item.get('required', False),
                                   action=item.get('action'), )
        try:
            res = req_parse.parse_args(req=value)
            return True, res

        except BadRequest as e:
            error_msg = getattr(e, 'data', {}).get('message')
            error_msg = str(error_msg) if error_msg else e
            return False, error_msg


def _reqparse(schema):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            flag, req_args = _DictParse(schema)(g.params)
            if not flag:
                return ResMsg(success=False, msg=req_args).data
            if not hasattr(g, 'data'):
                g.data = {}
            g.data = dict(req_args)
            return f(*args, **kwargs)

        return decorated

    return decorator


def record_request_info():
    def _get_json(data):
        try:
            new = data.replace("'", '"')
            new = json.loads(new)
            return new
        except ValueError as e:
            return data

    forward_ips = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    cur_ip = list(map(str.strip, forward_ips.split(",")))[0]
    cur_url = request.url
    cur_method = request.method.upper()
    if cur_method == "GET":
        params = ImmutableMultiDict(request.args).to_dict()
        for key, item in params.items():
            params[key] = _get_json(item)
        logger.info('IP: {} URL: {} METHOD: {} 参数: {}'.format(cur_ip, cur_url, cur_method, json.dumps(params)))
    else:
        try:
            params = json.loads(request.get_data())
            logger.info('IP: {} URL: {} METHOD: {} 参数: {}'.format(cur_ip, cur_url, cur_method, json.dumps(params)))
        except ValueError as e:
            params = request.get_data()
            logger.info('IP: {} URL: {} METHOD: {} 参数: {}'.format(cur_ip, cur_url, cur_method, json.dumps(params)))
    g.params = params
    return params


def check_sign(params):
    res = ResMsg()
    error_res = ResMsg(success=False, msg=config.SIGN_ERROR_MSG)
    # get timestamp and sign
    t, sign = request.headers.get('X-timestamp', None), request.headers.get('X-Signature', None)
    if not (t and sign):
        return error_res.data

    # splice sign string
    sign_str = ''
    params['t'] = t
    key_list = params.keys()
    key_list.sort()
    for key in key_list:
        sign_str += params[key]
    sign_str += config.SECRET_KEY
    # check sign
    if hashlib.sha1(sign_str).hexdigest() != sign:
        return error_res.data
    return res.data
