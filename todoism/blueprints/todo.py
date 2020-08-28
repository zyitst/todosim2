from flask import render_template, jsonify, request
from flask.blueprints import Blueprint
from flask_login import current_user

from todoism.models import Item
from todoism.extensions import db


todo_bp = Blueprint('todo', __name__)


@todo_bp.route('/app')
def app():
    all_count = Item.query.with_parent(current_user).count()
    completed_count = Item.query.filter_by(done=True).count()
    active_count = all_count - completed_count
    return render_template('_app.html', all_count=all_count, active_count=active_count, completed_count=completed_count,
                           items=current_user.todos)


@todo_bp.route('/items/new', methods=['POST'])
def new_item():
    data = request.get_json()
    if data is None or data['body'] == '':
        return jsonify(message='非法输入，请检查'), 400
    item = Item(content=data['body'], author=current_user)
    db.session.commit()
    return jsonify(message='待办事项已添加', html=render_template('_item.html', item=item))


@todo_bp.route('/item/<int:item_id>/edit', methods=['PUT'])
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
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    if item.author != current_user:
        return jsonify(message='对不起，此事项不属于你，你无权删除！'), 403
    db.session.delete(item)
    db.session.commit()
    return jsonify(message='删除成功！')


@todo_bp.route('/item/<int:item_id>/toggle', methods=['PATCH'])
def toggle_item(item_id):
    item = Item.query.get_or_404(item_id)
    if item.author != current_user:
        return jsonify(message='你不是本事项的主人，无法操作本事项！')
    item.done = not item.done
    db.session.commit()
    msg = '恭喜，已完成' if item.done else '恢复，未完成'
    return jsonify(message=msg)