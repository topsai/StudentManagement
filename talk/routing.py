#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
from channels import route
from talk.comsumers import ws_connect, ws_disconnect, ws_receive

channel_routing = [
    route('websocket.connect', ws_connect),
    route('websocket.disconnect', ws_disconnect),
    route('websocket.receive', ws_receive)
]