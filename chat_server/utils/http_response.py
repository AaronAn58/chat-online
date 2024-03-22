# -*- coding: utf-8 -*-

"""
@author: Aaron.An
@contact: QQ:294964314
@Created on: 2024/1/25 14:09
@Remark: 
"""
from rest_framework.response import Response


class HttpCode(object):
    OK = 200
    PARAMS_ERROR = 400
    UN_AUTH = 401
    METHOD_ERROR = 405
    SERVER_ERROR = 500
    IS_EXIT = 422
    LOGIN_NO = 303
    LOGIN_YES = 302
    NO_DATA = 0


class HttpResponse(Response):
    def __init__(self, code=HttpCode.OK, data=None, msg="success", status=None, template_name=None, headers=None,
                 exception=False, content_type=None, pagination=None):
        if pagination is not None:
            std_data = {
                "code": code,
                "data": data,
                "msg": msg,
                "pagination": pagination
            }
        else:
            std_data = {
                "code": code,
                "data": data,
                "msg": msg,
            }
        super().__init__(std_data, status, template_name, headers, exception, content_type)
