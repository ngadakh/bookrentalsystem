# pytest configurations

import json
import os

import pytest

import config
from brs.models import db
from run import app

CURRENT_PATH = os.path.abspath(os.path.dirname(__file__))


@pytest.fixture(scope="session")
def client():
    with app.test_client() as client:
        with app.app_context():
            app.init_app()
        yield client
        db.session.remove()
        db.drop_all()


class AuthOperations(object):
    def __init__(self, client):
        self._client = client

    def login(self, username=config.ENVIRONMENT.USERS['username'], password=config.ENVIRONMENT.USERS['password']):
        return self._client.post(
            '/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/logout')


@pytest.fixture(scope="session")
def auth(client):
    return AuthOperations(client)


try:
    with open(CURRENT_PATH + '/test_data.json') as data_file:
        test_data = json.load(data_file)
except FileNotFoundError:
    pass
