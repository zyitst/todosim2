import random
from datetime import datetime

from faker import Faker
from flask import render_template, jsonify, redirect, url_for, request, flash
from flask_login import login_required, login_user, logout_user, current_user
from flask.blueprints import Blueprint

from todoism.email import send_confirm_mail
from todoism.models import User, Item
from todoism.extensions import db
from todoism.utils import generate_token, validate_token

auth_bp = Blueprint('auth', __name__)
faker = Faker()


@auth_bp.route('/get_test_account')
def get_test_account():
    email = faker.email()
    while User.query.filter_by(name=email).first() is not None:
        email = faker.email()
    fake_name = faker.user_name()
    password = faker.word()
    user=User(name=fake_name, email=email, confirmed=True)
    user.set_password(password)

    db.session.add(user)

    todo_contents = [
        'Witness something truly majestic',
        'Help a complete stranger',
        'Drive a motorcycle on the Great Wall of China',
        'Sit on the Great Egyptian Pyramids',
        '找个好工作',
        '买个苹果AirPods Pro',
        '注册功能完善（电子邮件，token验证）',
        '优先级,设置，修改。。。',
        '拖拽调整顺序。。',
        '设定deadline并提醒',
        '倒垃圾',
        '国际化',
    ]
    items = []
    for i, content in enumerate(todo_contents):
        item = Item(content=content, author=user, priority=random.randrange(1,4,1))
        if i in [1, 6, 7, 10]:
            item.done = True
            item.done_time = datetime.utcnow()
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
            return jsonify(message='该邮箱已注册！', code='e101')
        user = User(name=username, email=email.lower())
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        token = generate_token(user=user, operation='confirm')
        send_confirm_mail(user, token)
        return jsonify(message='注册成功，请验登录后验证邮箱')
    return render_template('_register.html')


@auth_bp.route('/confirm/<token>')
@login_required
def confirm(token):
    # if not current_user.is_authenticated:
    #     flash('请先登录！','warning')
    #     next = request.url
    #     return redirect(url_for('home.index') + '#login&next=' + next, code=302)
    if current_user.confirmed:
        flash('已确认，无需操作')
        return redirect(url_for('home.index') + '#app')
    if validate_token(user=current_user, token=token, operation='confirm'):
        flash('确认成功！')
        return redirect(url_for('home.index') + '#app')
    else:
        flash('令牌过期或有误，请重新发送确认邮件！')
        return redirect(url_for('home.index') + '#app')


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
            message = '登陆成功'
            if not user.confirmed:
                message += ',请验证邮箱'
            return jsonify(message=message)
        else:
            return jsonify(message='用户或密码错误'), 400
    return render_template('_login.html')




@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify(message='您已登出！')
