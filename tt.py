from multiprocessing import Process, Pipe


def teste(cnn,v):	
	print 'running... %d' %v
	s = 0
	for i in xrange(1000):
		s += i
	cnn[0].send(s)

l = []
for i in xrange(5):
	parent_conn, child_conn = Pipe()
	l.append(parent_conn)
	p = Process(target=teste, args=((child_conn,),i))
	p.start()
	

for i in xrange(5):
	print l[i].recv()


