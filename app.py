#!/usr/bin/env python3
from flask import Flask


app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World!'


def main():
    import os
    app.run(host='0.0.0.0', port=int(os.environ.get('SERVER_PORT', 5000)))


if __name__ == '__main__':
    main()
