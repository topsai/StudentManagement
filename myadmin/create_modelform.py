#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
from django.forms import ModelForm, widgets, fields
from django import forms
from myadmin import models
# __all__ = (
#     'Media', 'MediaDefiningClass', 'Widget', 'TextInput', 'NumberInput',
#     'EmailInput', 'URLInput', 'PasswordInput', 'HiddenInput',
#     'MultipleHiddenInput', 'FileInput', 'ClearableFileInput', 'Textarea',
#     'DateInput', 'DateTimeInput', 'TimeInput', 'CheckboxInput', 'Select',
#     'NullBooleanSelect', 'SelectMultiple', 'RadioSelect',
#     'CheckboxSelectMultiple', 'MultiWidget', 'SplitDateTimeWidget',
#     'SplitHiddenDateTimeWidget', 'SelectDateWidget',
# )


def create_modelforms(admin_class=None):
    print('create model form', admin_class)
    _widgets = {}

    def __new__(cls, *args, **kwargs):
        print('cls', cls)
        print('cls base_fields', cls.base_fields.items())
        for field_name, field_obj in cls.base_fields.items():
            print(field_obj.widget)
            # TODO 待续
            _widgets[field_name] = forms.EmailField
            if isinstance(field_obj.widget, widgets.CheckboxInput):
                # field增加一个参数，方便前端获取widget 类型
                field_obj.type = 'checkbox'
            else:
                field_obj.widget.attrs['class'] = 'form-control '
        return forms.ModelForm.__new__(cls)

    class Meta:
        model = admin_class.model
        fields = "__all__"
        # widgets = {
        #     "username": forms.Textarea(attrs={'class': 'c1'}, )
        # }

    attr = {'Meta': Meta}
    obj = type('mf11', (forms.ModelForm,), attr)
    setattr(obj, '__new__', __new__)
    return obj


class UserInfoModelForm(forms.ModelForm):
    is_rember = forms.fields.CharField(widget=forms.widgets.CheckboxInput)  # 自定义额外字段

    class Meta:
        model = models.Menu
        fields = "__all__"  # 展示全部
        # fields = ["username", "email", "user_type", ]  # 写谁展示谁
        # exclude = ["username"]  # 排除哪一个
        labels = {
            "username": "用户名",
        }  # 指定label显示名字优先级高于models的verbose_name
        help_texts = {
            "username": "请输入用户名",
        }  # 帮助信息，没啥卵用
        widgets = {
            "username": forms.Textarea(attrs={'class': 'c1'}, )
        }  # 指定插件
        error_messages = {
            "__all__": {},  # 整体错误信息
            "username": {
                'required': "用户名不能为空",
            }
        }  # 指定错误信息
        field_classes = {
            'email': forms.fields.EmailField
        }  # 定义字段的类

    def clean_username(self):  # 钩子
        return self.cleaned_data["username"]


def modelform_factory(model, form=ModelForm, fields=None, exclude=None,
                      formfield_callback=None, widgets=None, localized_fields=None,
                      labels=None, help_texts=None, error_messages=None,
                      field_classes=None):
    """
    返回一个包含给定模型的表单字段的ModelForm。

    ``fields``是字段名称的可选列表。如果提供，则只有命名的字段将包含在返回的字段中。如果省略或“__all__”，将使用所有字段。

    ``exclude``是字段名称的可选列表。如果提供，则命名字段将从返回的字段中排除，即使它们在“fields”参数中列出。

    “widgets”是映射到小部件的模型字段名称的字典。

    `localized_fields``是应该被本地化的字段的名字列表。

    ``formfield_callback``是一个可调用的，它使用一个模型字段并返回一个表单域。

    ``labels``是映射到标签的模型字段名字典。

    ``help_texts``是映射到帮助文本的模型字段名字典。

    ``error_messages``是映射到错误消息字典的模型字段名字典。

    ``field_classes``是映射到表单字段类的模型字段名字典。
    """
    # 创建内部Meta类。
    # FIXME：理想情况下，我们应该能够构造一个ModelForm，而不需要创建和传递一个临时的内部类。 构建Meta对象将具有的属性列表。
    attrs = {'model': model}
    if fields is not None:
        attrs['fields'] = fields
    if exclude is not None:
        attrs['exclude'] = exclude
    if widgets is not None:
        attrs['widgets'] = widgets
    if localized_fields is not None:
        attrs['localized_fields'] = localized_fields
    if labels is not None:
        attrs['labels'] = labels
    if help_texts is not None:
        attrs['help_texts'] = help_texts
    if error_messages is not None:
        attrs['error_messages'] = error_messages
    if field_classes is not None:
        attrs['field_classes'] = field_classes

    # If parent form class already has an inner Meta, the Meta we're
    # creating needs to inherit from the parent's inner meta.
    parent = (object,)
    if hasattr(form, 'Meta'):
        parent = (form.Meta, object)
    Meta = type(str('Meta'), parent, attrs)
    if formfield_callback:
        Meta.formfield_callback = staticmethod(formfield_callback)
    # Give this new form class a reasonable name.
    class_name = model.__name__ + str('Form')

    # Class attributes for the new form class.
    form_class_attrs = {
        'Meta': Meta,
        'formfield_callback': formfield_callback
    }

    if (getattr(Meta, 'fields', None) is None and
                getattr(Meta, 'exclude', None) is None):
        raise ImproperlyConfigured(
            "Calling modelform_factory without defining 'fields' or "
            "'exclude' explicitly is prohibited."
        )

    # Instantiate type(form) in order to use the same metaclass as form.
    return type(form)(class_name, (form,), form_class_attrs)
