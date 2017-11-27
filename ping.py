#!/usr/bin/python
#_*_coding:utf-8 _*_
import subprocess,time
from multiprocessing import Pool

HOSTLIST_PATH = './hostlist'
LOG_FILE = './mping.log'
DB_PATH = './mping.db'
POOL_SIZE = 500

#调用ping程序获取延时信息
def mping(host):
	cmd=("ping -c 3 -i 0.1 -q " +host).split(" ")
	p = subprocess.Popen(cmd,stdout = subprocess.PIPE,stderr = subprocess.PIPE)
	time.sleep(2)														#停止2秒，等待程序运行
	if p.poll() == 0:
		rtt = p.stdout.readlines()[-1].strip().split('/')[-3]			#获取3次ping结果的平均值
		return(host,rtt)
	else:
		p.kill()
		rtt=99999														#运行2秒后如没有结果则直接Kill进程，返回'time out'
		return(host,rtt)

#多进程并发
def load_proc(hostfile):
	hostlist = []
	for host in hostfile:
		hostlist.append(host.strip('\n'))
	p = Pool(POOL_SIZE)													#一次最多允许并发运行POOL_SIZE个进程，可以根据硬件平台调整值大小
	res = p.map(mping, hostlist)
	p.close()
	p.join()
	return res

#写入数据，目前支持写入到sqlite数据库和log文件
class WriteData(object):
	def __init__(self, rttlist, t):
		self.rttlist = rttlist
		self.t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t)) + " "	#格式化时间字符串

#将数据写入到sqlite数据库
	def to_sqliteDB(self):
		try:
			import sqlite3
		except ImportError:
			print("Error, Import sqlite3 module failed, please check it...")
			exit(1)
		conn = sqlite3.connect(DB_PATH)
		cu = conn.cursor()	
		for rtt in self.rttlist:
			sql = "INSERT INTO HOST_LATENCY (RECORD_TIME,HOST,LATENCY) VALUES (\"%s\", \"%s\", \"%s\")" %(self.t, rtt[0], rtt[1])
			cu.execute(sql)
			conn.commit()
		conn.close()

#将数据写入到log文件
	def to_logfile(self):			
		try:
			with open(LOG_FILE,'a') as logfile:
				for rtt in self.rttlist:				
					msg = self.t + rtt[0] + " " + str(rtt[1]) + '\n'
					logfile.write(msg)
		except IOError:
			print("Error: Open logfile failed, please check it...")
			exit(1)	

def main():
	start_time = time.time()
	try:
		with open(HOSTLIST_PATH,'r') as hostfile:
			rttlist = load_proc(hostfile)
		data = WriteData(rttlist,start_time)
		data.to_logfile()

	except IOError:
		print("Error: Open hostfile failed, please check it...")
		exit(0)
	run_time = '%.2f'%(time.time() - start_time)
	print('Finished in '+ str(run_time) + 's')							#计算程序运行的时间

if __name__ == '__main__':
	main()
