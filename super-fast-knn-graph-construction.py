import Image
import math
from optparse import OptionParser
import igraph
from scipy import spatial
import numpy as np
from math import sqrt
import threading
from Queue import Queue
from multiprocessing import Process, Pipe
import os
import random
import time

def read_labels(arq):
	l = []
	d = dict()
	with open(arq, 'r') as f:
		for line in f:
			aux = line.split()
			vertex = int(aux[0])
			label = int(aux[1])
			l.append(vertex)
			d[vertex] = label
	return (l,d)

mylock = threading.RLock()

def aux_calc(vertex_set, graph, labeled, tree, sender):
	# atribui para os rotulados mais proximos
	buff = dict()	
	dic_nn = dict()
	far_nn = dict()
	for v in vertex_set:
		if v.index % 10000 == 0: 
			print v.index
		min_d = float('inf')
		min_l = -1
		v_pts = [v["x"], v["y"], v["r"], v["g"], v["b"]]
		for u_idx in labeled:
			u = graph.vs()[u_idx]
			d = ((v_pts[0] - u["x"])**2 + (v_pts[1] - u["y"])**2 + (v_pts[2] - u["r"])**2 + (v_pts[3] - u["g"])**2 + (v_pts[4] - u["b"])**2)
			if d < min_d:
				min_d = d
				min_l = u_idx
		buff[v.index] = (min_l, min_d)

		# atribui lista de k vizinhos mais proximos
		dic_nn[v.index] = tree.query(np.array([v_pts]), k=(k+1))
		far_nn[v.index] = dic_nn[v.index][0][0][-1]	# farthest kth neighbor
	
	sender.send((buff, dic_nn, far_nn))


def cal_NN(vertex_set, tree, k1, k2, buff, sender, dic_nn, far_nn):

	print k2
	l = []	
	for v in vertex_set:		
		if v.index % 10000 == 0:
			print v.index

		l_dists = []
		l_ew = []
		list_v_nn = dic_nn[v.index] # tree.query(np.array([[v["x"], v["y"], v["r"], v["g"], v["b"]]]), k=(k1+1));
		pts_v = (v["x"], v["y"], v["r"], v["g"], v["b"])
		# for each KNN vertex
		for i, nn in enumerate(list_v_nn[1][0]):
			if nn == v.index:
				continue
			u = graph.vs()[nn]
			pts_u = (u["x"], u["y"], u["r"], u["g"], u["b"])
			list_u_nn = dic_nn[nn] #tree.query(np.array([[u["x"], u["y"], u["r"], u["g"], u["b"]]]), k=(k1+1))
			# if it is mutual
			if spatial.distance.euclidean(pts_v, pts_u) <= far_nn[u.index]:
				d1 = list_v_nn[0][0][i]
				(lidx,d2) = buff[u.index] 		# near_labeled(v, pts, labeled, labeled_pts, buff)
				l_dists.append(d1 + d2)
				# tuple (edge, weight)
				l_ew.append(((v.index, nn), 1/(1+d1)))
		
		count = 0
		for idx in np.argsort(l_dists):
			if count < k2:
				# put(edge, weight)  (l_ew[idx][0], l_ew[idx][1])				
				l.append(l_ew[idx])
			else:	
				break
			count+=1
	print 'sending %d' %len(l)	
	sender.send(l)
					

