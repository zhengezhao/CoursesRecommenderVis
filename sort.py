import pandas as pd

import json
from glob import glob
import scipy,sys
import numpy as np
from scipy.stats import pearsonr
from operator import itemgetter, attrgetter


with open("similarity.txt", "r") as ins:
	array =[]
	for line in ins:
		line = line.split(' ')
		precourse  = line[0][7:10]
		course = line[0][11:14]
		sim = line[1].replace('\n','')
		#print (precourse,course,sim)
		#break
		array.append((precourse,course,sim))
		
    	#array.append(line)
array = sorted(array, key=itemgetter(1,0))

with open('sortedsimilarity.txt','w') as fo:
	for i in array:
		fo.write(i[0]+','+i[1]+','+i[2]+'\n')
