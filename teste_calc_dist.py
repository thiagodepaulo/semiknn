
from math import sqrt
import sys
import re

def sorted_idx(l):
	return sorted(range(len(l)), key=lambda k: l[k])
	
def dist(p1, p2):
	(x1, y1) = p1
	(x2, y2) = p2
	return sqrt((x1-x2)**2 + (y1-y2)**2)
	
	
if __name__ == '__main__':
	
	arq = sys.argv[1]
	arq_neig = 'neig_'+arq	
	arq_dist = 'dist_'+arq
	delimitador='[ ;,]'
	
	l_pxl = []
	with open(arq,'r') as f:
		for line in f:
			v = re.split(delimitador, line)
			l_pxl.append( tuple((float(v[0]),float(v[1]))))
	
	n = len(l_pxl)
	
	f_neig = open(arq_neig,'w')
	f_dist = open(arq_dist,'w')
	for i in xrange(n):
		print i,n
		l_dist = []
		for j in xrange(n):
			d = dist(l_pxl[i], l_pxl[j])
			l_dist.append(d)

		f_neig.write(' '.join(str(x) for x in sorted_idx(l_dist))+'\n')
		f_dist.write(' '.join(str(x) for x in l_dist) + '\n')
									
