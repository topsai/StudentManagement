#!/usr/bin/env python 
# -*- coding: utf-8 -*- 


import urllib.request
from bs4 import BeautifulSoup
import re
import os
import requests

##########################################
# # get ip address
# url = "http://1212.ip138.com/ic.asp"
# url_op = urllib.request.urlopen(url)
# url_content = url_op.read()
# # ip_content = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', url_content)
# # ipcode = ''.join(ip_content)
#
# soup = BeautifulSoup(url_content)
# # print(soup)
# # head = soup.find('head')
# # title = soup.find('title')
# body = soup.find('body').find('center').get_text()
# a = re.findall('\[(\w+\.\w+\.\w+\.\w+)\]', body)
# print(a[0])
#
#
# def my_ip():
#     get_ip_method = os.popen('curl -s ip.cn')
#     get_ip_responses = get_ip_method.readlines()[0]
#     get_ip_pattern = re.compile(r'\d+\.\d+\.\d+\.\d+')
#     get_ip_value = get_ip_pattern.findall(get_ip_responses)[0]
#     return get_ip_value
ip = requests.get('http://1212.ip138.com/ic.asp')
ip.encoding = 'gb2312'
# print(ip.text)
soup = BeautifulSoup(ip.text, "html.parser")
center = soup.find('center')
print(center.text)
t = re.search('\d+\.\d+\.\d+\.\d+', center.text)
print(t.group())


try:
    print('try')
except Exception as e:
    print('err', e)
else:
    print('no error')
finally:
    print('finally')



# Echo server program
import socket

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 50007              # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()
print('Connected by', addr)
while 1:
    data = conn.recv(1024)
    if not data: break
    conn.sendall(data)
conn.close()

# Echo client program
import socket

HOST = 'daring.cwi.nl'    # The remote host
PORT = 50007              # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.sendall('Hello, world')
data = s.recv(1024)
s.close()
print('Received', repr(data))