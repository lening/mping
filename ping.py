import os,subprocess,threading,sqlite3
from multiprocessing import Pool
from time import sleep

HOSTLIST_PATH='./hostlist'
DB_PATH='./mping.db'
RTTLIST=[]

def mping(host):
	cmd="fping -c 1 -q " +host
	p=subprocess.Popen(cmd,shell=True,stderr=subprocess.PIPE)
	p.wait()
	if p.returncode == 0:
		rtt=p.stderr.read().strip().split('/')[-1]
		return rtt
	else:
		return 1
		
#load_proc需要处理mping返回值
def load_proc(hostlist,rttlist):
	p=Pool(100)
	for host in hostlist:
		p.apply_async(mping, args=(host,rttlist))
	p.close()
	p.join()

def write_data(rttlist):
	conn=sqlite3.connect(DB_PATH)
	cu=conn.cursor()	
	for rtt in rttlist:
		sql="INSERT INTO HOST_LATENCY (HOST,LATENCY) VALUES (\"%s\", \"%s\")" %(rtt[0],rtt[1])
		cu.execute(sql)
		conn.commit()
	conn.close()

def main():
	with open(HOSTLIST_PATH,'r') as hostlist:
		load_proc(hostlist,RTTLIST)
		print(RTTLIST)
		# write_data(rttlist)

if __name__ == '__main__':
	main()
