#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
from django import forms
from django.forms import fields, widgets
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model
import unicodedata

User = get_user_model()
class login_form(forms.Form):
    u = fields.CharField(widget=widgets.TextInput(attrs={'class': 'hidden'}),)
    name = fields.CharField(
        strip=True,
        widget=widgets.TextInput(attrs={'class': 'form-control', 'placeholder': "Username"}),
    )
    pwd = fields.CharField(
        strip=True,
        widget=widgets.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Username",
            'type': "password",
        }),
    )


class regist_form(forms.Form):
    username = fields.CharField(
        strip=True,
        widget=widgets.TextInput(attrs={'class': 'form-control', 'placeholder': "Username"}),
    )
    password = fields.CharField(
        strip=True,
        widget=widgets.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Password",
            'type': "password",
        }),
    )


class UsernameField(forms.CharField):
    def to_python(self, value):
        return unicodedata.normalize('NFKC', super(UsernameField, self).to_python(value))


class MyUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = ("username",)
        field_classes = {'username': UsernameField}
