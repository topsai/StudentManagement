#!/usr/bin/env python
# -*- coding: utf-8 -*-


loan = 131000
interest_rate = 0.0057
Monthly_interest = loan*interest_rate
Repayment = 131000/12
for i in range(12):
    Balance = loan - Repayment*i
    print(Monthly_interest/Balance*100)



from pyfirmata import Arduino, util
board = Arduino('/dev/tty.usbserial-A6008rIF')
board.digital[13].write(1)