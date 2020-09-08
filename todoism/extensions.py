from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_moment import Moment
from flask_mail import Mail

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
moment = Moment()
mail = Mail()

login_manager.login_view = 'auth.login'
login_manager.login_message = '请先登录！'


@login_manager.user_loader
def user_loader(username):
    from todoism.models import User
    user = User.query.filter_by(id=username).first()
    return user
