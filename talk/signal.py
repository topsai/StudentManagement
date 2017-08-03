#!/usr/bin/env python 
# -*- coding: utf-8 -*- 


from django.contrib.auth import user_logged_in, user_logged_out
from django.dispatch import receiver
from manage.models import LoggedInUser


@receiver(user_logged_in)
def on_user_login(sender, **kwargs):
    print(kwargs.get('user'), 'login')
    LoggedInUser.objects.get_or_create(user=kwargs.get('user'))


@receiver(user_logged_out)
def on_user_logout(sender, **kwargs):
    print(kwargs.get('user'), 'logout')
    LoggedInUser.objects.filter(user=kwargs.get('user')).delete()
