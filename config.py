import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))
tmp = os.path.join(basedir,'tmp')

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    GITHUB_CLIENT_ID = os.environ.get('GITHUB_CLIENT_ID')
    GITHUB_CLIENT_SECRET = os.environ.get('GITHUB_CLIENT_SECRET')
    ORIGIN_REPO_NAME =  os.environ.get('ORIGIN_REPO_NAME')
    ORIGIN_REPO_USER =  os.environ.get('ORIGIN_REPO_USER')
