import Image
import math
from optparse import OptionParser
import igraph

def euclidian_distance(x1,y1,r1,g1,b1,x2,y2,r2,g2,b2):
    return math.sqrt(
    	(x1 - x2) ** 2 +
    	(y1 - y2) ** 2 +
    	(r1 - r2) ** 2 +
    	(g1 - g2) ** 2 +
    	(b1 - b2) ** 2
    )

def _plot_xy(g):
	visual_style = {}
	visual_style["vertex_shape"] = "circle"
	visual_style["label_color"] = "white"
	visual_style["edge_color"] = "black"
	visual_style["edge_width"] = 0.2
	visual_style["vertex_size"] = 0.5

	layout = []
	for vertex in g.vs():
		layout.append((vertex["x"],vertex["y"]))

	visual_style["layout"] = layout
	visual_style["bbox"] = (200, 200)
	visual_style["margin"] = 10
	igraph.plot(g, **visual_style)

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

	g = igraph.Graph()
	im = Image.open(filename)
	pix = im.load()
	for j in range(0,im.size[1]):
		for i in range(0,im.size[0]):
			g.add_vertex()
			vertex = g.vs[g.vcount()-1]
			vertex["name"] = vertex.index
			vertex["x"] = i
			vertex["y"] = j
			vertex["r"] = pix[i,j][0]
			vertex["g"] = pix[i,j][1]
			vertex["b"] = pix[i,j][2]

	for v in g.vs():
		set_distance = dict()
		for n in g.vs():
			distance = euclidian_distance(v["x"],v["y"],v["r"],v["g"],v["b"],n["x"],n["y"],n["r"],n["g"],n["b"])
			set_distance[n.index] = distance
		sorted_set_distance = sorted(set_distance.items(), key=lambda set_distance: set_distance[1])
		v["distance"] = sorted_set_distance[:k]

	edges = []
	weight = []
	for v in g.vs():
		for n in v["distance"]:
			edges += [(v.index, n[0])]
			weight.append(n[1])

	g.add_edges(edges)
	g.es["weight"] = weight

	_plot_xy(g)

	g.write(filename.split('.')[0]+".edgelist", format='ncol')