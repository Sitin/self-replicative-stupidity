#!/usr/bin/env python3
import json
import os

import dotenv
from flask import Flask, jsonify, redirect, url_for
from werkzeug.contrib.fixers import ProxyFix
from flask_dance.contrib.github import make_github_blueprint, github


HERE = os.path.abspath(os.path.dirname(__file__))
dotenv.load_dotenv(dotenv_path=f'{HERE}/.env')


app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

app.secret_key = b'\xb5{\xde\xd7\xdd\x12IG\x0e\nK@l\xc15\xd7'

blueprint = make_github_blueprint(
    client_id=os.environ['CLIENT_ID'],
    client_secret=os.environ['CLIENT_SECRET'],
    scope='public_repo',
)

app.register_blueprint(blueprint, url_prefix='/login')


def get_login():
    resp = github.get('/user')
    assert resp.ok

    return resp.json()['login']


def get_forks(owner='Sitin', repo='self-replicative-stupidity'):
    resp = github.get(f'/repos/{owner}/{repo}/forks')
    assert resp.ok

    return resp.json()


@app.route("/")
def index():
    if not github.authorized:
        return redirect(url_for('github.login'))

    app.logger.info('GitHub user @{login} asks for more.'.format(login=get_login()))

    forks = get_forks('amazon-archives', 'service-discovery-ecs-dns')

    return jsonify(forks)


def main():
    app.run(host='0.0.0.0', port=int(os.environ.get('SERVER_PORT', 5000)))


if __name__ == '__main__':
    main()
