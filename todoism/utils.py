from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature
from flask import current_app

from todoism.extensions import db


def generate_token(user, operation, expire_in=None, **kwargs):
    s = Serializer(current_app.config['SECRET_KEY'], expire_in)
    data = {
        'id': user.id,
        'operation': operation
    }
    data.update(**kwargs)
    return s.dumps(data)


def validate_token(user, operation, token):
    s = Serializer(secret_key=current_app.config['SECRET_KEY'])

    try:
        data = s.loads(token)
    except (SignatureExpired, BadSignature):
        return False

    if operation != data.get('operation') or user.id != data.get('id'):
        return False

    if operation == 'confirm':
        user.confirmed = True

    db.session.commit()
    return True
