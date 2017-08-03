#!/usr/bin/env python
# -*- coding: utf-8 -*-
from myadmin import actions as act


registry = {}


# basemodel
class Base(object):
    list_display = '__all__'
    # modelform显示的字段
    fields = ()
    ordering = []
    actions = []
    inlines = []

    def __init__(self, model, ):  # admin_site
        self.model = model
        self.opts = model._meta
        self._actions = {'delete_selected': act.delete_selected}
        if self.actions:
            for i in self.actions:
                if hasattr(self, i):
                    action = getattr(self, i)
                    self._actions[i] = action
        # 检查ordering字段是否合法,不合法会报错
        if self.ordering:
            for i in self.ordering:
                self.model._meta.get_field(i.lstrip('-'))

    # 获取所有actions字典
    def get_action(self):
        # 初始化默认actions
        return self._actions


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





