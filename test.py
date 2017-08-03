#!/usr/bin/env python 
# -*- coding: utf-8 -*- 


# socket server
import socket
sk = socket.socket()
sk.bind(('127.0.0.1', 8080))
sk.listen(1)
conn, addr = sk.accept()
conn.send('Hello, welcome')
conn.recv(1024)
conn.close()


# socket client
import socket
cli = socket.socket()
cli.connect(('127.0.0.1', 8080))
cli.send('Hi')
cli.recv(1024)
cli.close()

