#!/usr/bin/env python
"""
Script is aimed to get cpuUsage times since boot and form
corresponding metrics for graphite to send it over netcat
"""

import os, socket
import time

interval=5
hz=os.sysconf(os.sysconf_names['SC_CLK_TCK'])
now = int(time.time())
times = ['','user','nice','system','idle','iowait','irq','softirq','steal','guest','guest_nice']
hostprefix = '.'.join(list(reversed(socket.gethostname().split('.'))))
FORMAT = "system.%s.%s.%s %s %s\n"

def appendMetric(group,item,value,time):
	 return FORMAT % ( hostprefix, group, item, value, time )

def sendMetric(data):
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.sendto(out,carbon)	

def get_uptime():
	with open('/proc/uptime','r') as f:
		uptime_str = f.read().split()[0] 
	return float(uptime_str)

def get_times():
	uptime = get_uptime()
	ret={}
	with open('/proc/stat','r') as f:
		lines = f.readlines()
	stat = lines[0].split()
	for i in range(1,len(times)):
		ret[times[i]] = round(int(stat[i])/hz/uptime*100,2)
	return ret

def form_metric(stats):
	now = int(time.time())
	ret = ""
	for k in stats.keys():
		ret += appendMetric('cpuTime', k, stats[k], now)
	return ret

print form_metric(get_times())
