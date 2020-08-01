from flask import Flask

from todoism.extensions import db, login_manager
from todoism import settings


def create_app():
    app = Flask(__name__)
    register_extensions(app)
    return app


def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)


app = create_app()


@app.route('/')
def index():
    return 'init'
