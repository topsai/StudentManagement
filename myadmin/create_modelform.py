#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
from django.forms import ModelForm, widgets, fields
from django import forms


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




