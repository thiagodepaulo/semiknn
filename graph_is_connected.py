import igraph
import sys

if __name__ == '__main__':
	g = igraph.load(sys.argv[1],format='ncol')
	if g.is_directed():
		g.to_undirected()
	print g.is_connected()
