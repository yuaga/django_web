from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import PermissionsMixin, BaseUserManager
from django.core import validators
from shortuuidfield import ShortUUIDField


class UserManager(BaseUserManager):

    def _create_user(self, telephone, username, password, **kwargs):

        if not telephone:
            return ValueError('手机号码好像忘了！')
        if not username:
            return ValueError('请给自己取一个牛逼的名字吧！')
        if not password:
            return ValueError('没有密码，怎么登录呀！')
        user = self.model(telephone=telephone, username=username, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, telephone, username, password, **kwargs):
        kwargs['is_superuser'] = False
        return self._create_user(telephone=telephone, username=username, password=password, **kwargs)

    def create_superuser(self, telephone, username, password, **kwargs):
        kwargs['is_staff'] = True
        kwargs['is_superuser'] = True
        return self._create_user(telephone=telephone, username=username, password=password, **kwargs)



class User(AbstractBaseUser, PermissionsMixin):
    uuid = ShortUUIDField(primary_key=True)
    username = models.CharField(max_length=15)
    telephone = models.CharField(max_length=11, unique=True, validators=[validators.RegexValidator(r'1[35678]\d{9}')])
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'telephone'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username