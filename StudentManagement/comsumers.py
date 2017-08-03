#!/usr/bin/env python 
# -*- coding: utf-8 -*-
from channels import Group, Channel
# from channels.sessions import channel_session
from channels.sessions import channel_session
from channels.auth import http_session_user, channel_session_user, channel_session_user_from_http
import const



def ws_connect(message):
    # aaaa = ['channel', 'channel_layer', 'content', 'copy', 'get', 'items', 'keys', 'reply_channel', 'values']

    Group('users').add(message.reply_channel)



def ws_disconnect(message):

    # Group(const.GROUP_NAME).discard(message.reply_channel)
    Group('users').discard(message.reply_channel)



def ws_receive(message):
    print(message.http_session.get('channel'))
    # a = str(message.reply_channel)
    # print('3')
    # print(dir(message.channel_session))
    # print(message.channel, '|',
    #     message.channel_layer, '|',
    #     message.content, '|',
    #     message.copy, '|',
    #     message.get, '|',
    #     message.items, '|',
    #     message.keys, '|',
    #     message.reply_channel, '|',
    #     message.values,
    # )
    # print(message.content.get('text'))
    # message.reply_channel.send({'text': message.content.get('text')+'GGGG'})

    # Channel(a).send({'text': '111'})

