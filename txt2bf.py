#!/usr/bin/python2

# Usage:
# txt2bf.py input_file output_file
# 
# txt2bf.py some\ random\ string output_file
#
# txt2bf.py input_file          // output goes to stdout
#
# txt2bf.py input_file --no-nl  // without newlines - everything is in single line

from sys import argv
from os import path

b = lambda i: i*"<"               # back
n = lambda i: i*">"               # next
p = lambda i: i*"+"               # plus
m = lambda i: i*"-"               # minus
c = lambda i: "[{0}]".format(i)   # cycle
r = lambda i: int(round(i/10.,0)) # round

def move(i):
	if i<0: return b(abs(i))
	return n(i)
def get_ascii(data):
	symbols = list(data)
	ascii = []
	for i in symbols: ascii.append(ord(i))
	return ascii

def get_bases(ascii):
	last  =  0
	bases = []
	for i in ascii:
		if((last+10)<i):bases.append(i) # var limit = 10
		last = i
	return bases

def get_closest(integer,array):
	closest = array[0]
	for i in array:
		if abs(integer-i)<abs(integer-closest):closest=i
	return closest

def format_bf(data):
	u_ascii = get_ascii(data) # unsorted_ascii
	ascii   = []
	for i in u_ascii:ascii.append(i)
	ascii.sort()
	bases   = get_bases(ascii)
	index   = [0]
	cur_i   = 0
	
	init  = ""
	for i in bases:	
		tmp   = r(i)
		index.append(tmp*10)
		init +=">"+p(tmp)
	init += b(len(index)-1)+"-"
	
	bf = p(10)+c(init)
	
	for i in u_ascii:
		close = get_closest(i,index)
		close_id = index.index(close)
		if close_id!=cur_i:
			bf   += move(close_id-cur_i)
			cur_i = close_id
		if close!=i:
			tmp   = i-index[close_id]
			if tmp<0: bf+=m(abs(tmp))
			else:     bf+=p(tmp)
			index[close_id] += tmp
		bf+=".\n"
	return bf

if __name__=="__main__":
	if(path.exists(argv[1])): data = open(argv[1],"rb").read()
	else: data=argv[1]
	
	bf = format_bf(data)

	if "--no-nl" in argv:
		del(argv[argv.index("--no-nl")])
		bf = bf.replace("\n","")
	
	try:   open(argv[2],"w").write(bf)
	except:print(bf)
