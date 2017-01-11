from fault_engine import *
from markov import *
from correlated_alarm import *

# The main function
if __name__ == '__main__':
	print "main functions: "
	print "1. Root Cause Analysis"
	print "2. Correlated Device Identification"
	print "3. Markov Probability Calculation"
	print "Enter choice: "
	choice = input()
	if choice == 1:
		# First load the dependency graph edge relations
		filename = raw_input('Graph filename: ')
		#Initialize the object
		object1 = fault_engine(filename)
		# Now taking the input of alarming and unresponsive devices' ids
		try:
			faulty_devices = raw_input('Enter the unresponsive and faulty devices: ')
			faulty_devices = faulty_devices.split()
			alarming_devices = raw_input('Enter the alarming devices: ')
			alarming_devices = alarming_devices.split()
			object1.fault_data(faulty_devices, alarming_devices)
			# Getting the past failure log file data and plotting the histogram
			object1.fault_log(filename=raw_input('Fault filename: '))
			object1.print_log()
			# Computing the root cause analysis algorithm
			object1.root_cause_probability()
			# Printing the final result with the probable root cause devices
			print "The probable faulted devices with probability of failure and priority in the network are -"
			for i in object1.fault_detected_nodes:
				print i	
		except KeyError:
			print "Please check your input. Devices might not be in the graph."
	if choice == 2:	
		# For correlated alarms
		# First load the dependency graph edge relations
		filename = raw_input('Graph filename: ')	
		#Initialize the object
		object1 = fault_engine(filename)
		object1.fault_log(filename=raw_input('Fault filename: '))
		filename = raw_input('Filename for storing the community graph: ')
		# Initializing the correlated alarm module object.
		object2 = correlated_alarms(object1,filename)
		# Print the correlated components
		print "\n \n The correlated components are "
		print object2.comps 
	if choice == 3:
		# Markov transient model
		object3 = markov_state(input_filename=raw_input('Enter the markov failure log file: '))
		d = input('Enter the time period for markov failure model: ')
		print 'The probability of going to persistent state is ' + str(object3.markov_fail_model(d))
		d1 = input('Enter the time period for recovery : ')
		print 'The probability of recovery at time ' + str(d1) + ' is ' + str(object3.bayes_recovery_model(d,d1))
