#!/usr/bin/env python
import os, socket
import time

lavgs = [ 1, 5, 15 ]

out = ''
now = int(time.time())
FORMAT = "system.%s.%s.%s %s %s\n"
hostprefix = '.'.join(list(reversed(socket.gethostname().split('.'))))

carbon = ('127.0.0.1', 2003)

def appendMetric(group,item,value):
	 return FORMAT % ( hostprefix, group, item, value, now )

# read data
with open('/proc/loadavg','r') as f:
	data = f.read().strip()
items = data.split(' ')
# print loadaverages
for i in range(3):
	out += appendMetric( 'loadAvg', lavgs[i], items[i] )
# print proceses
procRun, procTot = items[3].split('/')
out += appendMetric( 'processes','running', procRun)
out += appendMetric( 'processes','total', procTot)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.sendto(out,carbon)
