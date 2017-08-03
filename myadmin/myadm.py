#!/usr/bin/env python
# -*- coding: utf-8 -*-
from myadmin import actions as act
from django.contrib.auth import get_user_model
from myadmin import models
from django import forms
from django.forms import ModelForm, widgets, fields
from django.contrib import messages

User = get_user_model()
registry = {}


# actions = {'delete_selected': act.delete_selected}


class Base(object):
    #  basemodel
    list_display = '__all__'
    # modelform显示的字段
    fields = ()
    ordering = []
    actions = []
    inlines = []

    def __init__(self, model, ):  # admin_site
        self.model = model
        self.opts = model._meta
        # self._actions = {'delete_selected': act.delete_selected}
        act.delete_selected.short_description = '删除所选的 {}'.format(self.model._meta.verbose_name_plural)
        self.actions = {'delete_selected': act.delete_selected}
        if self.actions:
            for i in self.actions:
                if hasattr(self, i):
                    action = getattr(self, i)
                    self.actions[i] = action
        # 检查ordering字段是否合法
        if self.ordering:
            for i in self.ordering:
                pass

    # 获取所有actions字典
    def get_action(self):
        # 初始化默认actions
        return self.actions


class DefaultModelAdmin(Base):
    list_display = "__all__"


class MenuModel(Base):
    list_display = ['id', 'name', 'url_name']
    actions = []
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


# class AdminSite(object):
#     def __init__(self, name='admin'):
#         self._registry = {}  # model_class class -> admin_class instance
#         self.name = name
#         # self._actions = {'delete_selected': actions.delete_selected}
#         self._actions = {}
#         self._global_actions = self._actions.copy()
#         # all_sites.add(self)

class Site:
    def __init__(self):
        self._registry = {}
        self._actions = None

    def register(self, model, admin_class=None, **options):
        print('model:', model, 'admin_class', admin_class)
        self._registry = {}  # model_class class -> admin_class instance
        # self.name = name
        self._actions = {'delete_selected': act.delete_selected}
        # self._global_actions = self._actions.copy()
        # all_sites.add(self)
        if not admin_class:
            admin_class = DefaultModelAdmin
        # if model._meta.app_label not in self._registry:
        #     self._registry[model._meta.app_label] = {}
        if options:
            options['__module__'] = __name__
            admin_class = type("%sAdmin" % model.__name__, (admin_class,), options)
        # usermodel = UserModel()
        # admin_class.model = model
        # self._registry[model._meta.app_label][model._meta.model_name] = admin_class(model)
        self._registry[model] = admin_class(model, '123', )
        print(self._registry)


def register(model, admin_class=None, **options):
    # actions = {'delete_selected': act.delete_selected}
    # self._global_actions = self._actions.copy()
    # all_sites.add(self)
    if not admin_class:
        admin_class = DefaultModelAdmin
    if model._meta.app_label not in registry:
        registry[model._meta.app_label] = {}
    if options:
        options['__module__'] = __name__
        admin_class = type("%sAdmin" % model.__name__, (admin_class,), options)
    registry[model._meta.app_label][model._meta.model_name] = admin_class(model)


register(models.Menu, MenuModel)
register(models.Authority, AuthorityModel)
register(User, UserModel)


def create_modelforms(request, admin_class):
    def __new__(cls, *args, **kwargs):
        # print(cls.fields)
        # print(dir(cls))
        for field_name, field_obj in cls.base_fields.items():
            if isinstance(field_obj.widget, widgets.CheckboxInput):
                # field增加一个参数，方便前端获取widget 类型
                field_obj.type = 'checkbox'
            # elif isinstance(field_obj.widget, widgets.Select):
            #     field_obj.widget.attrs['class'] = 'checkbox'

            else:
                field_obj.widget.attrs['class'] = 'form-control '
        return forms.ModelForm.__new__(cls)

    class Meta:
        model = admin_class.model
        fields = "__all__"

    attr = {'Meta': Meta}
    obj = type('mf', (forms.ModelForm,), attr)
    setattr(obj, '__new__', __new__)
    return obj
