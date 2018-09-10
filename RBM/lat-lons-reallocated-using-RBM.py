'''
Reallocate lat-lons(which were extracted from tweets) by RBM using elevation , proximity to waterbodies and rainfall
'''

import gdal
from gdalconst import *
import numpy as np
import pandas as pd
from osgeo import ogr
from shapely.geometry import Point
from RBM import RBM
import geopandas as gpd
import time
from input_feed import getRainfall
from sklearn import preprocessing
	

def map_coordinate_to_elevation(x, y, filename):
	try:
		dataset = gdal.Open(filename, GA_ReadOnly)
		transform = dataset.GetGeoTransform()
		#print transform
		xOrigin = transform[0]
		yOrigin = transform[3]
		pixelWidth = transform[1]
		pixelHeight = transform[5]

		band = dataset.GetRasterBand(1)
		bandtype = gdal.GetDataTypeName(band.DataType)
		x_off = int((x - xOrigin)/pixelWidth)
		y_off = int((y - yOrigin)/pixelHeight)
		try:
			data = band.ReadAsArray(x_off, y_off, 1, 1)
			#print "The elevation for co-ordinate ",x," and ",y," is ", data[0,0]
			return data[0,0]
		except:
			print "NAN"
			return 999999
	except: 
		print "Some Error Occured !"
		pass
	
	
	
def getPointsElevation(x,y):
	a = str(x).split(".")[0]
	b = str(y).split(".")[0]
	#print a,b
	
	if (int(a)<89 and int(a)>82 and int(b)<28 and int(b)>23) :
		#Reading elevation tiff dataset
		filename = "/home/abhisek/Documents/abhisek-workspace/codes/twitter/data-pull/dataset/elevation/srtm files/n"+b+"_e0"+a+"_1arc_v3.tif"
		return map_coordinate_to_elevation(x, y, filename)

	else :
		#print 'Co-ordinate out of range'
		return 999999	


#FINDING 8 NEIGHBORS OF A COORDINATE
def getNeighbors(x,y):
	#1 degree in google map is equal to 111.32 Kilometer. 
	#1Degree = 111.32KM. 
	#1KM in Degree = 1 / 111.32 = 0.008983. 
	#1M in Degree = 0.000008983
	b = 0.034  #shift factor
	nbr_x = []
	nbr_y = []
	ul_x = x-b
	nbr_x.append(ul_x)
	ul_y = y-b
	nbr_y.append(ul_y)
	um_x = x
	nbr_x.append(um_x)
	um_y = y-b
	nbr_y.append(um_y)
	ur_x = x+b
	nbr_x.append(ur_x)
	ur_y = y-b
	nbr_y.append(ur_y)
	l_x = x-b
	nbr_x.append(l_x)
	l_y = y
	nbr_y.append(l_y)
	r_x = x+b
	nbr_x.append(r_x)
	r_y = y
	nbr_y.append(r_y)
	ll_x = x+b
	nbr_x.append(ll_x)
	ll_y = y+b
	nbr_y.append(ll_y)
	lm_x = x
	nbr_x.append(lm_x)
	lm_y = y+b
	nbr_y.append(lm_y)
	lr_x = x-b
	nbr_x.append(lr_x)
	lr_y = y+b
	nbr_y.append(lr_y)
	return nbr_x , nbr_y



##GET INDEX & VALUES OF 8 NEIGHBORS	which has MAX Probability i.e. most vulnerable point
def maxProbability(nbr_x, nbr_y, model):
	probabilities = []
	for i in zip(nbr_x, nbr_y) :	
		dist = getDistanceFromWaterbodies(Point(i[1],i[0]),'/home/abhisek/Documents/abhisek-workspace/codes/twitter/data-pull/dataset/water_bodies/Bihar Waterbodies/water_bodies_bihar.shp')
		elev = getPointsElevation(i[0],i[1])
		rainfall = getRainfall(i[0],i[1],'/home/abhisek/Documents/abhisek-workspace/codes/twitter/data-pull/dataset/Rainfall Data Collection/shape/bihar-rainfall-2017.shp')
		point = np.array([[1/float(dist), 1/float(elev), rainfall[0]]])
		#point = np.array([[dist, elev, rainfall[0]]])
		
		
		point = preprocessing.normalize(point,norm='l1')
		
		
		pred = model.predict(point)
		probabilities.append(pred)
	return np.argmax(probabilities), np.max(probabilities) 	


#Returns the nearest distance of a point from the waterbodies
def getDistanceFromWaterbodies(point, filename):
	shapefile = gpd.read_file(filename)
	#point = Point(lat,lon)
	return point.distance(shapefile.geometry[0])

