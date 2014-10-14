import Image
import sys
from optparse import OptionParser

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
		f = open(filename.split('.')[0]+".rgb.dat",'w')
	else:
		f = open(outputname,'w')

	im = Image.open(filename)
	pix = im.load()
	for j in range(0,im.size[1]):
		for i in range(0,im.size[0]):
			f.write(str(i)+" "+str(j)+" "+str(pix[i,j][0])+" "+str(pix[i,j][1])+" "+str(pix[i,j][2])+"\n")

	f.close()