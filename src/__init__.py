# -*- coding:utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import import_string
from .settings import config
from .utils import JSONEncoder
from .libs.redis_session import RedisSessionInterface
from flask_apscheduler import APScheduler

db = SQLAlchemy()
scheduler = APScheduler()
blueprints = ['src.urls:base_api_bp']

redis_conf = {
    'host': config.REDIS_HOST,
    'port': config.REDIS_PORT,
    'password': config.REDIS_PASSWORD,
    'db': config.REDIS_DB
}


def create_app():
    import logging
    logging.basicConfig()
    app = Flask(__name__)
    app.config.from_object(config)
    app.session_interface = RedisSessionInterface(redis_conf=redis_conf)
    app.json_encoder = JSONEncoder
    for bp_name in blueprints:
        bp = import_string(bp_name)
        app.register_blueprint(bp)

    db.app = app
    db.init_app(app)
    scheduler.init_app(app)
    scheduler.start()
    return app
