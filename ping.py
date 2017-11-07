import os
import threading
import sqlite3

hostPath='./hostlist'
databasePath='./mping.db'
L=threading.Lock()

conn=sqlite3.connect(databasePath)
cu=conn.cursor()

#get network latency
rttlist=[]
def mping(host):
	cmd="ping -c 1 " + host
	p=os.popen(cmd)
	for line in p:
		#return the latency of ping result
		if line.startswith('rtt'):
			rtt=line.split('/')[-2]
			rttlist.append((host.strip(),rtt))		
		else:
			pass

# class ControlData:
# 	def __init__(self,):
# 		pass
# 	def connect_database():
# 		pass
# 	def write_data():
# 		pass

hostlist=open(hostPath,'r')
threads=[]
for host in hostlist:
	t=threading.Thread(target=mping,args=(host,))
	threads.append(t)
	t.start()

for t in threads:
	t.join()
hostlist.close()

for rtt in rttlist:
	sql="INSERT INTO HOST_LATENCY (HOST,LATENCY) VALUES (\"%s\", \"%s\")" %(rtt[0],rtt[1])
	cu.execute(sql)
	conn.commit()
conn.close()

# print mping('www.baidu.com')