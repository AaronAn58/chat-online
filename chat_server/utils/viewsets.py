# -*- coding: utf-8 -*-

"""
@author: Aaron.An
@contact: QQ:294964314
@Created on: 2024/1/26 15:51
@Remark: 
"""
from django.db import transaction
from rest_framework.viewsets import ModelViewSet

from utils.http_response import HttpCode, HttpResponse


class CustomModelViewSet(ModelViewSet):
    values_queryset = None
    ordering_fields = "__all__"
    create_serializer_class = None
    update_serializer_class = None
    filter_fields = "__all__"
    search_fields = ()
    extra_filter_class = []
    permission_classes = []
    import_field_dict = {}
    export_field_label = {}

    def filter_queryset(self, queryset):
        for backend in set(set(self.filter_backends) | set(self.extra_filter_class or [])):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset

    def get_queryset(self):
        if getattr(self, 'values_queryset', None):
            return self.values_queryset
        return super().get_queryset()

    def get_serializer_class(self):
        action_serializer_name = f"{self.action}_serializer_class"
        action_serializer_class = getattr(self, action_serializer_name, None)
        if action_serializer_class:
            return action_serializer_class
        return super().get_serializer_class()

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())

        # can_see = self.get_menu_field(serializer_class)
        # self.request.permission_fields = can_see
        if isinstance(self.request.data, list):
            with transaction.atomic():
                return serializer_class(many=True, *args, **kwargs)
        else:
            return serializer_class(*args, **kwargs)

    # def get_menu_field(self):
    #     """获取字段权限"""
    #     finded = False
    #     for model in get_custom_app_models():
    #         if model['object'] is serializer_class.Meta.model:
    #             finded = True
    #             break
    #     if finded is False:
    #         return []
    #     return MenuField.objects.filter(model=model['model']
    #                                     ).values('field_name', 'title')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, request=request)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return HttpResponse(code=HttpCode.OK, data=serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, request=request)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True, request=request)
        return HttpResponse(code=HttpCode.OK, data=serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return HttpResponse(code=HttpCode.OK, data=serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, request=request, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return HttpResponse(code=HttpCode.OK, data=serializer.data, msg="Success")

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return HttpResponse(code=HttpCode.OK, data=[], msg="Success")
