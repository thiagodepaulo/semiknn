import sys
import numpy as np
#from scipy.linalg import eig
from scipy.sparse import diags
from scipy.sparse.linalg import eigs
from scipy.cluster.vq import kmeans2
from scipy.sparse import lil_matrix

from scipy.sparse.linalg import eigsh
from scipy.sparse import identity

def cluster_points(L, k, n_eig):  
    # sparse eigen is a little bit faster than eig  
    #evals, evcts = eigen(L, k=15, which="SM")  
    #evals, evcts = eig(L,k=15,which="SM")  # calculate eigen-vectors and eigen-values
    print 'calculando autovetores e autovalores'
    #evals, evcts = eigs(L,k=n_eig,which='SR') 
    I = identity(L.shape[0])
    #evals, evcts = eigsh(L, M=I, k=n_eig, sigma=0, which='LM')
    #evals, evcts = eigsh(L, k=n_eig, sigma=0, which='LM', tol=1E-2)  
    evals, evcts = eigsh(L, M=I, k=n_eig, which='SM')  
    print 'heeee!!'
    evals, evcts = evals.real, evcts.real
    # sort eigen-vectors and eigen-values
    edict = dict(zip(evals, evcts.transpose()))
    #evals = sorted(edict.keys())  
    # second and n_eig smallest eigenvalue + vector  
    Y = np.array([edict[i] for i in evals[1:n_eig]]).transpose()  
    # calculate kmeans
    res, idx = kmeans2(Y, k, minit='random')  
    return res, idx

def create_sparse_matrix(arq, dx, dy):
	A=lil_matrix((dx, dy))
	with open(arq,'r') as f:
		for line in f:
			v1,v2,w12=line.split(';')
			A[int(v1), int(v2)] = w12
			A[int(v2), int(v1)] = w12
	return A	


if __name__ == '__main__':

	#with open(sys.argv[1],'r') as f:
	#W = np.loadtxt(f)
	dx = int(sys.argv[2])
	dy = int(sys.argv[3])

	centro_filename = sys.argv[4]
	idx_filename = sys.argv[5]

	print 'criando matrix sparsa'
	W = create_sparse_matrix(sys.argv[1],dx,dy)

	print 'criando diagonal'
	# create Laplacian Matrix
	D = lil_matrix((dy,dy))
	for i in xrange(dy):			
		s=sum(W.getrow(i).data[0])
		D[i,i] = s	

	#D = np.diag([sum(Wi) for Wi in W])
	#L = D - W
	
	print 'criando laplace'
	L = lil_matrix((dx,dy))

	rows,cols = W.nonzero()
	for row,col in zip(rows,cols):
		L[row, col] = D[row, col] - W[row, col]

	#print 'link'
	#for i in xrange(1, dx):
	#	L[0, i] = 1
	#print 'fim link'
	
	print 'criou laplace!!'
#	((row,col), x[row,col])
#	for linha in xrange(dy):
#		for coluna in xrange(dx):
#			L[linha, coluna] = D[linha, coluna] - W[linha, coluna]
	
	k = 2 # number of clusters
	n_eig = 5 # number of smallest eigen-values and eigen-vectors
	
	res, idx = cluster_points(L, k,n_eig)

	print 'salvando arquivos'
	np.savetxt(centro_filename,res)
	np.savetxt(idx_filename,[int(x) for x in idx])

		#154397
		#154401
