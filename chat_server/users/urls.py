# -*- coding: utf-8 -*-

"""
@author: Aaron.An
@contact: QQ:294964314
@Created on: 2024/3/21 10:27
@Remark: 
"""
from django.urls import path

from chat_server.users.views import LoginNoCaptchaView, RegisterView

urlpatterns = (
    [
        path("api/loginNoCap/", LoginNoCaptchaView.as_view(), name="loginNoCap"),
        path("api/register/", RegisterView.as_view({'post': 'update'}), name="register")
    ]
)
