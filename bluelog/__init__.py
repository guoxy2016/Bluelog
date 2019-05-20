import os

import click
from flask import Flask, render_template
from flask_login import current_user
from flask_wtf.csrf import CSRFError

from bluelog.extensions import db, mail, moment, bootstrap, ckeditor, migrate, login_manager, csrf
from bluelog.models import Admin, Category, Comment, Post, Link
from bluelog.settings import config


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('bluelog')
    app.config.from_object(config[config_name])

    register_logging()
    register_extensions(app)
    register_blueprints(app)
    register_shell_context(app)
    register_template_context(app)
    register_errors(app)
    register_commends(app)

    return app


def register_logging():
    ...


def register_extensions(app=None):
    db.init_app(app)
    mail.init_app(app)
    ckeditor.init_app(app)
    moment.init_app(app)
    bootstrap.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)


def register_blueprints(app=None):
    from bluelog.blueprints.admin import admin_bp
    from bluelog.blueprints.auth import auth_bp
    from bluelog.blueprints.blog import blog_bp
    app.register_blueprint(blog_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(auth_bp, url_prefix='/auth')


def register_shell_context(app=None):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db, mail=mail, ckeditor=ckeditor, moment=moment, bootstrap=bootstrap, Admin=Admin,
                    Category=Category, Comment=Comment, Post=Post)


def register_template_context(app=None):
    @app.context_processor
    def make_template_context():
        admin = Admin.query.first()
        categories = Category.query.all()
        links = Link.query.all()
        if current_user.is_authenticated:
            unread_comments = Comment.query.filter_by(reviewed=False).count()
        else:
            unread_comments = None
        return dict(admin=admin, categories=categories, unread_comments=unread_comments, links=links)


def register_errors(app=None):
    @app.errorhandler(400)
    def bad_required(_):
        return render_template('error/400.html'), 400

    @app.errorhandler(404)
    def not_found(_):
        return render_template('error/404.html'), 404

    @app.errorhandler(500)
    def server_error(_):
        return render_template('error/500.html'), 500

    @app.errorhandler(CSRFError)
    def csrf_error(e):
        return render_template('error/400.html', descraption=e.description), 400


def register_commends(app=None):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def init_db(drop):
        """Initialize the database."""
        if drop:
            click.confirm('This operation will delete the database, do you want to continue?', abort=True)
            db.drop_all()
            click.echo('Drop tables.')
        db.create_all()
        click.echo('Initialized database.')

    @app.cli.command()
    @click.option('--category', default=10, help='Quantity of category. default is 10.')
    @click.option('--post', default=50, help='Quantity of post, default is 50.')
    @click.option('--comment', default=500, help='Quantity of comment, default is 500.')
    def forge(category, post, comment):
        """Generates the fake categories, post, and comments."""
        from bluelog.fakes import fake_admin, fake_category, fake_post, fake_comment, fake_link
        db.drop_all()
        db.create_all()

        click.echo('Generating Administrator....')
        fake_admin()

        click.echo('Generating %s categories...' % category)
        fake_category(category)

        click.echo('Generating %s posts...' % post)
        fake_post(post)

        click.echo('Generating %s comments' % comment)
        fake_comment(comment)

        click.echo('Generating links')
        fake_link()

        click.echo('Done!')

    @app.cli.command()
    @click.option('--username', prompt=True, help='Quantity of username for login')
    @click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True,
                  help='Quantity of user\'s password for login')
    def init(username, password):
        db.create_all()

        admin = Admin.query.first()
        if admin:
            click.echo('Updating the user to Superuser...')
            admin.username = username
            admin.password = password
        else:
            click.echo('Creating the Superuser...')
            admin = Admin(username=username, blog_title='Blog', blog_sub_title='你的博客.', name='Admin',
                          about='Anything about you.')
            admin.password = password
            db.session.add(admin)

        db.session.commit()
        category = Category.query.first()
        if category is None:
            click.echo('Creating the default category...')
            category = Category(name='默认')
            db.session.add(category)

        db.session.commit()
        click.echo('Done!')
