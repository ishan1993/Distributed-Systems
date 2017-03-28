#!/usr/bin/python

import socket, struct
import sys
import time
from functools import partial
sys.path.append("../")
from pysyncobj import SyncObj, replicated


class QueObj(SyncObj):
    q_count = 0

    def __init__(self, selfNodeAddr, otherNodeAddrs):
        super(QueObj, self).__init__(selfNodeAddr, otherNodeAddrs)
        self.size = []
        self.label = []
        self.id = []
        self.data = []

    @replicated
    def create(self,label):
        self.label.append(label)
        self.id.append(QueObj.q_count)
        self.size.append(-1)
        QueObj.q_count = QueObj.q_count+1
        self.data.append([])

    @replicated
    def pop(self,q_id):
        item = self.data[q_id][self.size[q_id]]
        self.data[q_id].remove(item)
        self.size[q_id] = self.size[q_id] - 1

    @replicated
    def push(self,q_id,item):
        self.size[q_id] = self.size[q_id] + 1
        self.data[q_id].append(item)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: %s self_port partner1_port partner2_port ...' % sys.argv[0])
        sys.exit(-1)

    UDP_IP = "localhost"


    port = int(sys.argv[1])
    partners = ['localhost:%d' % int(p) for p in sys.argv[2:]]
    sock = socket.socket(socket.AF_INET,        # Internet
                             socket.SOCK_DGRAM)     # UDP
    sock.setblocking(False)

    sock.bind((UDP_IP,(int(sys.argv[1]))))               # Bind the socket


    o=QueObj('localhost:%d' % port, partners)


    while True:
        if o._getLeader() is None:
            continue

        data = "0,0,0"

        try:
            data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        except:
            pass

        data_parsed = data.split(',')
        command = int(data_parsed[0])
        param1 = int(data_parsed[1])
        param2 = int(data_parsed[2])
        if (command == 1):             # Check if it is the request for TIME Sync
            o.create(param1)
            sock.sendto(str(QueObj.q_count),addr)
            time.sleep(2)

        if (command == 2):
            sock.sendto(str(o.label.index(param1)),addr)

        if (command == 3):
            print "push ",param1,param2
            o.push(param1,param2)
            time.sleep(1)

        if (command == 4):
            print "pop ",param1
            sock.sendto(str(o.data[param1][o.size[param1]]),addr)
            o.pop(param1)
            time.sleep(1)

        if (command == 5):
            print "top ",param1
            sock.sendto(str(o.data[param1][0]),addr)

        if (command == 6):
            print "size ",param1
            sock.sendto(str(o.size[param1] + 1),addr)

        if (command == 7):
            print "ping"
            sock.sendto("ping",addr)