if __name__ == '__main__':

	parser = OptionParser()

	usage = "usage: python %prog [options] args ..."
	description = """Description"""
	parser.add_option("-f", "--file", dest="filename", help="read FILE", metavar="FILE")
	parser.add_option("-1", "--knn", dest="k", help="knn")
	parser.add_option("-2", "--semiknn", dest="semik", help="semiknn")
	parser.add_option("-l", "--labels", dest="labels", help="labels FILE")
	parser.add_option("-t", "--nthreads", dest="nthreads", help="number of threads", default=4)
	parser.add_option("-o", "--out", dest="out_filename", help="write FILE", metavar="OUTFILE")
	parser.add_option("-c", "--ncluster", dest="nclusters", help="number of clusters", metavar="nclusters")

	(options, args) = parser.parse_args()
	filename = options.filename
	k = int(options.k)
	k2 = int(options.semik)
	labels_filename = options.labels
	out_filename = options.out_filename
	n_threads = int(options.nthreads)
	c = int(options.nclusters)

	if filename is None:
		parser.error("required -f [filename] arg.")
	if labels_filename is None:
		parser.error("required -l [labels file] arg.")

	print k, k2

	graph = igraph.Graph()	
	graph.to_undirected()	
	im = Image.open(filename)
	pix = im.load()
	x, y, r, g, b = [], [], [], [], []

	t0 = time.time()
	
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

	# print "criou grafo"

	x = np.array(x)
	y = np.array(y)
	r = np.array(r)
	g = np.array(g)
	b = np.array(b)
	tree = spatial.KDTree(zip(x.ravel(), y.ravel(), r.ravel(), g.ravel(), b.ravel()))
	# print "criou kdtree"

	# labeled set
	labeled, map_labels = read_labels(labels_filename)
		
	# atribui para os rotulados mais proximos
	# print "procurando rotulados mais proximos"
	
	part = len(graph.vs())/n_threads	

	# ******************************************
	lq = []
	l_threads = []
	for i in xrange(0, len(graph.vs()), part ):
		sender, receiver = Pipe()
		p = Process(target=aux_calc, args=(graph.vs()[i:i+part], graph, labeled, tree, sender))
		p.daemon = True
		p.start()
		lq.append(receiver)
		l_threads.append(p)

	buff = dict()	
	dic_nn = dict()	
	far_nn = dict()
	for receiver in lq:
		(buff_p, dic_nn_p, far_nn_p) = receiver.recv()
		buff.update(buff_p)
		dic_nn.update(dic_nn_p)		
		far_nn.update(far_nn_p)
	# ******************************************

	lq = []
	l_threads = []
	for i in xrange(0, len(graph.vs()), part ):
		sender, receiver = Pipe()
		p = Process(target=cal_NN, args=(graph.vs()[i:i+part], tree, k, k2, buff, sender, dic_nn, far_nn))
		p.daemon = True
		p.start()
		l_threads.append(p)
		lq.append(receiver)
	
	edges = []
	weights = []
	for receiver in lq:
		# print 'calling receiver'
		l_ew = receiver.recv()
		# print 'retornou'
		for edge, weight in l_ew:
			edges += [edge]
			weights.append(weight)

	# write time
	t1 = time.time()
	with open('time','a') as f:
		f.write('%f\t%f\t%f\tgct\n' %(k, k2, (t1 - t0)))	

	print len(edges), len(weights)
	print out_filename

	graph.add_edges(edges)
	graph.es["weight"] = weights

	# _plot_xy(graph)

	graph.simplify(combine_edges='first')	
	# print 'escrevendo...' 		
	# graph.write(out_filename, format='ncol')

	#menbership = graph.community_leading_eigenvector(clusters=c,weights="weight")
	#menbership = graph.community_infomap(edge_weights="weight")

	fixed_l = [False]*len(graph.vs())
	init_l = [random.choice(list(set(map_labels.values()))) for x in range(len(graph.vs()))]
	for l in labeled:
		init_l[l] = map_labels[l]
		fixed_l[l] = True


#	cl = graph.community_fastgreedy()
#	membership = cl.as_clustering(2).membership

	t0 = time.time()
	menbership = graph.community_label_propagation(weights="weight", initial=init_l,fixed=fixed_l)
	# write time
	t1 = time.time()
	with open('time','a') as f:
		f.write('%f\t%f\t%f\tlpt\n' %(k, k2, (t1 - t0)))				

	ass = dict()	
	for cluster_id in xrange(len(menbership)):
		for v in menbership[cluster_id]:
			ass[v] = cluster_id

	print 'escrevendo cluster to %s' %out_filename
	with open(out_filename,'w') as f:
		for v in xrange(len(ass)):
			f.write(str(ass[v]+1)+'\n')

#	f = open(out_filename, 'w')
#	for edge in graph.es():
#		v1,v2,weight = edge.tuple[0], edge.tuple[1], edge["weight"]
#		f.write("%d\t%d\t%.3f\n"  %(v1, v2, weight))
#	f.close()
	print 'fim'	

