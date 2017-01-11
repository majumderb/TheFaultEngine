import seaborn
import matplotlib.pyplot as plt
import numpy as np
# plotting weibull hazard function for different scale factors
def fun(k,d1):
    prob = (k / 3) * (d1*1.0 / 3)**(k-1) * np.exp((1.0/3)**k-(d1*1.0/3)**k)
    return prob
x = range(2,10)
y1 = [fun(2.0,i) for i in x]
y2 = [fun(5.0,i) for i in x]
y0 = [fun(1.0,i) for i in x]
y3 = [fun(.2,i) for i in x]
y4 = [fun(.5,i) for i in x]
seaborn.set_style("darkgrid")
plt.plot(x,y3,color='blue',label='shape = 0.2')
plt.plot(x,y4,color='red',label='shape = 0.5')
plt.plot(x,y0,color='black',label='shape = 1.0')
plt.plot(x,y1,color='yellow',label='shape = 2.0')
plt.plot(x,y2,color='green',label='shape = 5.0')
plt.xlabel('Time')
plt.ylabel('Probability')
plt.title('Comparison of different recovery functions')
plt.legend()
plt.show()
# Plotting root cause analysis time complexity
n = [150, 1500, 13000, 105000]
sys_times = [0.328,.361,.515,2.077]
total_times = [3.941,7.404,34.077,199.923]
seaborn.set_style("darkgrid")
plt.plot(n,sys_times,color='blue',label='Sys Time')
plt.plot(n,total_times,color='red',label='Sys Time + User Time')
plt.xlabel('Number of Devices')
plt.ylabel('Time (in seconds)')
plt.title('Time complexity of Root Cause Analysis')
plt.legend(loc = 'upper left')
plt.show()
# Plotting correlated devices time complexity
n = [150, 1500, 7500, 13000]
sys_times = [0.328,5.41,19.55,23.678]
total_times = [3.446,2100.23,107976.452,301230.19]
seaborn.set_style("darkgrid")
plt.plot(n,sys_times,color='blue',label='Sys Time')
plt.plot(n,total_times,color='red',label='Sys Time + User Time')
plt.xlabel('Number of Devices')
plt.ylabel('Time (in seconds)')
plt.title('Time complexity of Clustering of Correlated Devices')
plt.legend()
plt.show()
# Plotting markov probability time complexity
n = [300,1200,5000,22000]
sys_times = [.412,.392,.4,.35]
total_times = [4.137,4.141,4.452,4.247]
seaborn.set_style("darkgrid")
plt.plot(n,sys_times,color='blue',label='Sys Time')
plt.plot(n,total_times,color='red',label='Sys Time + User Time')
plt.xlabel('Size of the Log File')
plt.ylabel('Time (in seconds)')
plt.title('Time complexity of Markov Failure Probability Calculation')
plt.legend(loc='best')
plt.show()
