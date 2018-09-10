'''
This code processes latlon columns and save into csv

INPUT:
2017-07-24 23:27:21,mit_chokshi,RT @vijayrupanibjp: Govt is doing its best to rescue those hit by flood. 12 teams of NDRF &amp; one Column of Army have been deployed in Banask...,RT| NDRF| Army,"[16.3792902, 80.53139279999999][40.2787639, -96.7472875]"
2017-07-24 23:21:19,besttopicin,Raw: Chopper Lifts Flood Stranded Hikers To Safety https://t.co/jLyX26MM1q,Chopper Lifts Flood| Hikers To Safety,[][]
2017-07-24 23:17:01,XTOLZ,RT @Edwardbani: Please Pray for our country. Flood is going on for a long time. https://t.co/M3ItGAbhwi,RT| Flood,"[37.2923509, -78.73277999999999]"


OUTPUT:
lat,lon
27.0238036,74.2179326
30.906587,75.840648
37.2923509,-78.73278
16.3792902,80.5313928


Run this code : python lat-lons.py kolkata 20170731

'''


import sys
import pandas as pd

location = str(sys.argv[1])
file_name = str(sys.argv[2])

x = pd.read_csv('flood-'+location+'-1000km-tweets-with-geo-coords-'+file_name+'-output.csv',usecols=["extr-latlon"])
output_file = 'latlons-'+location+'-'+file_name+'.csv'

print x.head()

latlons = []
each_latlons = [] 
X = [] 
Y = []

for row in x.itertuples():
	if (type(row[1]) is not float):
#		print type(row[1])
		latlons = str(row[1])
		#print latlons
		each_latlons = latlons.split("][")
		for each_latlon in each_latlons:
			each_latlon = str(each_latlon).replace("[", "")
			each_latlon = str(each_latlon).replace("]", "")
			#print each_latlon 
			try:
				X.append(float(each_latlon.split(",")[0]))
				Y.append(float(each_latlon.split(",")[1]))
			except:
				pass


#with open('latlons.csv', 'w'):
#    pass

#fo = open('latlons.csv', 'w')
#fo.close()
y = pd.DataFrame()
y['lat'] = X
y['lon'] = Y
y.to_csv(output_file,encoding='utf-8',index=False)





			



