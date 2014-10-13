import numpy as np
import sys
import Image
import colorsys
from optparse import OptionParser
from skimage.color import rgb2lab, lab2rgb

def get_N_colors(N=5):
	HSV_tuples = [(x*1.0/N, 0.5, 0.5) for x in xrange(N)]
	rgb_l = []
	for rgb in HSV_tuples:
		rgb = map(lambda x: int(x*255),colorsys.hsv_to_rgb(*rgb))
		rgb_l.append(tuple(rgb))
	return rgb_l

def get_N_gray_scale(N=5):
	v = 255/N
	d = dict()
	for i in range(0,N):
		d[i] = (v*i,v*i,v*i)
	return d

if __name__ == '__main__':

	parser = OptionParser()
	usage = "usage: python %prog [options] args ..."
	description = """Description"""
	parser.add_option("-f", "--file", dest="filename", help="read FILE", metavar="FILE")
	parser.add_option("-m", "--mode", dest="mode", default="build", help="interaction mode: build, rebuild [default: build]", metavar="MODE")
	parser.add_option("-x", "--dimension-x-axis", dest="dx", help="dimension of x-axis")
	parser.add_option("-y", "--dimension-y-axis", dest="dy", help="dimension of y-axis")

	(options, args) = parser.parse_args()
	filename = options.filename
	dx = int(options.dx)
	dy = int(options.dy)
	mode = options.mode

	if filename == "None":
		parser.error("required -f [filename] arg.")

	if mode == "build":

		if dx == "None" or dy == "None":
			parser.error("required -x [x-axis] and -y [yaxis] args.")

		with open(filename,'r') as f:
			set_cluster_id = np.loadtxt(f)

		k = len(set(set_cluster_id))
		d = get_N_gray_scale(k)

		l = []
		for cluster_id in set_cluster_id:
			l.append(d[int(cluster_id-1)])

	elif mode == "rebuild":
		l = []
		with open(filename, 'r') as f:
			for line in f:
				v = line.split()
				print v[2]
				print v[3]
				print v[4]
				l.append((int(v[2]), int(v[3]), int(v[4])))

	else:
		parser.error("incorrect -m [mode] arg.")

	im = Image.new('RGB', (dx, dy))
	im.putdata(l)
	im.save(filename.split('.')[0] + '.png')