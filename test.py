import os,subprocess,threading,sqlite3
from multiprocessing import Pool
from time import sleep

def pf(i):
	print('test%d'%(i))

def load_proc():
	p=Pool(4)
	for i in range(19):
		p.apply_async(pf, args=(i,))
	p.close()
	p.join()

def main():
	load_proc()

if __name__ == '__main__':
	main()
	
