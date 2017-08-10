#!/usr/bin/env python 
# -*- coding: utf-8 -*- 


from django.contrib.auth import get_user_model, password_validation
from myadmin.create_modelform import *
from myadmin import myadmbase
from myadmin.myadmbase import Base, register, registry
from myadmin import models
from django.contrib import messages
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth.forms import UsernameField
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


class UserCreationForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        # label="Password confirmation",
        widget=forms.PasswordInput,
        strip=False,
        help_text=_("Enter the same password as before, for verification. hhh"),
        # help_text="Enter the same password as before, for verification. hhhh",
    )
    # email = forms.EmailField(
    #     label='email..',
    #     widget=forms.EmailField,
    #     help_text='请输入邮箱',
    # )

    class Meta:
        model = get_user_model()
        fields = ("username",)
        field_classes = {'username': UsernameField}

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs.update({'autofocus': True})

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        self.instance.username = self.cleaned_data.get('username')
        password_validation.validate_password(self.cleaned_data.get('password2'), self.instance)
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserModel(Base):
    form = None
    add_form = UserCreationForm
    # 显示的字段
    list_display = ['id', 'username', 'password', 'email', 'last_login', 'auths']
    # list_display = '__all__'
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
register(models.Permissions)
