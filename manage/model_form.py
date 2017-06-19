#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

from django import forms
from django.forms import widgets, fields
from manage import models



class UserInfoMF(forms.ModelForm):
    class Meta:
        model = models.Student
        fields = '__all__'


class LoginMF(forms.ModelForm):
    class Meta:
        model = models.Student
        fields = ['name', 'pwd']


# class HostGroupMF(forms.ModelForm):
#     hosts = forms.ModelMultipleChoiceField(queryset=models.HostInfo.objects.all())
#
#     class Meta:
#         model = models.HostGroup
#         fields = ['name', 'hosts']
#
#
# class HostGroupF(forms.Form):
#     hosts = fields.MultipleChoiceField(
#         choices=models.HostInfo.objects.all().values_list('id', 'name'),
#     )
