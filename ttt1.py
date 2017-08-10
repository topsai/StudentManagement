#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

from pyfirmata import Arduino, util
import time
board = Arduino('COM8')
time.sleep(5)
it = util.Iterator(board)
it.start()
a0 = board.get_pin('a:0:i')
a1 = board.get_pin('d:12:o')
a2 = board.get_pin('d:13:o')
time.sleep(1)
i = 0
while True:
    try:
        a1.write(i % 2)
        a2.write(i % 2)
        print('湿度：{:.2%}'.format(1-float(a0.read())))
        print('灯{}'.format('开'if a1.read() else '关'))

        i+=1
        time.sleep(0.1)
    except:
        time.sleep(1)
        print('err')
