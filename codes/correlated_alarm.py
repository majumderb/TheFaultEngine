from fault_engine import *
from community import *

# Inherits fault engine module
class correlated_alarms(fault_engine):
	def __doc__():
		print 'This is the class correlated alarms. This inherits class fault engine.'

	def __init__(self,object1,filename):
		print "creating the dependency graph."
		# Creating the dependency graph based on the nodes reachable in fault engine graph. weight(i,j) is the bayes probability(j,i)
		with open(filename,'w') as ff:
			for i in object1.graph:
				x = object1.graph.nodes().index(i)
				for j in object1.graph:
					y = object1.graph.nodes().index(j)
					try:
						n = object1.bayes_probability(j,i)
						if object1.is_reachable(i,j) and n > 0:
							if i != j:
								ff.write(str(x))
								ff.write(',')
								ff.write(str(y))
								ff.write(',')
								ff.write(str(n))
								ff.write('\n')
					except ZeroDivisionError:
						continue
		print "graph loaded. calculating girvan newman community."
		# Get the communities among the nodes
		self.comps = girvan_main(filename)
		s = sorted(self.comps, key=len, reverse=True)
		s = [list(i) for i in s]
		s = [[object1.graph.nodes()[i] for i in j] for j in s]
		self.comps = s
