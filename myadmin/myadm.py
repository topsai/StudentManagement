#!/usr/bin/env python 
# -*- coding: utf-8 -*- 


from django.contrib.auth import get_user_model
from myadmin.create_modelform import *
from myadmin import myadmbase
from myadmin.myadmbase import Base, register, registry
from myadmin import models
from django.contrib import messages
User = get_user_model()


class MenuModel(Base):
    list_display = ['id', 'name', 'url_name']
    actions = ['delete_menu']
    ordering = ['-id']

    def delete_menu(self, request, queryset):
        try:
            # rows_updated = queryset.update(is_active=False)
            messages.info(request, "%s 条记录修改完成." % len(queryset))
        except Exception as e:
            messages.error(request, "{}:修改失败".format(e))

    delete_menu.short_description = '删除所选的 菜单'


class AuthorityModel(Base):
    list_display = ['id', 'name']


class UserModel(Base):
    # 显示的字段
    list_display = ['id', 'username', 'password', 'email', 'last_login', 'auths']
    # modelform显示的字段
    fields = (
        'username',
        'email',
        'phone',
        'qq',
        'is_active',
        'is_superuser',
        'date_joined',
        'user_type',
        'user_class',
    )
    # 排序的列
    ordering = ['id']
    # 绑定action
    actions = ['disabled_user', 'abled_user']

    # inlines = [UserInline]

    def disabled_user(self, request, queryset):
        try:
            rows_updated = queryset.update(is_active=False)
            self.message_user(request, "%s 条记录修改完成." % rows_updated)
        except Exception as e:
            self.message_user(request, "{}:修改失败".format(e))

    disabled_user.short_description = '禁用所选的 用户'


register(models.Menu, MenuModel)
register(models.Authority, AuthorityModel)
register(User, UserModel)
