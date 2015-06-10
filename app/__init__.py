import os
import imp

from flask import Flask, abort
from flask.ext.mail import Mail
from cqlengine import connection
from cqlengine.management import sync_table
from flask.ext.login import LoginManager
from config import config

mail = Mail()

login_manager = LoginManager()
login_manager.session_protection = 'strong'


def _get_default_config_path():
    for name in ("prod.py", "dev.py"):
        path = "config/{}".format(name)
        if os.path.exists(path):
            return path
    else:
        logger.error("Couldn't locate the files in config/")
        exit(1)


def _load_config():
    """Load config object for workers.

    Look the environment variable called `WORKER_CONFIG`. If present
    load the python file else look for `prod.py`, `dev.py` in the order.
    If both are missing quit.

    `WORKER_CONFIG` can be of form `config/prod.py` or `config.prod.py`.
    """
    path = os.environ.get('WORKER_CONFIG')
    if not path:
        path = _get_default_config_path()

    mod_name, file_ext = os.path.splitext(os.path.split(path)[-1])
    config = imp.load_source(mod_name, path)
    return config

def _set_env_vars(config):
    for k, v in config.__dict__.items():
        if isinstance(v, (int, basestring)):
            os.environ[k] = unicode(v)

def _setup_cassandra(hosts, keyspace):
    """Setup connection to cassandra nodes.

    This function needs to be called before making any queries.

    :param hosts `list`: list of hosts to connect to.
    :param keyspace `unicode`: name of the keyspace to connect.
    """
    if not isinstance(hosts, list):
        raise ValueError("hosts only accpets list of ips.")
    connection.setup(hosts=hosts, default_keyspace=keyspace,
                     protocol_version=3)

def _setup_connections(config):
    """Set connection to Cassandra, SQLAlchemy, cassandra
    """
    keyspace = config.CASSANDRA_KEYSPACE
    hosts = config.CASSANDRA_HOSTS
    _setup_cassandra(hosts=hosts, keyspace=keyspace)
    _set_env_vars(config)


def create_app(config_name):
    app = Flask(__name__)
    config = _load_config()
    app.config.from_object(config)
    _setup_connections(config)

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
