#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
from django.contrib import messages


# 默认actions
def delete_selected(modeladmin, request, queryset):
    model = modeladmin.model
    count = queryset.count()
    try:
        queryset.delete()
        messages.info(request, "{}:条记录删除完成.".format(count))
    except Exception as e:
        messages.error(request, "修改失败:{}".format(e))
# action名字，前端tags根据当前请求进行格式化
delete_selected.short_description = '删除所选的 {default_short_description}'



