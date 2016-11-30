import pandas as pd

import json
from glob import glob
import scipy,sys
import numpy as np
from scipy.stats import pearsonr

'''
This one is used to read the orignial normal_cs.csv and get the attribute we want
it also correct the COursenumber to 3-digits
Input: normal_cs.csv
OUTPUT: output2.txt
'''

with open('normal_cs.csv') as f:
	with open('output2.txt','w') as fo:

		l = f.readline().replace('\n','')
		while l:
			l = l.split(',')
			student = l[1]
			#course = l[3].replace('"','') + l[4].replace('"','')
			term = l[2]
			grade = int(l[5].replace('"',''))
			fo.write(student+','+l[4][:3]+","+term+','+str(grade)+'\n')
			#df1[course][student] = grade
			l = f.readline().replace('\n','')



'''
This one is used for filter data, we delete all the courses that are taken by less than 10 students
and students who have taken less than 10 courses
INPUT: output2.csv
OUTPUT: output2.filter.csv
'''
u_cols = ['StudentID','CourseNumber','Term', 'Grade']

df = pd.read_csv('output2.txt', sep=',', names=u_cols)

dfFiltered = None
for stu in set(df['StudentID']):
	df1 = df[df['StudentID'] == stu]
	if df1.shape[0] > 10:
		if dfFiltered is not None:
			dfFiltered = pd.concat([dfFiltered,df1])
		else:
			dfFiltered = df1


df = dfFiltered

dfFiltered2 = None
for course in set(df['CourseNumber']):
	df1 = df[df['CourseNumber'] == course]
	if df1.shape[0] > 10:
		if dfFiltered is not None:
			dfFiltered2 = pd.concat([dfFiltered2,df1])
		else:
			dfFiltered2 = df1

dfFiltered2.to_csv('output2filter.txt',header=False,index=False)


	


'''
This one is used for build the Matrix for  course-student 
INPUT: output2filter.txt
OUTPUT: dfsc.pkl
'''

df = pd.read_csv('output2filter.txt', sep=',', names=u_cols)

dfsc = pd.DataFrame(index= set(df['CourseNumber']) ,
					 columns= set(df['StudentID'])  )
dfsc = pd.DataFrame()
print(dfsc)

with open('output2filter.txt') as f:
	l = f.readline().replace('\n','')
	while l:
		
		l = l.split(',')
		student,course,_,grade = l
		#print (student,course,grade)
		dfsc.set_value(course,student,float(grade))
		#print(dfsc.shape)
		l = f.readline().replace('\n','')
print(dfsc.shape)


dfsc.to_pickle('dfsc.pkl')




'''
This one is caculate the predicted matrix 
'''
dfsc0 = pd.read_pickle('dfsc.pkl')
preddf = None
#print(dfsc.shape)
dfsc0 = dfsc0.transpose().fillna(dfsc0.mean(axis=1)).transpose()

dfsc = (dfsc0.transpose() - dfsc0.mean(axis=1)).transpose()


for i1 in range(dfsc.shape[0]):
	pers= np.array([])
	for i2 in range(dfsc.shape[0]):
		if i2!=i1:
			per = scipy.stats.pearsonr(dfsc.iloc[i1],dfsc.iloc[i2])[0]
			pers = np.append(pers,per)
				
	#print (pers)
	#print (dfsc.iloc[i1])
	#print(dfsc.iloc[i1].name)	 
	dfsctem = dfsc0.drop(dfsc0.iloc[i1].name)
	#print (dfsctem)
	scorePred = pers.dot(dfsctem)/np.sum(pers)	
	#print (scorePred.shape)
	
	if preddf is None:
		preddf = scorePred.reshape([1,-1])
	else:
		preddf = np.append(preddf,scorePred.reshape([1,-1]),axis=0)
#print (preddf)	
preddf = pd.DataFrame(preddf, index=dfsc.index, columns=dfsc.columns)
		

'''
This one is used to generate the parallel coordiate
'''

for i in sorted(set(df['CourseNumber'])):
	for j in sorted(set(df['CourseNumber'])):
		
		if i!=j:
			#print(i,j)
			df1 = df[df['CourseNumber']==i]
			df2 = df[df['CourseNumber']==j]
			dfm = df1.merge(df2, on='StudentID')
			dfm2 = dfm[ dfm['Term_x'] < dfm['Term_y'] ]
			
			if dfm2.shape[0]>10:
				
			
				
				filename = str(dfm2.iloc[0]['CourseNumber_x']) +'_'+str(dfm2.iloc[0]['CourseNumber_y'])  
				dfm2.to_csv('./data/'+filename+'.txt')
		

	
'''
This is is calcuate the similarity between each pair of courses using the average of the  difference


'''

for filename in glob('./data/*.txt'):
	with open(filename) as f:
		with open('similarity.txt','a') as simlirityfile:
			l = f.readline().replace('\n','')
			l = f.readline().replace('\n','')
			diffsum,i =0,0
			while l:
				l = l.split(',')
				student,course,grade = l[1],l[5],float(l[7])
				diff = grade - preddf[student][course]
				diffsum += diff
				i+=1
				l = f.readline().replace('\n','')
			filename_rec = diffsum/i
			simlirityfile.write(filename + ' '+ str(filename_rec)+'\n')
		





	



