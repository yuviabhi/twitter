import pandas as pd
import numpy as np

input_file = "flood-kolkata-1000km-tweets-with-geo-coords-20170725-output.csv"
output_file = ""
create_output = "Y"


# read from csv to a dataframe
data = pd.read_csv(input_file, sep = ",",
	header=0,
        index_col=["created-at", "username"], 
        usecols=["created-at", "username", "text","extr-places","extr-latlon"],
        parse_dates=["created-at"])
#print data.head()


fv = []
feature_vector = np.array([])
feature_vector.reshape(1,-1)


for row in data.itertuples():

	try:
		word_count = len(row[1].split())
		flood_index = row[1].find('flood')
		#print 'Word Count: ' + word_count
		
		#if flood_index == '-1':
		#	print 'Flood index : NA'			
		#else:
		#	print 'Flood index : ' + flood_index

		#feature_vector = np.concatenate([[feature_vector,[word_count,flood_index]]],axis=0)
		fv.append([word_count,flood_index])

	
	except Exception,e:
		print str(e) 
		pass


try :
	feature_vector= np.array([fv])
	#print feature_vector


	#write into file
	with open('feature_vector_output.csv','w') as f:
		for row in feature_vector:
			np.savetxt(f, row, delimiter=',', fmt='%d')

	#read from file
	with open('feature_vector_output.csv') as f:print f.read()
except Exception,e:
	print str(e)



