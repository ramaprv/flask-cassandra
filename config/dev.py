# -*- coding: utf-8 -*-

import os

DATABASE_CONNECT_OPTIONS = {}
THREADS_PER_PAGE = 2
CSRF_ENABLED     = True
CSRF_SESSION_KEY = "secret"
SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret'
SSL_DISABLE = False
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
FLASKY_MAIL_SENDER = 'Flasky Admin <flasky@example.com>'
FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
DEBUG = True
CASSANDRA_KEYSPACE = 'shop'
CASSANDRA_HOSTS = ['127.0.0.1']
CQLENG_ALLOW_SCHEMA_MANAGEMENT = 'CQLENG_ALLOW_SCHEMA_MANAGEMENT'

@staticmethod
def init_app(app):
    pass
