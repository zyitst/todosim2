from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_moment import Moment

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
moment = Moment()

login_manager.login_view = 'auth.login'
login_manager.login_message = '请先登录！'


@login_manager.user_loader
def user_loader(username):
    from todoism.models import User
    user = User.query.filter_by(uid=username).first()
    return user
