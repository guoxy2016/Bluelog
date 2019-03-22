from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from sqlalchemy import MetaData

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)
mail = Mail()
bootstrap = Bootstrap()
ckeditor = CKEditor()
moment = Moment()
migrate = Migrate()
login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    from bluelog.models import Admin
    user = Admin.query.get(int(user_id))
    return user

