#!/usr/bin/env python 
# -*- coding: utf-8 -*- 


import json
from channels import Group, channel
from channels.auth import channel_session_user, channel_session_user_from_http,channel_session
from manage import models


@channel_session_user_from_http
def ws_connect(message):
    Group('users').add(message.reply_channel)
    Group('users').send({
        'text': json.dumps({
            'username': message.user.username,
            'is_logged_in': True
        })
    })


@channel_session_user
def ws_disconnect(message):
    Group('users').send({
        'text': json.dumps({
            'username': message.user.username,
            'is_logged_in': False
        })
    })
    Group('users').discard(message.reply_channel)


@channel_session_user_from_http
def user_connect(message):
    message.reply_channel.send({'accept': True})
    # print('user:{},connect'.format(message.user.username))
    print(message.content)


# {'path': '/talk/', 'headers': [[b'host', b'127.0.0.1:8080'], [b'connection', b'Upgrade'], [b'pragma', b'no-cache'], [b'cache-control', b'no-cache'], [b'upgrade', b'websocket'], [b'origin', b'http://127.0.0.1:8080'], [b'sec-websocket-version', b'13'], [b'user-agent', b'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'], [b'accept-encoding', b'gzip, deflate, br'], [b'accept-language', b'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4'], [b'cookie', b'csrftoken=rN8y5BKbbqsSSYGRKcwtSiHT9YbVRRYCqH55eka1Xku341mqTtxlBjPzGrmj2avw; sessionid=y2f7yvtc8yeo0yt7qetlnsz22408wxhm'], [b'sec-websocket-key', b'pO6W9Vz4zZWihHwYlTNQwg=='], [b'sec-websocket-extensions', b'permessage-deflate; client_max_window_bits']], 'query_string': b'', 'client': ['127.0.0.1', 50716], 'server': ['127.0.0.1', 8080], 'reply_channel': 'daphne.response.tJptszxPwO!VyPKqGhein', 'order': 0, 'method': 'FAKE'}

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



# ['__class__', '__contains__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setitem__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'channel', 'channel_layer', 'channel_session', 'content', 'copy', 'get', 'items', 'keys', 'reply_channel', 'user', 'values']
# {'reply_channel': 'daphne.response.AXohEbuATi!WAvVTaawST', 'path': '/talk/', 'order': 1, 'text': '安抚'}
