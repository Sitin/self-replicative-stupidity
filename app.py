#!/usr/bin/env python3
from flask import Flask, redirect, url_for
from werkzeug.contrib.fixers import ProxyFix
from flask_dance.contrib.github import make_github_blueprint, github

from config import *


app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

app.secret_key = APP_SECRET

blueprint = make_github_blueprint(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    scope='public_repo',
)

app.register_blueprint(blueprint, url_prefix='/login')


def get_login():
    resp = github.get('/user')
    assert resp.ok

    return resp.json()['login']


def make_a_fork(owner, repo):
    resp = github.post(f'/repos/{owner}/{repo}/forks')
    assert resp.ok

    return resp.json()


@app.route("/")
def index():
    if not github.authorized:
        return redirect(url_for('github.login'))

    make_a_fork(REPO_OWNER, REPO_NAME)

    login = get_login()
    return f'Made a fork of the {REPO_OWNER}/{REPO_NAME} for @{login}.'


def main():
    app.run(host='0.0.0.0', port=SERVER_PORT)


if __name__ == '__main__':
    main()
