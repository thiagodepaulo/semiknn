import sys
from optparse import OptionParser
from skimage import io, color

if __name__ == '__main__':

	parser = OptionParser()

	usage = "usage: python %prog [options] args ..."
	description = """Description"""
	parser.add_option("-f", "--file", dest="filename", help="read FILE", metavar="FILE")
	parser.add_option("-o", "--output", dest="outputname", help="write FILE", metavar="FILE")

	(options, args) = parser.parse_args()
	filename = options.filename
	outputname = options.outputname

	if filename is None:
		parser.error("required -f [filename] arg.")

	if outputname is None:
		f = open(filename.split('.')[0]+".lab.dat",'w')
	else:
		f = open(outputname,'w')

	rgb = io.imread(filename)
	print rgb
	exit()
	lab = color.rgb2lab(rgb)
	m = len(lab)
	n = len(lab[0])
	for i in range(0,m):
		for j in range(0,n):
			f.write(str(i)+" "+str(j)+" "+str(lab[i,j][0])+" "+str(lab[i,j][1])+" "+str(lab[i,j][2])+"\n")

	f.close()