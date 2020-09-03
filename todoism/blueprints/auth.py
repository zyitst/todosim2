import random

from faker import Faker
from flask import render_template, jsonify, redirect, url_for, request
from flask_login import login_required, login_user, logout_user, current_user
from flask.blueprints import Blueprint

from todoism.models import User, Item
from todoism.extensions import db

auth_bp = Blueprint('auth', __name__)
faker = Faker()


@auth_bp.route('/get_test_account')
def get_test_account():
    email = faker.email()
    while User.query.filter_by(name=email).first() is not None:
        email = faker.email()
    fake_name = faker.user_name()
    password = faker.word()
    user=User(name=fake_name, email=email)
    user.set_password(password)

    db.session.add(user)

    todo_contents = [
        'Witness something truly majestic',
        'Help a complete stranger',
        'Drive a motorcycle on the Great Wall of China',
        'Sit on the Great Egyptian Pyramids',
        '买个苹果AirPods Pro',
        '换台新的5G手机（华为 or 小米 or OV or 一加）',
        '找个好工作',
        # '找个女朋友',
        '注册功能完善（电子邮件，验证。。。）',
        '优先级？？设置，修改。。。默认优先级',
        '拖拽调整顺序。。',
        '日历功能',
        '倒垃圾',
        '设定deadline并提醒',
    ]
    items = []
    for i, content in enumerate(todo_contents):
        item = Item(content=content, author=user, priority=random.randrange(1,4,1))
        if i == 3 or i == 10 or i == 11:
            item.done = True
        items.append(item)

    db.session.add_all(items)
    db.session.commit()
    return jsonify(email=email, password=password, message='假账号生成成功')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('todo.app'))
    if request.method == 'POST':
        data = request.get_json()
        email = data['email']
        username = data['username']
        password = data['password']
        if User.query.filter_by(email=email.lower()).first():
            return jsonify(message='该邮箱已注册！')
        user = User(name=username, email=email.lower())
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return jsonify(message='注册成功，请验证邮箱然后登录')
    return render_template('_register.html')




@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('todo.app'))
    if request.method == 'POST':
        data = request.get_json()
        email = data['email']
        password = data['password']

        user = User.query.filter_by(email=email).first()
        if user and user.valid_password(password):
            login_user(user)
            return jsonify(message='登陆成功')
        else:
            return jsonify(message='用户或密码错误'), 400
    return render_template('_login.html')




@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify(message='您已登出！')
