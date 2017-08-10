#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

import serial
import json
import time
import datetime
import logging

# logging.basicConfig(level=logging.DEBUG,
#                     format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
#                     datefmt='%a, %d %b %Y %H:%M:%S',
#                     filename='state.log',
#                     filemode='w',
#                     )
# 第一步，创建一个logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)  # Log等级总开关

# 第二步，创建一个handler，用于写入日志文件
logfile = 'state.log'
fh = logging.FileHandler(logfile, mode='w')
fh.setLevel(logging.DEBUG)  # 输出到file的log等级的开关

# 第三步，再创建一个handler，用于输出到控制台
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)  # 输出到console的log等级的开关

# 第四步，定义handler的输出格式
formatter = logging.Formatter("%(asctime)s - %(levelname)s: %(message)s")
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# 第五步，将logger添加到handler里面
logger.addHandler(fh)
logger.addHandler(ch)

arduino = serial.Serial('COM8')
print(arduino.is_open)
last_status = 0
humidity = 0
while True:
    if arduino.readable():
        data = json.loads(arduino.readline().decode().lstrip('state:'))
        now_humidity = (1023 - data[1]) / 1023
        if abs(humidity-now_humidity) > 0.01:
            humidity = now_humidity
            print(humidity)
        if last_status != data[0]:
            # print()
            print(humidity)
            logger.info('light is {}'.format('opend' if data[0] else 'closed'))
            last_status = data[0]
