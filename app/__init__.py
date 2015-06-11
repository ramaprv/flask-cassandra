import os

from flask import Flask, abort
from flask.ext.mail import Mail
from cqlengine import connection
from cqlengine.management import sync_table
from flask.ext.login import LoginManager
from config import config

from .connection import load_config, setup_connections

mail = Mail()

login_manager = LoginManager()
login_manager.session_protection = 'strong'


def create_app(config_name):
    app = Flask(__name__)
    config = load_config()
    app.config.from_object(config)
    setup_connections(config)

    mail.init_app(app)
    login_manager.init_app(app)

    if not app.debug and not app.testing and not app.config['SSL_DISABLE']:
        from flask.ext.sslify import SSLify
        sslify = SSLify(app)

    from app.api import api
    app.register_blueprint(api, url_prefix='/api')

    from app.models import models
    app.register_blueprint(models)

    return app
