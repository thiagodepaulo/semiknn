
import sys
import igraph

def _plot_xy(g):
	visual_style = {}
	visual_style["vertex_shape"] = "circle"
	visual_style["label_color"] = "white"
	visual_style["edge_color"] = "black"
	visual_style["edge_width"] = 0.0
	visual_style["vertex_size"] = 0.001

	layout = []
	for vertex in g.vs():
		layout.append((vertex["x"],vertex["y"]))

	visual_style["layout"] = layout
	visual_style["bbox"] = (800, 1200)
	visual_style["margin"] = 10
	igraph.plot(g, **visual_style)



g = igraph.load(sys.argv[1],format='ncol')
xyrgb_arq=sys.argv[2]

with open(xyrgb_arq,'r') as f:	
	for i, line in enumerate(f):
		x,y=line.split()[:2]		
		x=int(x)
		y=int(y)
		g.vs[i]['x'] = x
		g.vs[i]['y'] = y

_plot_xy(g)


	

