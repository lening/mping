#!/usr/bin/python
#_*_coding:utf-8 _*_
import subprocess,sqlite3,time
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
		p.kill()														#运行2秒后如没有结果则直接Kill进程，返回'time out'
		return(host,"time out")

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

#将数据写入sqlite数据库
def write_data(rttlist):
	conn = sqlite3.connect(DB_PATH)
	cu = conn.cursor()	
	for rtt in rttlist:
		sql = "INSERT INTO HOST_LATENCY (HOST,LATENCY) VALUES (\"%s\", \"%s\")" %(rtt[0],rtt[1])
		cu.execute(sql)
		conn.commit()
	conn.close()

#将数据写入log文件
def write_log(rttlist,t):
	t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t)) + " "		#格式化时间字符串
	try:
		with open(LOG_FILE,'a') as logfile:
			for rtt in rttlist:				
				msg = t + rtt[0] + " " + rtt[1] + '\n'
				logfile.write(msg)
	except IOError:
		print('Error: Open logfile failed, please check it...')
		exit(0)

def main():
	start_time = time.time()											#记录程序开始时间
	try:
		with open(HOSTLIST_PATH,'r') as hostfile:
			rttlist = load_proc(hostfile)
			write_log(rttlist,start_time)
	except IOError:
		print('Error: Open hostfile failed, please check it...')
		exit(0)
	end_time = '%.2f'%(time.time() - start_time)
	print('Finished in '+ str(end_time) + 's')							#计算程序运行的时间

if __name__ == '__main__':
	main()
