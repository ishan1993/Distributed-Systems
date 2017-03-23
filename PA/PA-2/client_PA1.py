#!/usr/bin/python

import socket
import sys
import time

UDP_IP = "localhost"    # Server's IP
UDP_PORT = 5001         # Server's Port
data = 0                # Variable to check if any data is received

sock = socket.socket(socket.AF_INET,    # Internet
                     socket.SOCK_DGRAM) # UDP




while(1):
    print "Available commands\n\n"
    print "1. qCreate <label>"
    print "2. qId <label>"
    print "3. qPush <qId> <item>"
    print "4. qPop <qId>"
    print "5. qTop <qId>"
    print "6. qSize <qId>"
    user_input =  str(raw_input())
    input_parsed = user_input.split(' ')
    command = input_parsed[0]

    if(command == "qCreate"):
        label = input_parsed[1]
        sock.sendto("1,"+str(label)+",0", (UDP_IP, UDP_PORT))
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        print "id - ", data
    elif(command == "qId"):
        label = input_parsed[1]
        sock.sendto("1,"+str(label)+",0", (UDP_IP, UDP_PORT))
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        print "id - ", data
    elif(command == "qPush"):
        qId = input_parsed[1]
        item= input_parsed[2]
        sock.sendto("3,"+str(qId)+","+str(item), (UDP_IP, UDP_PORT))
    elif(command == "qPop"):
        qId = input_parsed[1]
        sock.sendto("4,"+str(qId)+",0", (UDP_IP, UDP_PORT))
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        print data
    elif(command == "qTop"):
        qId = input_parsed[1]
        sock.sendto("5,"+str(qId)+",0", (UDP_IP, UDP_PORT))
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        print data
    elif(command == "qSize"):
        qId = input_parsed[1]
        sock.sendto("6,"+str(qId)+",0", (UDP_IP, UDP_PORT))
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        print data
    else:
        print "Invalid command"
