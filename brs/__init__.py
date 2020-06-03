import os
from functools import wraps
from importlib import import_module

from flask import Flask
from flask import redirect, url_for, session
from werkzeug.utils import find_modules

import config
from brs.models import db
from brs.utils import BRSModule

BASEDIR = os.path.abspath(os.path.dirname(__file__))


class BRS(Flask):
    """
    This class find the modules from the project and import it in the memory
    """
    def __init__(self, *args, **kwargs):
        super(BRS, self).__init__(*args, **kwargs)

    def find_submodules(self, base_module):
        for module_name in find_modules(base_module, True):
            module = import_module(module_name)
            for key in list(module.__dict__.keys()):
                if isinstance(module.__dict__[key], BRSModule):
                    yield module.__dict__[key]

    def init_app(self):
        pass


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))

    return wrap


def create_app():
    """
    This function creates the Flask app and set the default configs set in config.py
    :return: flask app
    """
    flask_app = BRS(__name__)
    flask_app.config.from_object('config.ENVIRONMENT')

    # Set the SQLITE database file path
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(config.ENVIRONMENT.SQLITE_PATH)
    db.init_app(flask_app)

    # Create database tables data models
    with flask_app.app_context():
        from brs import models
        db.create_all()

    # Register blueprints for available modules like books & customer
    for module in flask_app.find_submodules('brs'):
        flask_app.register_blueprint(module)

    return flask_app
