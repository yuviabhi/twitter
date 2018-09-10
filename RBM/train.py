## Training the model 

from RBM import RBM
import numpy as np
import pandas as pd
from input_feed import findNeighbourhood
from input_feed import getDistanceFromWaterbodies
from input_feed import map_coordinate_to_elevation
from input_feed import getPointsElevation



# Normalization  :  x-min(x) / max(x)-min(x)
def normalize(rawpoints):
    mins = np.min(rawpoints, axis=0)
    maxs = np.max(rawpoints, axis=0)
    rng = maxs - mins
    #print maxs, mins, rng
    return (rawpoints - mins) / rng


def shift():
	file_latlons = '/home/abhisek/Documents/abhisek-workspace/codes/twitter/extract_place/latlons-kolkata-20170724-20170913.csv'
	
	df_latlon = pd.read_csv(file_latlons)
	
	for row in df_latlon.itertuples():
		print row[1] , row[2]
		

def train(trX_norm):	
	
	model = RBM(2, 1, 0.001, ne=1000)
	model.fit(trX_norm)

	pred = model.predict(trX_norm)
	print np.concatenate([trX_norm,pred], axis=1)


def train_gbrbm(trX_norm):
	'''
	TRYING TO IMPLEMENT THE Gaussian-Bernoulli RBM USING KERAS	
	'''	
	from keras_extensions.rbm import GBRBM
	#from keras_extensions.models import SingleLayerUnsupervised
	batch_size = 5
	nb_epoch = 100
	lr = 0.001
	rbm = GBRBM(input_dim=2, hidden_dim=1)
	#train_model = SingleLayerUnsupervised()
    	#train_model.add(rbm)
	#train_model.fit(trX_norm, batch_size, nb_epoch, verbose=1, shuffle=False)


if __name__ == '__main__':
	
	
	data = pd.read_csv('input_file_dist_elev.csv')
	#print data.values
	data1 = np.array(data.values)
	trX = data1[0:100,2:4]  #Choosing only first 100 rows

	from sklearn import preprocessing
	trX_norm = preprocessing.normalize(trX)
	#trX_norm = normalize(trX)
	#print trX_norm
	
	
	train(trX_norm)
	#train_gbrbm(trX_norm)
	
	


	
