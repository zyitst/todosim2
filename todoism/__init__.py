import os

import click
from flask import Flask, render_template
from flask_login import current_user

from todoism.blueprints.home import home_bp
from todoism.blueprints.todo import todo_bp
from todoism.extensions import db, login_manager, csrf, moment
from todoism.blueprints.auth import auth_bp
from todoism import settings
from todoism.models import Item


def create_app(config_name=None):
    app = Flask(__name__)

    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'dev')
    app.config.from_object(settings.config[config_name])

    register_extensions(app)
    register_blueprints(app)
    register_template_ctx(app)
    return app


def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    moment.init_app(app)


def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(todo_bp)
    app.register_blueprint(home_bp)


def register_template_ctx(app):
    @app.context_processor
    def make_template_context():
        if current_user.is_authenticated:
            active_items = Item.query.with_parent(current_user).filter_by(done=False).count()
        else:
            active_items = None
        return dict(active_items=active_items)


app = create_app()


@app.cli.command()
@click.option('--drop', is_flag=True, help='is_flag啥用?')
def init(drop):
    if drop:
        click.confirm('此操作会删除数据库表，你确定要继续吗?', abort=True)
        db.drop_all()
        click.echo('数据表已删除！')
    db.create_all()
    click.echo('已重新生成数据库表！')


@app.route('/')
def index():
    return render_template('index.html')
