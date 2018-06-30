#!/usr/bin/env python3
from flask import Flask, redirect, render_template, send_from_directory, url_for
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
    redirect_to='/fork',
)

app.register_blueprint(blueprint, url_prefix='/login')


def get_login():
    resp = github.get('/user')
    assert resp.ok

    return resp.json()['login']


def make_a_fork(owner, repo_name):
    resp = github.post(f'/repos/{owner}/{repo_name}/forks')
    assert resp.ok

    return resp.json()


def authorize(fn):
    def wrapper(*args, **kwargs):
        if not github.authorized:
            return redirect(url_for('github.login'))

        return fn(*args, **kwargs)

    return wrapper


@app.route('/', methods=['GET'])
@authorize
def index():
    return render_template('index.html', REPO_OWNER=REPO_OWNER, REPO_NAME=REPO_NAME)


@app.route('/<path:path>', methods=['GET'])
def serve_file_in_dir(path):

    if not os.path.isfile(os.path.join(STATIC_PATH, path)):
        path = os.path.join(path, 'index.html')

    return send_from_directory(STATIC_PATH, path)


@app.route('/fork', methods=['GET'])
@authorize
def fork():
    make_a_fork(REPO_OWNER, REPO_NAME)

    return render_template('fork.html', login=get_login(), REPO_OWNER=REPO_OWNER, REPO_NAME=REPO_NAME)


def main():
    app.run(host='0.0.0.0', port=SERVER_PORT)


if __name__ == '__main__':
    main()
