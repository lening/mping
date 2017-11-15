import os,subprocess,threading,sqlite3,time
from multiprocessing import Pool

HOSTLIST_PATH='./hostlist'
DB_PATH='./mping.db'

def mping(host):
	cmd=("ping -c 3 -i 0.1 -q " +host).split(" ")
	p=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	time.sleep(2)
	if p.poll() == 0:
		rtt=p.stdout.readlines()[-1].strip().split('/')[-3]
		return(host,rtt)
	else:
		p.kill()
		return(host,'time out')

def load_proc(hostfile):
	hostlist=[]
	for host in hostfile:
		hostlist.append(host.strip('\n'))
	p=Pool(500)	
	res=p.map(mping, hostlist)
	p.close()
	p.join()
	return res

def write_data(rttlist):
	conn=sqlite3.connect(DB_PATH)
	cu=conn.cursor()	
	for rtt in rttlist:
		sql="INSERT INTO HOST_LATENCY (HOST,LATENCY) VALUES (\"%s\", \"%s\")" %(rtt[0],rtt[1])
		cu.execute(sql)
		conn.commit()
	conn.close()

def main():

	with open(HOSTLIST_PATH,'r') as hostfile:
		rttlist=load_proc(hostfile)
		write_data(rttlist)

if __name__ == '__main__':
	main()
