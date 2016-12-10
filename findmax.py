import pandas as pd

import json
from glob import glob
import scipy,sys
import numpy as np
from scipy.stats import pearsonr
from operator import itemgetter, attrgetter
import matplotlib.pyplot as plt


with open("sortedsimilarity.txt", "r") as ins:
	array =[]
	for line in ins:
		line = line.split(',')
		precourse  = line[0]
		course = line[1]
		sim = float(line[2].replace('\n',''))
		#print (precourse,course,sim)
		#break
		array.append((precourse,course,sim))
		
    	#array.append(line)
array = sorted(array, key=itemgetter(2))
print (array)

array = np.array(array)
sim = np.array(array[:,2], dtype=np.float64)
print (array[:,2].dtype)
x= np.arange(len(array))
print(x)
plt.hist(sim)
plt.show()
