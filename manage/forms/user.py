#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
from django import forms
from django.forms import fields, widgets


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
