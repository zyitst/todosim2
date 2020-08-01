from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from todoism.extensions import db


class User(db.Model, UserMixin):
    id =db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(20))
    password_hash=db.Column(db.String(128))
    todos = db.relationship('Item', back_populates='author', cascade='all')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def valid_password(self, password):
        return check_password_hash(self.password_hash, password)


class Item(db.Model):
    id =db.Column(db.Integer, primary_key=True)
    content=db.Column(db.String(30))
    done=db.Column(db.Boolean, default=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship('User', back_populates='todos')
