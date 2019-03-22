from flask_ckeditor.fields import CKEditorField
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, InputRequired, Length, ValidationError, Email, URL, Optional

from bluelog.models import Category, Post


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired('用户名不能为空或空格开头'), Length(1, 20, '用户名长度范围在1-20之间')])
    password = PasswordField('密码', validators=[InputRequired('请输入密码'), Length(6, 128, '密码长度范围在6-128之间')])
    remember = BooleanField('下次自动登陆')
    submit = SubmitField('登陆')


class PostForm(FlaskForm):
    title = StringField('标题', validators=[DataRequired('请输入标题'), Length(1, 30, '标题长度范围在1-30之间')])
    slug = StringField('slug', validators=[Optional(), Length(0, 80, 'slug的长度不超过80个ASCII字符')])
    body = CKEditorField('内容', validators=[DataRequired('请输入内容')])
    category = SelectField('分类', coerce=int, default=1)
    submit = SubmitField('提交')

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.category.choices = [(category.id, category.name) for category in
                                 Category.query.order_by(Category.name).all()]

    def validate_slug(self, field):
        if Post.query.filter_by(slug=field.data).first():
            raise ValidationError('slug以存在')
        for word in field.data:
            if ord(word) > 128:
                raise ValidationError('不支持非ascii字符')


class CategoryForm(FlaskForm):
    name = StringField('类型', validators=[DataRequired('请输入类型名'), Length(1, 30, '类型名的长度范围在1-30之间')])
    submit = SubmitField('提交')

    def validate_name(self, field):
        if Category.query.filter_by(name=field.data).first():
            raise ValidationError('类型名以存在')


class CommentForm(FlaskForm):
    author = StringField('昵称', validators=[DataRequired('请输入昵称'), Length(1, 20, '不要超过20个字符')])
    email = StringField('Email', validators=[DataRequired('请输入邮箱'), Email('邮箱格式错误'), Length(1, 254, '不要超过254个字符')])
    site = StringField('URL', validators=[Optional(), URL(message='格式错误'), Length(0, 255, '不能超过255个字符')])
    body = TextAreaField('评论', validators=[DataRequired('请输入内容')])
    submit = SubmitField('提交')


class AdminCommentForm(CommentForm):
    author = HiddenField()
    email = HiddenField()
    site = HiddenField()
