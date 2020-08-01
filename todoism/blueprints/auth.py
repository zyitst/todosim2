from flask import render_template
from flask_login import login_required, login_user, logout_user, current_user
from flask.blueprints import Blueprint

from todoism import login_manager

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    pass


@auth_bp.route('logout')
@login_required
def logout():
    pass
