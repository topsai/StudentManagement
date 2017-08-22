#!/usr/bin/env python 
# -*- coding: utf-8 -*-
from django import template
from django.utils.safestring import mark_safe
from django.forms import widgets
register = template.Library()


@register.simple_tag
def get_action(obj):
    # 获取action
    tags = []
    actions = obj.get_action()
    for action_name, action in actions.items():
        tag = """<option value = "{}"> {} </option>""". \
            format(action_name, action.short_description if hasattr(action, 'short_description') else action_name)
        # 格式化默认action的short_description
        tags.append(tag.format(default_short_description=obj.model._meta.verbose_name_plural))
    return mark_safe('\n'.join(tags))


@register.simple_tag
def dir_obj(obj):
    return dir(obj)


@register.simple_tag
def check_checkbox(obj):
    return isinstance(obj.widget, widgets.CheckboxInput)


@register.simple_tag
def obj_getattr(obj, item):

    return getattr(obj, item)


@register.simple_tag
def get_name_or_verbose_name(obj):
    return obj.model._meta.verbose_name_plural


def recursive_related_objs_lookup(objs):
    # model_name = objs[0]._meta.model_name
    ul_ele = "<ul>"
    for obj in objs:
        li_ele = '''<li><span class='btn-link'> %s:</span> %s </li>''' % (
            obj._meta.verbose_name, obj.__str__().strip("<>"))
        ul_ele += li_ele

        # for local many to many
        # print("------- obj._meta.local_many_to_many", obj._meta.local_many_to_many)
        for m2m_field in obj._meta.local_many_to_many:  # 把所有跟这个对象直接关联的m2m字段取出来了
            sub_ul_ele = "<ul>"
            m2m_field_obj = getattr(obj, m2m_field.name)  # getattr(customer, 'tags')
            for o in m2m_field_obj.select_related():  # customer.tags.select_related()
                li_ele = '''<li> %s: %s </li>''' % (m2m_field.verbose_name, o.__str__().strip("<>"))
                sub_ul_ele += li_ele

            sub_ul_ele += "</ul>"
            ul_ele += sub_ul_ele  # 最终跟最外层的ul相拼接

        for related_obj in obj._meta.related_objects:
            if 'ManyToManyRel' in related_obj.__repr__():

                if hasattr(obj, related_obj.get_accessor_name()):  # hassattr(customer,'enrollment_set')
                    accessor_obj = getattr(obj, related_obj.get_accessor_name())
                    # print("-------ManyToManyRel",accessor_obj,related_obj.get_accessor_name())
                    # 上面accessor_obj 相当于 customer.enrollment_set
                    if hasattr(accessor_obj, 'select_related'):  # slect_related() == all()
                        target_objs = accessor_obj.select_related()  # .filter(**filter_coditions)
                        # target_objs 相当于 customer.enrollment_set.all()

                        sub_ul_ele = "<ul style='color:red'>"
                        for o in target_objs:
                            li_ele = '''<li> <span class='btn-link'>%s</span>: %s </li>''' % (
                                o._meta.verbose_name, o.__str__().strip("<>"))
                            sub_ul_ele += li_ele
                        sub_ul_ele += "</ul>"
                        ul_ele += sub_ul_ele

            elif hasattr(obj, related_obj.get_accessor_name()):  # hassattr(customer,'enrollment_set')
                accessor_obj = getattr(obj, related_obj.get_accessor_name())
                # 上面accessor_obj 相当于 customer.enrollment_set
                if hasattr(accessor_obj, 'select_related'):  # slect_related() == all()
                    target_objs = accessor_obj.select_related()  # .filter(**filter_coditions)
                    # target_objs 相当于 customer.enrollment_set.all()
                else:
                    # print("one to one i guess:",accessor_obj)
                    target_objs = [accessor_obj]
                # print("target_objs",target_objs)
                if len(target_objs) > 0:
                    # print("\033[31;1mdeeper layer lookup -------\033[0m")
                    # nodes = recursive_related_objs_lookup(target_objs,model_name)
                    nodes = recursive_related_objs_lookup(target_objs)
                    ul_ele += nodes
    ul_ele += "</ul>"
    return ul_ele


@register.simple_tag
def display_obj_related(objs):
    '''把对象及所有相关联的数据取出来'''
    if objs:
        model_class = objs[0]._meta.model
        # mode_name = objs[0]._meta.model_name
        return mark_safe(recursive_related_objs_lookup(objs))
