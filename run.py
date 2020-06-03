# Entry point for project
# Create the flask app and loads all necessary modules

import flask
from flask import render_template, redirect, url_for, session

import config
from brs import create_app, login_required

app = create_app()


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'GET':
        return render_template("login.html")

    username = flask.request.form['username']
    if flask.request.form['password'] == config.ENVIRONMENT.USERS['password']:
        session['logged_in'] = session['username'] = username
        return flask.redirect(flask.url_for('home'))

    return 'Login unsuccessful!!'


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    session.clear()
    return redirect(url_for('login'))


def main():
    app.run(
        host=config.ENVIRONMENT.DEFAULT_SERVER,
        port=config.ENVIRONMENT.DEFAULT_SERVER_PORT,
    )


if __name__ == '__main__':
    main()
