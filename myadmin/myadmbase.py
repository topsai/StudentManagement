#!/usr/bin/env python
# -*- coding: utf-8 -*-
from myadmin import actions as act
from myadmin.create_modelform import create_modelforms
from django.contrib.auth.backends import ModelBackend

registry = {}


# basemodel
class Base(object):
    list_display = '__all__'
    # modelform显示的字段
    fields = ()
    ordering = []
    actions = []
    inlines = []
    form = None
    add_form = None

    def __init__(self, model, ):  # admin_site
        self.model = model
        self.opts = model._meta
        self._actions = {'delete_selected': act.delete_selected}
        self._list_display = []
        # 初始化所有actions
        if self.actions:
            for i in self.actions:
                if hasattr(self, i):
                    action = getattr(self, i)
                    self._actions[i] = action
        # 检查ordering字段是否合法,不合法会报错
        if self.ordering:
            for i in self.ordering:
                self.model._meta.get_field(i.lstrip('-'))
        if self.list_display == '__all__':
            for i in self.model._meta.fields:
                self._list_display.append(i.attname)
            print(self._list_display)

    # 获取所有actions字典
    def get_action(self):
        # 初始化默认actions
        return self._actions

    # 获取modelform
    def get_modelform(self, args=None):
        # args 有参数代表是添加数据，返回add form
        if args:
            print('add form :', self.add_form)
            return self.add_form or create_modelforms(self)
        else:
            print('form :', self.form)
            return self.form or create_modelforms(self)

    # 获取list_display
    def get_list_display(self):
        return self._list_display or self.list_display


class DefaultModelAdmin(Base):
    list_display = "__all__"


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


# 自定义认证后端
class MyModelBackend(object):
    def get_all_permissions(self, user_obj, obj=None):
        pass

    # def has_perm(self, user_obj, perm, obj=None):
    #     if not user_obj.is_active:
    #         return False
    #     return perm in self.get_all_permissions(user_obj, obj)
    def has_perm(self, user_obj, perm, obj=None):
        # print(user_obj)
        # print(perm)
        return 6667
