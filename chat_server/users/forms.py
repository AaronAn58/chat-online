# -*- coding: utf-8 -*-

"""
@author: Aaron.An
@contact: QQ:294964314
@Created on: 2024/3/20 22:58
@Remark: 
"""
from django.contrib.auth.forms import UserCreationForm

from chat_server.users.models import Users


class RegistrationForm(UserCreationForm):

    class Meta:
        model = Users
        fields = ('username', 'phone', 'password1', 'password2')