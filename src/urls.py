# -*- coding:utf-8 -*-
from flask import Blueprint
from flask_restful import Api

base_api_bp = Blueprint('base', __name__, url_prefix='')
base_api = Api(base_api_bp)

from src.views import base
