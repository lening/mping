import os,threading,sqlite3
from time import sleep

HOSTLIST_PATH='./hostlist'
DB_PATH='./mping.db'
RTTLIST=[]

def mping(host,rttlist=[]):
	cmd="fping -c 1 -q " + host
	p=os.popen(cmd)
	rtt=p.split('/')[-1]
	rttlist.append((host.strip(),rtt))	


def load_thread(hostlist,rttlist):
	for host in hostlist:
		t=threading.Thread(target=mping,args=(host, rttlist,))
		t.start()
		t.join()
	return rttlist

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
		while(1):
			rttlist=load_thread(hostlist, RTTLIST)
			write_data(rttlist)
			sleep(10)

if __name__ == '__main__':
	main()
