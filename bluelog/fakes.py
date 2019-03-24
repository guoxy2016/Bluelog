import random

from faker import Faker
from sqlalchemy.exc import IntegrityError

from bluelog.extensions import db
from bluelog.models import Admin, Comment, Category, Post

fake = Faker('zh_CN')


def fake_admin():
    admin = Admin(
        username='admin',
        blog_title='Blog',
        blog_sub_title='博客网站',
        name='Vim',
        about='关于我自己, 写网站就好了'
    )
    admin.password = 'helloflask'
    db.session.add(admin)
    db.session.commit()


def fake_category(count=10):
    category = Category(name='默认')
    db.session.add(category)
    for i in range(count):
        category = Category(name=fake.word())
        db.session.add(category)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def fake_post(count=50):
    for i in range(count):
        post = Post(
            title=fake.sentence(),
            body=fake.text(2000),
            category=Category.query.get(random.randint(1, Category.query.count())),
            timestamp=fake.date_time_this_year()
        )
        db.session.add(post)
    db.session.commit()


def fake_comment(count=500):
    for i in range(count):
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            body=fake.sentence(),
            reviewed=True,
            post=Post.query.get(random.randint(1, Post.query.count())),
            timestamp=fake.date_time_this_year()
        )
        db.session.add(comment)

    salt = int(count * 0.1)

    # 回复
    for i in range(salt):
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            body=fake.sentence(),
            reviewed=True,
            post=Post.query.get(random.randint(1, Post.query.count())),
            replied=Comment.query.get(random.randint(1, Comment.query.count())),
            timestamp=fake.date_time_this_year()
        )
        db.session.add(comment)
    db.session.commit()

    # admin回复
    admin = Admin.query.first()
    for i in range(salt):
        comment = Comment(
            author=admin.name,
            email='admin@example.com',
            site='example.com',
            body=fake.sentence(),
            from_admin=True,
            reviewed=True,
            post=Post.query.get(random.randint(1, Post.query.count())),
            timestamp=fake.date_time_this_year()
        )
        db.session.add(comment)

    # 未审核
    for i in range(salt):
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            body=fake.sentence(),
            reviewed=False,
            post=Post.query.get(random.randint(1, Post.query.count())),
            timestamp=fake.date_time_this_year()
        )
        db.session.add(comment)
    db.session.commit()
