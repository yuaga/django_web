from django import forms
from django.core import validators
from django.core.exceptions import ValidationError

from apps.forms import FormMixin


class LoginForm(forms.Form, FormMixin):
    telephone = forms.CharField(
        max_length=11,
        min_length=11,
        strip=True,
        error_messages={
            'max_length': '请正确输入手机号码！',
            'min_length': '请输入11位手机号码！',
            'required': "手机号不能为空!"
        })
    password = forms.CharField(
        max_length=16,
        min_length=8,
        strip=True,
        error_messages={
            'max_length': '密码输入错误！',
            'min_length': '密码输入错误！',
            'required': "密码不能为空!"
        })
    remember = forms.IntegerField(required=False)


class RegisterForm(forms.Form, FormMixin):
    telephone = forms.CharField(
        validators=[validators.RegexValidator(r'1[35678]\d{9}', '请输入正确的手机号码!')],
        max_length=11,
        min_length=11,
        strip=True,
        error_messages={
            'max_length': '请正确输入手机号码！',
            'min_length': '请输入11位手机号码！',
            'required': "手机号不能为空！"
        })
    username = forms.CharField(
        max_length=50,
        strip=True,
        error_messages={
            'required': "用户名不能为空！"
        })
    password1 = forms.CharField(
        max_length=16,
        min_length=8,
        strip=True,
        error_messages={
            'max_length': '密码长度太长！',
            'min_length': '密码不足8位！',
            'required': "密码不能为空！"
        })
    password2 = forms.CharField(
        max_length=16,
        min_length=8,
        strip=True,
        error_messages={
            'max_length': '密码长度太长！',
            'min_length': '密码不足8位！',
            'required': "密码不能为空！"
        })

    def clean_username(self):
        # 从cleaned_data中取出想要的数据
        username = self.cleaned_data.get("username")
        values=['sb', 'SB', '傻逼', '傻狗', '全家死了', '作者是傻逼', '垃圾']
        for value in values:
            if value in username:
                # 错误就抛异常
                raise ValidationError("不要使用侮辱性的用户名！")
            else:
                return username


class EditForm(forms.Form, FormMixin):
    telephone = forms.CharField(
        max_length=11,
        min_length=11,
        strip=True,
        error_messages={
            'max_length': '请正确输入手机号码！',
            'min_length': '请输入11位手机号码！',
            'required': "手机号不能为空!"
        })

    old_pwd = forms.CharField(
        max_length=16,
        min_length=8,
        strip=True,
        error_messages={
            'max_length': '密码输入错误！',
            'min_length': '密码输入错误！',
            'required': "密码不能为空!"
        })
    new_pwd1 = forms.CharField(
        max_length=16,
        min_length=8,
        strip=True,
        error_messages={
            'max_length': '密码输入错误！',
            'min_length': '密码输入错误！',
            'required': "密码不能为空!"
        })
    new_pwd2 = forms.CharField(
        max_length=16,
        min_length=8,
        strip=True,
        error_messages={
            'max_length': '密码输入错误！',
            'min_length': '密码输入错误！',
            'required': "密码不能为空!"
        })