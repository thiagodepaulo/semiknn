import igraph
import sys

if __name__ == '__main__':
	g = igraph.load(sys.argv[1],format='ncol')
	print len(g.components())
	print g.is_connected()
