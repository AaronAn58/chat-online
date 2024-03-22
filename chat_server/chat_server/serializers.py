# -*- coding: utf-8 -*-

"""
@author: Aaron.An
@contact: QQ:294964314
@Created on: 2024/3/20 23:22
@Remark: 
"""
from django_restql.mixins import DynamicFieldsMixin
from rest_framework import serializers
from rest_framework.fields import empty
from rest_framework.request import Request
from rest_framework.serializers import ModelSerializer

from users.models import Users


class CustomModelSerializer(DynamicFieldsMixin, ModelSerializer):
    """
        增强DRF的ModelSerializer,可自动更新模型的审计字段记录
        (1)self.request能获取到rest_framework.request.Request对象
    """

    # 修改人的审计字段名称, 默认modifier, 继承使用时可自定义覆盖
    modifier_field_id = "modifier"
    # modifier = serializers.SerializerMethodField(read_only=True)

    # 创建人的审计字段名称, 默认creator, 继承使用时可自定义覆盖
    creator_field_id = "creator"
    # creator = serializers.SlugRelatedField(
    #     slug_field="name", source="creator", read_only=True
    # )
    # 添加默认时间返回格式
    create_time = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", required=False, read_only=True
    )
    update_time = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", required=False
    )

    def __init__(self, instance=None, data=empty, request=None, **kwargs):
        super().__init__(instance, data, **kwargs)
        self.request: Request = request or self.context.get("request", None)

    def get_modifier(self, instance):
        if not hasattr(instance, "modifier"):
            return None
        queryset = (
            Users.objects.filter(id=instance.modifier)
            .values_list("name", flat=True)
            .first()
        )
        if queryset:
            return queryset
        return None

    def get_request_username(self):
        if getattr(self.request, "user", None):
            return getattr(self.request.user, "username", None)
        return None

    def get_request_name(self):
        if getattr(self.request, "user", None):
            return getattr(self.request.user, "name", None)
        return None

    def get_request_user_id(self):
        if getattr(self.request, "user", None):
            return getattr(self.request.user, "id", None)
        return

    def create(self, validated_data):
        if self.request:
            if str(self.request.user) != "AnonymousUser":
                if self.modifier_field_id in self.fields.fields:
                    validated_data[self.modifier_field_id] = self.get_request_user_id()
                if self.creator_field_id in self.fields.fields:
                    validated_data[self.creator_field_id] = self.request.user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if self.request:
            if str(self.request.user) != "AnonymousUser":
                if self.modifier_field_id in self.fields.fields:
                    validated_data[self.modifier_field_id] = self.get_request_user_id()
            if hasattr(self.instance, self.modifier_field_id):
                setattr(
                    self.instance, self.modifier_field_id, self.get_request_user_id()
                )
        return super().update(instance, validated_data)

    @property
    def errors(self):
        # get errors
        errors = super().errors
        verbose_errors = {}

        # fields = { field.name: field.verbose_name } for each field in model
        fields = {field.name: field.verbose_name for field in
                  self.Meta.model._meta.get_fields() if hasattr(field, 'verbose_name')}

        # iterate over errors and replace error key with verbose name if exists
        for field_name, error in errors.items():
            if field_name in fields:
                verbose_errors[str(fields[field_name])] = error
            else:
                verbose_errors[field_name] = error
        return verbose_errors
