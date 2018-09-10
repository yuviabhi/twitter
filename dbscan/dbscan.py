#DBSCAN Algo

import pandas as pd
from sklearn.cluster import DBSCAN
import numpy as np
from sklearn import metrics
from sklearn.preprocessing import StandardScaler

'''
Run : python dbscan.py
Change the Constants value accordingly for each run
'''

#Constants
date = '20170724-20170913'
place = 'kolkata'
_eps = 0.2
_min_samples = 6

#X = pd.read_csv('~/Documents/abhisek-workspace/codes/twitter/extract_place/latlons-'+place+'-'+date+'.csv')
X = pd.read_csv('~/Documents/abhisek-workspace/codes/twitter/extract_place/reallocated-latlons-'+place+'-'+date+'-using-RBM.csv')
#X_fit=np.loadtxt('/home/abhisek/Documents/abhisek-workspace/codes/twitter/extract_place/latlons-'+place+'-'+date+'.csv',delimiter=",",skiprows=1)
output_file = 'dbscan_clusters_rellocated_'+place+'_'+date+'-eps_'+str(_eps)+'_minsamples_'+str(_min_samples)+'.csv'
#print X.head()
#print X.head().to_string(index=False)

#X_fit = StandardScaler().fit_transform(X)
X_fit = np.array(X)
db = DBSCAN(eps=_eps, min_samples=_min_samples).fit(X_fit)
print db.labels_
core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
core_samples_mask[db.core_sample_indices_] = True
labels = db.labels_

# Number of clusters in labels, ignoring noise if present.
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

cl_array_x = []
cl_array_y = []

cluster_nos = []

df_univ = pd.DataFrame(columns=['lat','lon'])

i=1

# #############################################################################
# Plot result
import matplotlib.pyplot as plt

# Black removed and is used for noise instead.
unique_labels = set(labels)
colors = [plt.cm.Spectral(each)
          for each in np.linspace(0, 1, len(unique_labels))]
for k, col in zip(unique_labels, colors):
	if k == -1:
		  # Black used for noise.
		  col = [0, 0, 0, 1]

	class_member_mask = (labels == k)

	xy = X[class_member_mask & core_samples_mask]    
	#print '1ST..................................................'
	#print xy

	#saving each cluster using numpy array
	#np.savetxt(output_file+"_#"+str(i)+".csv", np.float32(xy), delimiter=",")
	#i=i+1       
		  
	#saving each cluster using pandas dataframe
	#xy.to_csv(output_file+"_#_"+str(i)+".csv",encoding='utf-8',index=False, header=['lat','lon'])
	#i=i+1       

	df_univ=df_univ.append(xy, ignore_index=True)
	# generating cluster_nos array
	for row in xy.iterrows():
		  cluster_nos.append(i)
	i=i+1   

	# Appending x columns to cl_array_x and y columns to cl_array_y 
	#cl_array_x.append(xy[:, 0])
	#cl_array_y.append(xy[:, 1])

	xy_fit = X_fit[class_member_mask & core_samples_mask]    		
	plt.plot(xy_fit[:, 0], xy_fit[:, 1], 'o', markerfacecolor=tuple(col),
		markeredgecolor='k', markersize=14)


	xy_fit = X_fit[class_member_mask & ~core_samples_mask]    
	#print '2ND..................................................'
	#print xy

	# Appending x columns to cl_array_x and y columns to cl_array_y 
	#cl_array_x.append(xy[:, 0])
	#cl_array_y.append(xy[:, 1])


	plt.plot(xy_fit[:, 0], xy_fit[:, 1], 'o', markerfacecolor=tuple(col),
		       markeredgecolor='k', markersize=6)
             
#cl_array_x = np.array(cl_array_x)
#cl_array_y = np.array(cl_array_y)


'''
print 'cluster array of x has total ' + str(np.size(cl_array_x)) + ' points'
print cl_array_x
print 'cluster array of y has total '+ str(np.size(cl_array_y)) + ' points'
print cl_array_y
'''

'''
#Printing the generated array
i=0
for m,n in zip(cl_array_x,cl_array_y):
    i = i+1
    print i,m,n    
'''



#print len(cluster_nos)
#print df_univ.shape
df_univ['cluster'] = np.array(cluster_nos)
df_univ.to_csv(output_file,encoding='utf-8',index=False)

print 'Estimated number of clusters: %d' % n_clusters_
plt.title('Estimated number of clusters: %d' % n_clusters_)
plt.show()



