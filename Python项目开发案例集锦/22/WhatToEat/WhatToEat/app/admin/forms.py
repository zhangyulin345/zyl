# _*_ coding: utf-8 _*_

from flask_wtf import FlaskForm
from flask_wtf.file import  FileAllowed
from wtforms import StringField, PasswordField, SubmitField, FileField, TextAreaField, RadioField,SelectField,IntegerField
from wtforms.validators import DataRequired, ValidationError
from app.models import Admin


class LoginForm(FlaskForm):
    """
    管理员登录表单
    """
    account = StringField(
        label="账号",
        validators=[
            DataRequired("账号不能为空")
        ],
        description="账号",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入账号！",
        }
    )
    pwd = PasswordField(
        label="密码",
        validators=[
            DataRequired("密码不能为空")
        ],
        description="密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入密码！",
        }
    )
    submit = SubmitField(
        '登录',
        render_kw={
            "class": "btn btn-primary btn-block btn-flat",
        }
    )

    # 验证账号，命名规则：validate_ + 字段名。如果要验证密码，则可以创建函数validate_pwd
    def validate_account(self, field):
        account = field.data
        admin = Admin.query.filter_by(name=account).count()
        if admin == 0:
            raise ValidationError("账号不存在! ")

class PwdForm(FlaskForm):
    old_pwd = PasswordField(
        label="旧密码",
        validators=[
            DataRequired("旧密码不能为空！")
        ],
        description="旧密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入旧密码！",
        }
    )
    new_pwd = PasswordField(
        label="新密码",
        validators=[
            DataRequired("新密码不能为空！")
        ],
        description="新密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入新密码！",
        }
    )
    submit = SubmitField(
        '保存',
        render_kw={
            "class": "btn btn-primary",
        }
    )

    def validate_old_pwd(self, field):
        from flask import session
        pwd = field.data
        name = session["admin"]
        admin = Admin.query.filter_by(
            name=name
        ).first()
        if not admin.check_pwd(pwd):
            raise ValidationError("旧密码错误！")

class CategoryForm(FlaskForm):
    """添加/编辑菜系的表单"""
    name = StringField(
        label="菜系名称",
        validators=[
            DataRequired("菜系名不能为空")
        ],
        description="菜系",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入菜系名称！"
        }
    )
    order_num = IntegerField(
        label="排序",
        validators=[
            DataRequired("请输入1-100之间的整数"),
        ],
        description="排序",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入1-100的整数，编号越大越靠前！"
        }
    )
    submit = SubmitField(
        '添加',
        render_kw={
            "class": "btn btn-primary",
        }
    )

class FoodForm(FlaskForm):
    name = StringField(
        label="菜品名称",
        validators=[
            DataRequired("菜品名称不能为空！")
        ],
        description="菜品名称",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入菜品名称！"
        }
    )
    cate_id = SelectField(
        label="所属菜系",
        validators=[
            DataRequired("请选择所属菜系！")
        ],
        coerce=int,
        description="所属菜系",
        render_kw={
            "class": "form-control",
        }
    )
    submit = SubmitField(
        '添加',
        render_kw={
            "class": "btn btn-primary",
        }
    )

class TravelsForm(FlaskForm):
    title = StringField(
        label="标题",
        validators=[
            DataRequired("标题不能为空！")
        ],
        description="标题",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入标题！"
        }
    )
    author = StringField(
        label="作者",
        validators=[
            DataRequired("作者不能为空！")
        ],
        description="作者",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入作者！"
        }
    )
    content = TextAreaField(
        label="游记内容",
        validators=[
            DataRequired("游记内容不能为空！")
        ],
        description="游记内容",
        render_kw={
            "class": "form-control ckeditor",
        }
    )
    scenic_id = SelectField(
        label="所属景区",
        validators=[
            DataRequired("请选择景区！")
        ],
        coerce=int,
        description="所属景区",
        render_kw={
            "class": "form-control",
        }
    )
    submit = SubmitField(
        '添加',
        render_kw={
            "class": "btn btn-primary",
        }
    )

