# -*- coding: utf-8 -*-

"""
@author: Aaron.An
@contact: QQ:294964314
@Created on: 2024/3/21 10:47
@Remark: 
"""
from django.db import models


class CoreModel(models.Model):
    """
    核心标准抽象模型模型,可直接继承使用
    增加审计字段, 覆盖字段时, 字段名称请勿修改, 必须统一审计字段名称
    """
    id = models.BigAutoField(primary_key=True, help_text="Id", verbose_name="Id")
    desc = models.CharField(max_length=255, verbose_name="描述", null=True, blank=True, help_text="描述")
    creator = models.CharField(max_length=255, null=True, verbose_name='创建人', help_text="创建人")
    modifier = models.CharField(max_length=255, null=True, blank=True, help_text="修改人", verbose_name="修改人")
    is_delete = models.BooleanField('是否删除', default=False)
    update_time = models.DateTimeField(auto_now=True, null=True, blank=True, help_text="修改时间",
                                       verbose_name="修改时间")
    create_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, help_text="创建时间",
                                       verbose_name="创建时间")

    class Meta:
        abstract = True
        verbose_name = '核心模型'
        verbose_name_plural = verbose_name
