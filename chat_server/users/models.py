import hashlib

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

from chat_server.chat_server.settings import SYSTEM_USER_GENDER, SYSTEM_USER_TYPE, TABLE_PREFIX


# Create your models here.

class CustomUserManager(UserManager):
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        user = super(CustomUserManager, self).create_superuser(username, email, password, **extra_fields)
        user.set_password(password)
        try:
            user.save(using=self._db)
            return user
        except ObjectDoesNotExist:
            user.delete()
            raise ValidationError("角色`管理员`不存在, 创建失败, 请先执行python manage.py init")


class Users(AbstractUser):
    username = models.CharField(max_length=100, unique=True, db_index=True, verbose_name="用户名", help_text="用户名")
    email = models.EmailField(max_length=255, verbose_name="邮箱", help_text="邮箱", null=True, blank=True)
    phone = models.CharField(max_length=50, verbose_name="手机号", help_text="手机号", null=True, blank=True)
    avatar = models.CharField(max_length=255, verbose_name="头像", help_text="头像", null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name="姓名", help_text="姓名", null=True, blank=True)
    gender = models.IntegerField(choices=SYSTEM_USER_GENDER, default=0, verbose_name="性别", help_text="性别")
    user_type = models.IntegerField(choices=SYSTEM_USER_TYPE, default=0, verbose_name="用户类型", help_text="用户类型")
    is_online = models.BooleanField(default=False, verbose_name="是否在线")
    role = models.ForeignKey('Role', on_delete=models.DO_NOTHING, null=True)
    update_time = models.DateTimeField(auto_now=True, null=True, blank=True, help_text="修改时间",
                                       verbose_name="修改时间")
    create_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, help_text="创建时间",
                                       verbose_name="创建时间")
    creator = models.CharField(max_length=255, null=True, verbose_name='创建人', help_text="创建人")
    modifier = models.CharField(max_length=255, null=True, blank=True, help_text="修改人", verbose_name="修改人")

    objects = CustomUserManager()

    def set_password(self, raw_password):
        super().set_password(hashlib.md5(raw_password.encode(encoding="UTF-8")).hexdigest())

    class Meta:
        db_table = TABLE_PREFIX + 'users'
        verbose_name = "用户表"
        verbose_name_plural = verbose_name
        ordering = ("create_time",)

    def __str__(self):
        return self.username
