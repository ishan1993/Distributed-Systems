#!/usr/bin/python

import socket
import sys
import time

UDP_IP = "localhost"    # Server's IP
UDP_PORT = 5002         # Server's Port
data = 0                # Variable to check if any data is received

sock = socket.socket(socket.AF_INET,    # Internet
                     socket.SOCK_DGRAM) # UDP


sock.sendto("INC", (UDP_IP, UDP_PORT))
time.sleep(1)
sock.sendto("INC", (UDP_IP, UDP_PORT))
time.sleep(1)
sock.sendto("INC", (UDP_IP, UDP_PORT))
time.sleep(1)
sock.sendto("GET", (UDP_IP, UDP_PORT))
data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes

if(data != 0):
    print data
