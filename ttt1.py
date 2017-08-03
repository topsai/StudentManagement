#!/usr/bin/env python 
# -*- coding: utf-8 -*- 


class A:
    a1 = 1
    a2 = []

    def __init__(self):
        self.b = 2
        self.a1 = 6
        # print('a1', self.a1)

a = A()
a.a2.append(8)
print('a------', a.__dict__)
print('A------', A.__dict__)


