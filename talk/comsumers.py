#!/usr/bin/env python 
# -*- coding: utf-8 -*-
from channels import Group
from constantly import

# from django.contrib.gis.gdal.raster import const
# from django.contrib.gis.db.backends.postgis import const
# from twisted.internet.iocpreactor import const
# from infi.instruct.struct import const

def ws_connect(message):
    message.reply_channel.send({'accept': True})
    Group(const.GROUP_NAME).add(message.reply_channel)

def ws_disconnect(message):
    Group(const.GROUP_NAME).discard(message.reply_channel)

def ws_receive(message):
    pass