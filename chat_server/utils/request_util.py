# -*- coding: utf-8 -*-

"""
@author: Aaron.An
@contact: QQ:294964314
@Created on: 2024/1/26 16:58
@Remark: 
"""
import requests
from django.conf import settings

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from user_agents import parse

from system.models import LoginLog


def get_ip_analysis(ip):
    data = {
        "continent": "",
        "country": "",
        "province": "",
        "city": "",
        "district": "",
        "isp": "",
        "area_code": "",
        "country_english": "",
        "country_code": "",
        "longitude": "",
        "latitude": ""
    }
    if ip != 'unknown' and ip:
        if getattr(settings, 'ENABLE_LOGIN_ANALYSIS_LOG', True):
            res = requests.get(url='https://ip.django-vue-admin.com/ip/analysis', params={"ip": ip}, timeout=5)
            if res.status_code == 200:
                res_data = res.json()
                if res_data.get('code') == 0:
                    data = res_data.get('data')
            return data
    return data


def save_login_log(request):
    ip = get_request_ip(request=request)
    analysis_data = get_ip_analysis(ip)
    analysis_data['username'] = request.user.username
    analysis_data['ip'] = ip
    analysis_data['agent'] = str(parse(request.META['HTTP_USER_AGENT']))
    analysis_data['browser'] = get_browser(request)
    analysis_data['os'] = get_os(request)
    analysis_data['creator_id'] = request.user.id
    analysis_data['dept_belong_id'] = getattr(request.user, 'dept_id', '')
    LoginLog.objects.create(**analysis_data)


def get_request_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR', '')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
        return ip
    ip = request.META.get('REMOTE_ADDR', '') or getattr(request, 'request_ip', None)
    return ip or 'unknown'


def get_request_user(request):
    user: AbstractBaseUser = getattr(request, 'user', None)
    if user and user.is_authenticated:
        return user
    try:
        user, token = JWTAuthentication().authenticate(request)
    except Exception:
        pass
    return user or AnonymousUser()


def get_browser(request):
    ua_string = request.META['HTTP_USER_AGENT']
    user_agent = parse(ua_string)
    return user_agent.get_browser()


def get_os(request):
    ua_string = request.META['HTTP_USER_AGENT']
    user_agent = parse(ua_string)
    return user_agent.get_os()
