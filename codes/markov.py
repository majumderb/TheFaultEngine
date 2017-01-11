try:
   import csv
   import numpy as np
   import math
   from scipy.stats import exponweib
   import matplotlib.pyplot as plt
   import seaborn
except ImportError:
   print "please install csv numpy and math package"

def weibull(u,shape,scale):
    #Weibull distribution for wind speed u with shape parameter k and scale parameter A
    return (shape / scale) * (u / scale)**(shape-1) * np.exp(-(u/scale)**shape)

class markov_state():
    def __doc__():
        print 'This is the class markov model'
    def __init__(self,input_filename=None):
        self.streamdata = []
        with open(input_filename, 'rb') as csvfile:
            inputdata = csv.reader(csvfile)
            for row in inputdata:
                self.streamdata.append(str(row[0]))
    
        # MTTR Calculation
        failcount = 0
        failcount_list = []
        streamdata = self.streamdata
        for i in xrange(len(streamdata)):
            if streamdata[i] == 'OK':
                continue
            if streamdata[i] == 'Fail' and streamdata[i+1] != 'OK':
                failcount = failcount + 1
            if streamdata[i] == 'Fail' and streamdata[i+1] == 'OK':
                failcount = failcount + 1
                # taking count = 15 as a starting point of being permanent failure        
                if failcount > 15:
                    failcount = 0           
                    continue
                else: 
                    failcount_list.append(failcount)
                    failcount = 0
    
        MTTR = np.mean(failcount_list)
        # weibull distribution fit
        dd = exponweib.fit(failcount_list, floc=0,fa=1)
        dummy = list(set(list(failcount_list)))
        seaborn.set_style("darkgrid") 
        values,bins,hist = plt.hist(failcount_list,bins=len(dummy),range=(0,max(dummy)),normed=True,rwidth=.5)
        plt.plot(bins,weibull(bins,dd[1],dd[3]),label='Fitted Weibull Distribution')
        plt.xlabel('Recovery Time')
        plt.ylabel('Probability')
        plt.title('Historical Recovery Time Distribution')
        plt.legend()
        plt.show()
        # MTTF Calculation
        OKcount = 0
        OKcount_list = []
        for i in xrange(len(streamdata)):
            if streamdata[i] == 'Fail':
                continue
            if i != (len(streamdata)-1) and streamdata[i] == 'OK' and streamdata[i+1] != 'Fail':
                OKcount = OKcount + 1
            if i == (len(streamdata)-1) and streamdata[i] == 'OK':
                OKcount = OKcount + 1
            if i != (len(streamdata)-1) and streamdata[i] == 'OK' and streamdata[i+1] == 'Fail':
                OKcount = OKcount + 1
                OKcount_list.append(OKcount)
                OKcount = 0        
        MTTF = np.mean(OKcount_list)
        # MLT Calculation
        check_faillist = ['Fail' for i in xrange(15)]
        lifecount = 0
        lifecount_list = []
        for i in xrange(len(streamdata)):
            if streamdata[i] == 'OK':
                lifecount = lifecount + 1
                if streamdata[i+1:i+16] == check_faillist:
                    lifecount_list.append(lifecount)
                    lifecount = 0
        MLT = np.mean(lifecount_list)
        self.lamda = 1/MTTF
        self.mu = 1/MTTR
        self.delta = 1/MLT
        self.shape = dd[1]
        self.scale = dd[3]
	# Calculating weibull fitted markov failure probability of persistent failure
    def markov_fail_model(self,d):
        prob = self.delta/(self.delta + self.lamda*np.exp(-(d*1.0/self.scale)**self.shape))
        return prob
	# Calculating bayesian probability of recovery
    def bayes_recovery_prob(self,d,d1):
        prob = (self.shape / self.scale) * (d1 / self.scale)**(self.shape-1) * np.exp((d/self.scale)**self.shape-(d1/self.scale)**self.shape)
        return prob

    def bayes_recovery_model(self,d,d1):
        x = range(d+1,max(2*d,d1+1))
        y = [self.bayes_recovery_prob(d,i) for i in x]
        seaborn.set_style("darkgrid")		
        plt.plot(x,y)
        plt.xlabel('Recovery Time')
        plt.ylabel('Probability')
        plt.title('Probability of Conditional Recovery')
        plt.show()
        return self.bayes_recovery_prob(d,d1)
        
     
    
