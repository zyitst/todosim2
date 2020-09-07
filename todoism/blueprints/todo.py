from datetime import datetime

from flask import render_template, jsonify, request
from flask.blueprints import Blueprint
from flask_login import current_user, login_required

from todoism.models import Item
from todoism.extensions import db


todo_bp = Blueprint('todo', __name__)


@todo_bp.route('/app')
@login_required
def app():
    all_count = Item.query.with_parent(current_user).count()
    completed_count = Item.query.with_parent(current_user).filter_by(done=True).count()
    active_count = all_count - completed_count
    return render_template('_app.html', all_count=all_count, active_count=active_count, completed_count=completed_count,
                           items=current_user.todos)


@todo_bp.route('/items/new', methods=['POST'])
@login_required
def new_item():
    data = request.get_json()
    if data is None or data['body'] == '':
        return jsonify(message='非法输入，请检查'), 400
    item = Item(content=data['body'], author=current_user)
    db.session.commit()
    return jsonify(message='待办事项已添加', html=render_template('_item.html', item=item))


@todo_bp.route('/item/<int:item_id>/edit', methods=['PUT'])
@login_required
def edit_item(item_id):
    item = Item.query.get_or_404(item_id)
    if item.author != current_user:
        return jsonify(message='对不起，此事项不属于你，你无权编辑！'), 403
    data = request.get_json()
    if data is None or data['body'].strip() == '':
        return jsonify(message='不合法的消息体'), 400
    item.content = data['body']
    db.session.commit()
    return jsonify(message='修改成功！')


@todo_bp.route('/item/<int:item_id>/delete', methods=['DELETE'])
@login_required
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    if item.author != current_user:
        return jsonify(message='对不起，此事项不属于你，你无权删除！'), 403
    db.session.delete(item)
    db.session.commit()
    return jsonify(message='删除成功！')


@todo_bp.route('/item/<int:item_id>/toggle', methods=['PATCH'])
@login_required
def toggle_item(item_id):
    item = Item.query.get_or_404(item_id)
    if item.author != current_user:
        return jsonify(message='你不是本事项的主人，无法操作本事项！')
    item.done = not item.done
    if item.done:
        item.done_time = datetime.utcnow()
        msg = '恭喜，已完成'
    else:
        item.done_time = None
        msg = '恢复，未完成'
    db.session.commit()
    return jsonify(message=msg)


@todo_bp.route('/item/<int:item_id>/change_priority', methods=['PATCH'])
@login_required
def change_priority(item_id):
    item = Item.query.get_or_404(item_id)
    if item.author != current_user:
        return jsonify(message='你不是本事项的主人，无法操作本事项！')
    data = request.get_json()
    if data is None or data['priority'] not in [1, 2, 3]:
        return jsonify(message='优先级非法'), 400
    item.priority = int(data['priority'])
    db.session.commit()
    return jsonify(message='优先级修改成功！')


@todo_bp.route('/items/clear', methods=['DELETE'])
@login_required
def clear():
    done_items = Item.query.with_parent(current_user).filter_by(done=True).all()
    for item in done_items:
        db.session.delete(item)
    return jsonify(message='清空成功！')
