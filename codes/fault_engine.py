# First import all the necessary packages
try:
	import networkx
	import matplotlib.pyplot as plt
	import pandas
	import numpy
	import uuid
	import seaborn
	import sys
	import numpy as np
	import networkx as nx
	import csv
	import math
	import random as rand
except ImportError:
	print "install the following python packages - pandas, matplotlib and networkx"


class fault_engine():
	def __doc__():
		print 'This is the class fault engine'
	
	def __init__(self,filename=None,faulty_nodes = None,alarming_nodes = None):
		G = networkx.DiGraph()	
		# input the graph file. format u,v 
		graphdata = open(filename)
		for line in graphdata:
      			l = line.split()
			G.add_edge(l[0],l[1])	
		self.graph = G
		self.faulty_nodes = []
		self.alarming_nodes = []
		self.all_failures = []
		self.count_of_failure = []
		self.fault_detected_nodes = []
		self.faulted_devices = []
		self.size_code = {}
		# Topological sort on the graph
		sorted_nodes = networkx.topological_sort(self.graph)
		self.sorted_nodes = sorted_nodes
		dict1 = {i:sorted_nodes.index(i) for i in sorted_nodes}
		self.dict = dict1
		self.probability_dict = {}
		# Checking all pair reachability
		self.all_pair_connections = networkx.all_pairs_dijkstra_path_length(self.graph)
		# Getting size code based on topological ordering		
		for node in self.graph:
			if node in self.faulty_nodes:
				self.size_code[node] = 6000*1.0/(self.sorted_nodes.index(node)+1)
			else:
				self.size_code[node] = 6000*1.0/(self.sorted_nodes.index(node)+1)
		
	def fault_data(self,faulty_nodes,alarming_nodes):
		self.faulty_nodes = faulty_nodes
		self.alarming_nodes = alarming_nodes
	# Getting the fault log file and counting the number of failures for all the nodes
	def fault_log(self, filename=None):
		logfile = pandas.read_csv(filename)
		logfile['count'] = 1
		count_of_failure = logfile.groupby(['root_cause','timestamp'])['count'].agg(['sum'])
		count_of_failure.reset_index(inplace=True)
		all_failures = count_of_failure['root_cause']
		count_of_failure['count'] = 1
		count_of_failure = count_of_failure.groupby(['root_cause'])['count'].agg(['sum'])
		count_of_failure.reset_index(inplace=True)
		self.count_of_failure = count_of_failure
		self.all_failures = all_failures
		self.faulted_devices = list(set(self.all_failures))

	# Histogram plot of all the failures
	def print_log(self):
		seaborn.countplot(list(self.all_failures))
		plt.title('Histogram of failures of the devices')
		plt.xlabel('Device id')
		plt.ylabel('Frequency of failures')
		plt.show()
		plt.close()
	
	# Historical probability of failure of a node based on the historical log file
	def probability_of_failure(self,x):
		if x in self.faulted_devices:
			return float(self.count_of_failure[self.count_of_failure['root_cause'] == x]['sum'])*1.0/len(self.count_of_failure)
		else:
			return 0

	# Checking whether a node is reachable from another
	def is_reachable(self,target,source):
		if target in self.all_pair_connections[source].keys():
			return 1
		else:
			return 0

	# Defining the bayes probability = probability of (failure of device A|device C sends an alarm)
	def bayes_probability(self,faulty_device,alarming_device):
		count = 0
		for source in self.graph:
			count += self.is_reachable(alarming_device,source)*self.probability_of_failure(source)
		return self.is_reachable(alarming_device,faulty_device)*self.probability_of_failure(faulty_device)*1.0/count

	# Root Cause Probability of a faulty node based on the other alarming nodes. The value is average of all the bayes probability values
	def root_cause_probability(self):
		for i in self.faulty_nodes:
			temp = []
			for j in self.alarming_nodes:
				temp.append(self.bayes_probability(i,j))
			temp = [xx for xx in temp if xx != 0]
			if len(temp) != 0:	
				self.probability_dict[i] = numpy.array(temp).mean()
			else:
				self.probability_dict[i] = 0
			self.fault_detected_nodes.append((i,self.probability_dict[i],self.size_code[i]))

