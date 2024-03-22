# -*- coding: utf-8 -*-

"""
@author: Aaron.An
@contact: QQ:294964314
@Created on: 2024/1/27 12:44
@Remark: 
"""
import hashlib
import logging
from django.utils import timezone

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import check_password
from rest_framework.exceptions import APIException

logger = logging.getLogger(__name__)
UserModel = get_user_model()


class CustomBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        msg = f"{username} 正在使用本地登录..."
        logger.info(msg)
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        try:
            user = UserModel._default_manager.get_by_natural_key(username)
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
        else:
            verify_password = check_password(password, user.password)
            if not verify_password:
                password = hashlib.md5(password.encode(encoding='utf-8')).hexdigest()
                verify_password = check_password(password, user.password)
            if verify_password:
                if self.user_can_authenticate(user):
                    user.last_login = timezone.now()
                    user.save()
                    return user
                raise APIException("用户被禁用")
