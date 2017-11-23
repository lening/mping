#!/usr/bin/python
#_*_coding:utf-8 _*_
import subprocess,sqlite3,time
from multiprocessing import Pool

HOSTLIST_PATH='./hostlist'
DB_PATH='./mping.db'

#调用ping程序获取延时信息
def mping(host):
	cmd=("ping -c 3 -i 0.1 -q " +host).split(" ")
	p=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	time.sleep(2)														#停止2秒，等待程序运行
	if p.poll() == 0:
		rtt=p.stdout.readlines()[-1].strip().split('/')[-3]
		return(host,rtt)
	else:
		p.kill()														#运行2秒后如没有结果则直接Kill进程
		return(host,'time out')

#多进程并发
def load_proc(hostfile):
	hostlist=[]
	for host in hostfile:
		hostlist.append(host.strip('\n'))
	p=Pool(500)															#一次最多允许同时运行500个进程
	res=p.map(mping, hostlist)
	p.close()
	p.join()
	return res

#将数据写入sqlite数据库
def write_data(rttlist):
	conn=sqlite3.connect(DB_PATH)
	cu=conn.cursor()	
	for rtt in rttlist:
		sql="INSERT INTO HOST_LATENCY (HOST,LATENCY) VALUES (\"%s\", \"%s\")" %(rtt[0],rtt[1])
		cu.execute(sql)
		conn.commit()
	conn.close()

def main():
	stime=time.time()													#记录程序开始时间
	try:
		with open(HOSTLIST_PATH,'r') as hostfile:
			rttlist=load_proc(hostfile)
			write_data(rttlist)
	except IOError:
		print('Error: Open hostfile failed, please check it...')
		exit(0)
	print ('%.2f' %(time.time()-stime))									#计算程序运行时间
if __name__ == '__main__':
	main()