##SHIFTING POINT X,Y and returns newX, newY and isShift boolean
def shift_by_RBM(x, y, model):
	this_dist = getDistanceFromWaterbodies(Point(y,x),'/home/abhisek/Documents/abhisek-workspace/codes/twitter/data-pull/dataset/water_bodies/Bihar Waterbodies/water_bodies_bihar.shp')
	this_elev = getPointsElevation(x,y)
	this_rainfall = getRainfall(x,y,'/home/abhisek/Documents/abhisek-workspace/codes/twitter/data-pull/dataset/Rainfall Data Collection/shape/bihar-rainfall-2017.shp')
	
	#print this_elev , x , y
	#print this_dist,this_elev,this_rainfall[0]
	
	if(this_elev == 999999):
		return x,y,0
	else:
		this_point = np.array([[1/float(this_dist), 1/float(this_elev), this_rainfall[0]]])
		#this_point = np.array([[this_dist, this_elev, this_rainfall[0]]])
		
				
		this_point = preprocessing.normalize(this_point, norm='l1')
		
		
		this_pred = model.predict(this_point)	
		nbr_x , nbr_y = getNeighbors(x,y)

		maxIndex, maxValue = maxProbability(nbr_x, nbr_y, model)
		this_pred = this_pred.flatten()
		print 'Point: ',this_point, ' Dist: ',this_dist,' Elev: ', this_elev, ' Rf: ', this_rainfall[0],' Pred: ', this_pred[0], ' Neighbr: ',maxValue,' N. Index: ', maxIndex
		
		if(this_pred[0] >= maxValue) :
			#print x,y,' Point is fix\n'
			return x, y, 0
		else :
			#print x,y,' Point will shift to : ',nbr_x[maxIndex], nbr_y[maxIndex]
			return nbr_x[maxIndex], nbr_y[maxIndex], 1
			

    
def train(model):
	#data = pd.read_csv('input_file.csv')
	
	###############################
	#change here : file will be 'input_file_buffer_dist_elev_rainfall.csv'
	data = pd.read_csv('input_file_buffer_dist_elev_rainfall.csv')
	###############################
	
	#print data.values
	data1 = np.array(data.values)
	trX = data1[:,2:5]
	#trX = data1[0:100,2:5] #only first 100 rows
	trX[:,0] = 1/(trX[:,0].astype(float)) # inverting the distance	
	trX[:,1] = 1/(trX[:,1].astype(float)) # inverting the elevation
	trX[:,2] = trX[:,2].astype(float) # inverting the rainfall
	#print 'after inverting ..... \n\n', trX
	
	
	trX_norm = preprocessing.normalize((trX.astype(float)), norm='l1')
	
	
	#print trX_norm, maxs, mins
	#np.savetxt('trX_norm.csv', trX_norm, delimiter=',') 
	model.fit(trX_norm)
	#model.fit(trX)
	
	'''
	try:
		predict = model.predict(trX_norm)
		a = np.concatenate([trX_norm,predict], axis=1)
		np.savetxt("prob-dist-2.csv", a, delimiter=",")
		print 'Saved prediced probabilities'
	except :
		print 'Unable to Save prediced probabilities'		
	'''	
		
	return model 



def main():

	eps = '0.2'
	minsamples = '6'
	place = 'kolkata'
	dataset = '20170724-20170913'
	
	fname = '/home/abhisek/Documents/abhisek-workspace/codes/twitter/extract_place/latlons-'+place+'-'+dataset+'.csv'
	
	output = '/home/abhisek/Documents/abhisek-workspace/codes/twitter/extract_place/reallocated-latlons-'+place+'-'+dataset+'-using-RBM.csv'

	with open(fname, "r") as file:
		lines = file.read().split("\n")
		#print lines

	new_points = 'lat,lon\n'	
	
	model = RBM(3, 1, 0.001, ne=10, bt=10)
	time_training_start = time.ctime()
	print 'Training started... ', time_training_start
	model = train(model)
	time_training_end = time.ctime()
	print 'Training completed... ', time_training_end
	
	print 'No of points ',len(lines)-1
	line_no = 1
	for line in lines[:-1]:
		if('lat' not in line): #to ignore the first line in the dataset
			print "\nProcessing... ",int(line_no),"\n", line
			line_no = line_no + 1
			pt= line.split(',')
			isShift = 1
			shift_x = float(pt[1])
			shift_y = float(pt[0])
			while(int(isShift)):
				shift_x, shift_y, isShift = shift_by_RBM(shift_x, shift_y, model)
				if(isShift == 1):
					print '------------ SHIFTED --------------', pt[0],pt[1],' to ',shift_x, shift_y
				#else:
					#print '------------ INTACT --------------', pt[0],pt[1],' to ',shift_x, shift_y
			if(shift_x !=0 and shift_y!=0):
				new_points +=str(shift_y) + ',' + str(shift_x) + '\n'
			print 'Processing Done... '

	time_output = time.ctime()
	print '\n\n-#-#-#-#-#-#-#-#-#-#-#-#-   Output [',time_output,']   -#-#-#-#-#-#-#-#-#-#-#-#-\n\n'
	print 'New points: ',len(new_points.split('\n'))-1 

	with open(output, "w") as file:
		file.write(new_points)
		
	print '\nTraining started at ', time_training_start
	print 'Training ended at ', time_training_end
	print 'Final Output at ', time_output




if __name__ == "__main__":
	main()

	
	


