import os

basedir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))


class BaseConfig:
    SECRET_KEY = os.getenv('SECRET_KEY', 'development secret key')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = ('GreenBlog', MAIL_USERNAME)

    BLOG_ADMIN_EMAIL = os.getenv('GUOBLOG_EMAIL')
    BLOG_POST_PER_PAGE = 10
    BLOG_MANAGE_POST_PER_PAGE = 15
    BLOG_COMMENT_PER_PAGE = 15
    BLOG_MANAGE_COMMENT_PER_PAGE = 15

    BLOG_THEMES = {'default': '默认', 'lux': 'LUX', 'darkly': 'Darkly', 'cerulean': 'Cerulean', 'litera': 'Litera'}


class DevelopConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite3')


class TestingConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLE = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class ProductConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite3')


config = {
    'development': DevelopConfig,
    'testing': TestingConfig,
    'production': ProductConfig
}
