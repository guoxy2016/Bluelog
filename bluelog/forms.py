from flask_ckeditor.fields import CKEditorField
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, InputRequired, Length, ValidationError, Email, URL, Optional

from bluelog.models import Category


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired('用户名不能为空或空格开头'), Length(1, 20, '用户名长度范围在1-20之间')])
    password = PasswordField('密码', validators=[InputRequired('请输入密码'), Length(6, 128, '密码长度范围在6-128之间')])
    remember = BooleanField('下次自动登陆')
    submit = SubmitField('登陆')


class PostForm(FlaskForm):
    title = StringField('标题', validators=[DataRequired('请输入标题'), Length(1, 30, '标题长度范围在1-30之间')])
    # slug = StringField('slug', validators=[Optional(), Length(0, 80, 'slug的长度不超过80个ASCII字符')])
    category = SelectField('分类', coerce=int, default=1)
    body = CKEditorField('内容', validators=[DataRequired('请输入内容')])
    submit = SubmitField('提交')

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.category.choices = [(category.id, category.name) for category in
                                 Category.query.order_by(Category.name).all()]

    # def validate_slug(self, field):
    #     if Post.query.filter_by(slug=field.data).first():
    #         raise ValidationError('slug以存在')
    #     for word in field.data:
    #         if ord(word) > 128:
    #             raise ValidationError('不支持非ascii字符')


class UpdateCategoryForm(FlaskForm):
    name = StringField('分类', validators=[DataRequired('请输入分类名'), Length(1, 30, '分类名的长度范围在1-30之间')])
    submit = SubmitField('提交')


class CategoryForm(UpdateCategoryForm):

    def validate_name(self, field):
        if Category.query.filter_by(name=field.data).first():
            raise ValidationError('分类以存在')


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


class LinkForm(FlaskForm):
    name = StringField('连接名', validators=[DataRequired('输入名称'), Length(1, 20, '连接名不超过20个字')])
    url = StringField('URL地址', validators=[DataRequired('输入URL'), URL(False, '连接格式不规范'), Length(1, 255, '不支持超过255个字符的连接')])
    submit = SubmitField('提交')


class SettingForm(FlaskForm):
    name = StringField('姓名', validators=[DataRequired('输入姓名'), Length(1, 30, '姓名的长度只支持30个字')])
    blog_title = StringField('博客名称', validators=[DataRequired('请输入名称'), Length(1, 60, '名称的长度最多60个字')])
    blog_sub_title = StringField('博客副标题', validators=[DataRequired('请输入名称'), Length(1, 100, '副标题最多100个字')])
    about = CKEditorField('关于', validators=[DataRequired('请填写内容')])
    submit = SubmitField('提交')
