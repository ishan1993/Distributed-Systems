#!/usr/bin/python

import socket, struct
import sys
import time
from functools import partial
sys.path.append("../")
from pysyncobj import SyncObj, replicated
import netaddr


class TestObj(SyncObj):

    def __init__(self, selfNodeAddr, otherNodeAddrs):
        super(TestObj, self).__init__(selfNodeAddr, otherNodeAddrs)
        self.__size = 0
        self.label = 0
        self.queue_id 

    @replicated
    def incCounter(self):
        self.__counter += 1
        return self.__counter

    def getCounter(self):
        return self.__counter

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: %s self_port partner1_port partner2_port ...' % sys.argv[0])
        sys.exit(-1)

    UDP_IP = "localhost"



    port = int(sys.argv[1])
    partners = ['localhost:%d' % int(p) for p in sys.argv[2:]]
    o = TestObj('localhost:%d' % port, partners)
    n = 0
    old_value = -1

    while True:
        if o.getCounter() != old_value:
            old_value = o.getCounter()
        if o._getLeader() is None:
            continue

        sock = socket.socket(socket.AF_INET,        # Internet
                                 socket.SOCK_DGRAM)     # UDP

        sock.bind((UDP_IP,(int(sys.argv[1]))))               # Bind the socket

        try:
            data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        except socket.error:
            print ""

        if (data == "INC"):             # Check if it is the request for TIME Sync
            o.incCounter();

        if (data == "GET"):
            sock.sendto(str(o.getCounter()),addr)
