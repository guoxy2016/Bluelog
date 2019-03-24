from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from bluelog.extensions import db


class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    _password_hash = db.Column(db.String(255))

    blog_title = db.Column(db.String(60))
    blog_sub_title = db.Column(db.String(100))
    name = db.Column(db.String(30))

    about = db.Column(db.TEXT)

    def validate_password(self, password):
        return check_password_hash(self._password_hash, password)

    @property
    def password(self):
        raise AttributeError('属性不可读取')

    @password.setter
    def password(self, password):
        self._password_hash = generate_password_hash(password=password)

    def __repr__(self):
        return '<Admin %r>' % self.username


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    posts = db.relationship('Post', back_populates='category')

    def delete(self):
        default_category = Category.query.get(1)
        posts = self.posts.copy()
        for post in posts:
            post.category = default_category
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return '<Category %r>' % self.name


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30))
    body = db.Column(db.Text)
    # slug = db.Column(db.String(40), unique=True)
    can_comment = db.Column(db.Boolean, default=True)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', back_populates='posts')

    comments = db.relationship('Comment', back_populates='post', cascade='all, delete-orphan')

    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    def __repr__(self):
        return '<Post %r>' % self.title


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    author = db.Column(db.String(20), index=True)
    email = db.Column(db.String(254))
    site = db.Column(db.String(255))
    body = db.Column(db.String(200))

    from_admin = db.Column(db.Boolean, default=False)
    reviewed = db.Column(db.Boolean, default=False)

    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    post = db.relationship('Post', back_populates='comments')

    replied_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    replied = db.relationship('Comment', back_populates='replies', remote_side=[id])
    replies = db.relationship('Comment', back_populates='replied', cascade='all')

    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
