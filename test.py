import os,threading,sqlite3,subprocess
from time import sleep

cmd="fping -c 1 -q 172.20.1.10"
p=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
p.wait()
print p.returncode
print p.stderr.read()
# rtt=p.split('/')[-1]
# rttlist.append((host.strip(),rtt))	
