#!/usr/bin/env python 
# -*- coding: utf-8 -*- 


import json
from channels import Group, channel
from channels.auth import channel_session_user, channel_session_user_from_http, channel_session
from manage import models


@channel_session_user_from_http
def ws_connect(message):
    print('ws_connect')
    if message.user.id:
        print(message.user)
        print(message.user.username)
        print(message.user.id)
    else:
        print("no ligin")
        message.reply_channel.send({'accept': True})
    Group('users').add(message.reply_channel)
    Group('users').send({
        'text': json.dumps({
            'username': message.user.username,
            'is_logged_in': True
        })
    })

@channel_session_user
def ws_disconnect(message):
    print('ws_disconnect')
    Group('users').send({
        'text': json.dumps({
            'username': message.user.username,
            'is_logged_in': False
        })
    })
    Group('users').discard(message.reply_channel)


@channel_session_user_from_http
def user_connect(message):
    print('user_connect')
    message.reply_channel.send({'accept': True})
    if message.user:
        print(message.user)
        print(message.user.username)
        print(message.user.id)
    else:
        print("no ligin")



@channel_session_user
def user_disconnect(message):
    print('user_disconnect')
    print(message.reply_channel)


@channel_session_user
def user_receive(message):
    data = json.loads(message['text'])
    print('从  %s  收到信息：%s ,接收者 %s ' % (message.user, data.get('text'), data.get('id')))
    models.Talk.objects.create(send=message.user, receive_id=data.get('id'), content=data.get('text'))
    # models.Talk.objects.create(send=message.user, receive_)
    # for i in message.keys:
    #     print(message.get(i))
    print(message.content)

