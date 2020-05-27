import os
import sqlite3
from flask import Flask, g

import config

DATABASE = 'brs.db'

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])


@app.route('/home')
def hello_name():
    return "Hello World!"


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


if __name__ == '__main__':
    app.run(
        host=config.DEFAULT_SERVER,
        port=config.DEFAULT_SERVER_PORT
    )
