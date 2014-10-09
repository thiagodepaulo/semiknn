import Image
import math
from optparse import OptionParser
import igraph
from scipy import spatial
import numpy as np

def _plot_xy(graph):
	visual_style = {}
	visual_style["vertex_shape"] = "circle"
	visual_style["label_color"] = "white"
	visual_style["edge_color"] = "black"
	visual_style["edge_width"] = 0.1
	visual_style["vertex_size"] = 0.3

	layout = []
	for vertex in graph.vs():
		layout.append((vertex["x"],vertex["y"]))

	visual_style["layout"] = layout
	visual_style["bbox"] = (800, 800)
	visual_style["margin"] = 10
	igraph.plot(graph, **visual_style)

if __name__ == '__main__':

	parser = OptionParser()

	usage = "usage: python %prog [options] args ..."
	description = """Description"""
	parser.add_option("-f", "--file", dest="filename", help="read FILE", metavar="FILE")
	parser.add_option("-k", "--knn", dest="k", help="knn")

	(options, args) = parser.parse_args()
	filename = options.filename
	k = int(options.k)

	if filename is None:
		parser.error("required -f [filename] arg.")

	graph = igraph.Graph()
	im = Image.open(filename)
	pix = im.load()
	x, y, r, g, b = [], [], [], [], []
	for j in range(0,im.size[1]):
		for i in range(0,im.size[0]):
			graph.add_vertex()
			vertex = graph.vs[graph.vcount()-1]
			vertex["name"] = vertex.index
			vertex["x"] = i
			vertex["y"] = j
			vertex["r"] = pix[i,j][0]
			vertex["g"] = pix[i,j][1]
			vertex["b"] = pix[i,j][2]
			x.append(i)
			y.append(j)
			r.append(pix[i,j][0])
			g.append(pix[i,j][1])
			b.append(pix[i,j][2])

	x = np.array(x)
	y = np.array(y)
	r = np.array(r)
	g = np.array(g)
	b = np.array(b)
	tree = spatial.KDTree(zip(x.ravel(), y.ravel(), r.ravel(), g.ravel(), b.ravel()))

	edges = []
	weight = []
	for v in graph.vs():
		pts = np.array([[v["x"], v["y"], v["r"], v["g"], v["b"]]])
		list_nn = tree.query(pts, k=k);
		for idx, nn in enumerate(list_nn[1][0]):
			edges += [(v.index, nn)]
			weight.append(1/(1+list_nn[0][0][idx]))

	graph.add_edges(edges)
	graph.es["weight"] = weight

	_plot_xy(graph)

	graph.write(filename.split('.')[0]+".edgelist", format='ncol')