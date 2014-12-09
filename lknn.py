import sys
from linecache import getline
import numpy as np

def read_knn(arq, k, v_idx):
	#print linecache.getline(your_file.txt, randomLineNumber) # Note: first line is 1, not 0
	line = getline(arq, v_idx + 1)
	l_all = line.split()
	l_all = l_all[1:]
	l_knn = []
	for i in xrange(k):
		l_knn.append(int(l_all[i]))
	return l_knn

def dist(arq, v, u):
	return 1
	#return read_dist_file(arq,v)[u]

def read_dist_file(arq, v):
	line = getline(arq, v+1)
	return [float(x) for x in line.split()]

def read_labels(arq):
	s = set()
	with open(arq, 'r') as f:
		for line in f:
			s.add(int(line))
	return s

def create_KnnMutuo(neig_mmap, k, n):
	l = []
	for v in xrange(n):
		l_knnM = []
		l_knn = neig_mmap[v][1:k]  	# read_knn(arq, k, v)
		for nn in l_knn:
			l_nn = neig_mmap[nn][1:k]		 # read_knn(arq,k,nn)
			if v in l_nn:
				l_knnM.append(nn)
		l.append(l_knnM)
	return l

def label_KNN(k, v, label, l_knnM, v_dists, label_dists):
	d = dict()
	for nnM in l_knnM:
		d1 = v_dists[nnM]
		d2 = label_dists[nnM]
		dsum = d1 + d2
		d[dsum] = nnM
	min_dists = sorted(d)

	l = []
	for i in xrange(k):
		if len(min_dists) > i:
			l.append(d[min_dists[i]])

	return l

def load_memmap(filename, nrows, ncolumns):
	return np.memmap(filename, dtype='float32', mode='r', shape=(nrows,ncolumns))

if __name__ == '__main__':

	n = int(sys.argv[1])	# numero de vertices
	k1 = int(sys.argv[2])	# k do knnMutuo
	k2 = int(sys.argv[3])   # k do label Knn

	arq_knn = sys.argv[4]	# arquivo com indice dos knn mais proximos (ordenados por proximidade)
	arq_dist = sys.argv[5]  # arquivo com as distancias (distancias nao ordenada)

	arq_labels = sys.argv[6] 	# arquivo com o indices dos vertices rotulados

	arq_out = sys.argv[7]	# arquivo com os resultados

	set_labels = read_labels(arq_labels)

	dist_mmap = load_memmap(arq_dist, n, n)
	neig_mmap = load_memmap(arq_knn, n, n)

	print 'Associando vertices aos rotulos mais proximos...'
	l_n_label = []
	for v in xrange(n):
		print v
		r_dist = dict()
		min_dist = float("inf")
		min_v_label = 0
		for v_label in set_labels:
			r_dist = dist_mmap[v][v_label]
			if r_dist < min_dist:
				min_dist = r_dist
				min_v_label = v_label

		l_n_label.append(min_v_label)
	print 'OK'

	print 'Criando Knn Mutuo...'
	knnM = create_KnnMutuo(neig_mmap, k1, n)
	print 'OK'

	print 'Calculando Knn Mutuo rotulado'
	l = []
	for v in xrange(n):
		if v%1000 == 0:
			print v
		l_knnM = knnM[v]
		v_label = l_n_label[v]
		l_v_dist = dist_mmap[v] 	# read_dist_file(arq_dist, v)
		l_label_dist = dist_mmap[v_label]			# read_dist_file(arq_dist, v_label)
		l_label_Knn = label_KNN(k2, v, v_label, l_knnM, l_v_dist, l_label_dist)
		l.append(l_label_Knn)
	print 'OK'

	print 'escrevendo saida...'
	with open(arq_out, 'w') as f_out:
		for v in xrange(n):
			for u in l[v]:
				f_out.write(str(v)+','+str(u)+','+str(dist(arq_dist, u, v))+'\n')


