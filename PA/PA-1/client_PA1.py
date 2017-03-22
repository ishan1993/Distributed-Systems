#!/usr/bin/python

import socket
import sys
import time

UDP_IP = sys.argv[1]    # Server's IP
UDP_PORT = 3333         # Server's Port
MESSAGE = "TIME"        # Request message
data = 0                # Variable to check if any data is received

sock = socket.socket(socket.AF_INET,    # Internet
                     socket.SOCK_DGRAM) # UDP


sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
request_time = time.time()  # Timestamp for client sending request

data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
response_time = time.time() # Timestamp of client receiving response from server
if(data != 0):
    server_time_list = data.split(',')  # Parse server's response
    server_receive = server_time_list[0]    # Timestamp of server receiving request
    server_response = server_time_list[1]   # Timestamp of server sending response
    print "\n\nRequest sent at ",request_time
    print "Server received request at ", server_receive
    print "\nServer sent response at ", server_response
    print "Response received at ", response_time
