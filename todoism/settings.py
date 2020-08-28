import os
import sys

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'


class BaseConfig:
    SECRET_KEY = os.getenv('SECRET_KEY', 'bli jiojio')

    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', prefix + os.path.join(basedir, 'data.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSONIFY_MIMETYPE = "application/json;charset=utf-8"


class DevConfig(BaseConfig):
    pass


class ProdConfig(BaseConfig):
    pass


config = {
    'dev': DevConfig,
    'prod': ProdConfig
}
