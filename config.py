import os

import dotenv


HERE = os.path.abspath(os.path.dirname(__file__))
dotenv.load_dotenv(dotenv_path=f'{HERE}/.env')


APP_SECRET = os.environ['APP_SECRET'].encode()
SERVER_PORT = int(os.environ.get('SERVER_PORT', 5000))
STATIC_PATH = os.path.join(HERE, 'static')

REPO_OWNER = os.environ.get('REPO_OWNER', 'Sitin')
REPO_NAME = os.environ.get('REPO_NAME', 'self-replicative-stupidity')

CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']
