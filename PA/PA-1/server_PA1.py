#!/usr/bin/python

import socket
import sys
import time

UDP_IP = sys.argv[1]    # Server's IP
print "Server's IP is ", UDP_IP
UDP_PORT = 3333                                     # Port for server process
print "Server's Port is ", UDP_PORT

sock = socket.socket(socket.AF_INET,        # Internet
                     socket.SOCK_DGRAM)     # UDP

sock.bind((UDP_IP, UDP_PORT))               # Bind the socket

while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    receive_time = time.time()       # Timestamp of server receiving request
    if (data == "TIME"):             # Check if it is the request for TIME Sync
        print "\n\nReceived TIME request from", addr
        sock.sendto(str(receive_time)+","+str(time.time()),addr)    # Send response
