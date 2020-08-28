from faker import Faker
from flask import render_template, jsonify, redirect, url_for, request
from flask_login import login_required, login_user, logout_user, current_user
from flask.blueprints import Blueprint

from todoism import login_manager
from todoism.models import User, Item
from todoism.extensions import db

auth_bp = Blueprint('auth', __name__)
faker = Faker()


@auth_bp.route('/register')
def register():
    username = faker.user_name()
    while User.query.filter_by(name=username).first() is not None:
        username = faker.user_name()
    password = faker.word()
    user=User(name=username)
    user.set_password(password)

    db.session.add(user)

    item = Item(content='买个苹果AirPods Pro', author=user)
    item2 = Item(content='换台新的5G手机（华为 or 小米 or OV or 一加）', author=user)
    item3 = Item(content='找个好工作', author=user)
    item4 = Item(content='找个女朋友', author=user)
    db.session.add_all([item, item2, item3, item4])

    db.session.commit()

    return jsonify(username=username, password=password, message='假账号生成成功')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('todo.app'))
    if request.method == 'POST':
        data = request.get_json()
        username = data['username']
        password = data['password']

        user = User.query.filter_by(name=username).first()
        if user and user.valid_password(password):
            login_user(user)
            return jsonify(message='登陆成功')
        else:
            return jsonify(message='用户或密码错误'), 400
    return render_template('_login.html')




@auth_bp.route('/logout')
@login_required
def logout():
    pass
