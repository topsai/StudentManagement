#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
from django.contrib import messages


def delete_selected(modeladmin, request, queryset):
    model = modeladmin.model
    count = queryset.count()
    try:
        queryset.delete()
        messages.info(request, "{}:条记录删除完成.".format(count))
    except Exception as e:
        messages.error(request, "修改失败:{}".format(e))


def get_info(obj):
    l = {}
    for i in dir(obj):
        l[i] = getattr(obj, i)
    return l


delete_selected.short_description = '删除所选的 {}'

