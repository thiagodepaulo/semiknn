import os
import sys
import re

from math import sqrt

def sorted_idx(l):
	return sorted(range(len(l)), key=lambda k: l[k])

def dist(p1, p2):
	(x1, y1, r1, g1, b1) = p1
	(x2, y2, r2, g2, b2) = p2
	return sqrt((r1-r2)**2 + (g1 - g2)**2 + (b1 - b2)**2 + (x1-x2)**2 + (y1-y2)**2)


if __name__ == '__main__':

	arq = sys.argv[1]
	arq_neig = os.path.dirname(arq)+"/neig_"+os.path.basename(arq)
	arq_dist = os.path.dirname(arq)+"/dist_"+os.path.basename(arq)
	delimitador='[ ;]'

	l_pxl = []
	with open(arq,'r') as f:
		for line in f:
			v = re.split(delimitador, line)
			l_pxl.append( tuple((float(v[0]), float(v[1]), float(v[2]), float(v[3]), float(v[4]))) )

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

