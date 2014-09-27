import sys
from scipy.sparse import lil_matrix

def create_sparse_matrix(arq, dx, dy):
	A=lil_matrix((dx, dy))
	with open(arq,'r') as f:
		for line in f:
			v1,v2,w12=line.split(';')
			A[int(v1),int(v2)] = w12
	return A	

def connected_components(A):

	result = []
	nodes=set(range(A.shape[0]))	

	print len(nodes)

	while nodes:		
		n = nodes.pop()
		group = {n}
		queue = [n]
		
		print len(nodes)

		while queue:
			n=queue.pop(0)
			neighbors = set(A.getrow(n).rows[0])
			neighbors = neighbors - group
			nodes = nodes - neighbors
			group = group | neighbors
			queue.extend(neighbors)
		result.append(group)				

	return result

if __name__ == '__main__':
	dx = int(sys.argv[2])
	dy = int(sys.argv[3])

	print 'criando matrix sparsa'
	W = create_sparse_matrix(sys.argv[1],dx,dy)
	print 'calculando componente conexos'
	print len(connected_components(W))
