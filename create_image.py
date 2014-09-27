import numpy as np
import sys
import Image
import colorsys

def get_N_col(N=5):
	HSV_tuples = [(x*1.0/N, 0.5, 0.5) for x in xrange(N)]
	rgb_l = []
	for rgb in HSV_tuples:
		rgb = map(lambda x: int(x*255),colorsys.hsv_to_rgb(*rgb))        
		rgb_l.append(tuple(rgb))
	return rgb_l

def load_idx(arq):
	with open(arq,'r') as f:
		idx = np.loadtxt(f)
	return idx

if __name__ == '__main__':
	
	idx_img = True

	dx = int(sys.argv[2])
	dy = int(sys.argv[3])

	if idx_img:
		idx = load_idx(sys.argv[1])

		k = len(set(idx))
		d = get_N_col(k)	
	
#	d=dict()
#	for i in xrange(k):
#		d[i] = RGB_tuples[i]

		l = []
		for clus_id in idx:
			l.append(d[int(clus_id-1)])
	else:
		l = []
		with open(sys.argv[1], 'r') as f:
			for line in f:
				v=line.split()
				l.append((int(v[2]), int(v[3]), int(v[4])))
	
	im = Image.new('RGB', (dx, dy))

	im.putdata(l)
	im.save(sys.argv[1]+'_test.png')
	
	
