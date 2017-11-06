from scapy.all import *
import os

def mping(host):
	cmd="ping -c 1 " + host
	p=os.popen(cmd)
	for line in p:
		#return the latency of ping result
		if line.startswith('rtt'):
			return line.split('/')[-2]
		else:
			pass

print mping('www.baidu.com')