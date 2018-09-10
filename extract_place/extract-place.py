'''
This code extracts location names from tweets and generate a new column with lat,lon values of those locations by forward geocoding

Input :
-----------------
2017-07-24 23:27:21,mit_chokshi,RT @vijayrupanibjp: Govt is doing its best to rescue those hit by flood. 12 teams of NDRF &amp; one Column of Army have been deployed in Banask...,RT| NDRF| Army
2017-07-24 23:21:19,besttopicin,Raw: Chopper Lifts Flood Stranded Hikers To Safety https://t.co/jLyX26MM1q,Chopper Lifts Flood| Hikers To Safety,[][]
2017-07-24 23:17:01,XTOLZ,RT @Edwardbani: Please Pray for our country. Flood is going on for a long time. https://t.co/M3ItGAbhwi,RT| Flood

Output:
-----------------
2017-07-24 23:27:21,mit_chokshi,RT @vijayrupanibjp: Govt is doing its best to rescue those hit by flood. 12 teams of NDRF &amp; one Column of Army have been deployed in Banask...,RT| NDRF| Army,"[16.3792902, 80.53139279999999][40.2787639, -96.7472875]"
2017-07-24 23:21:19,besttopicin,Raw: Chopper Lifts Flood Stranded Hikers To Safety https://t.co/jLyX26MM1q,Chopper Lifts Flood| Hikers To Safety,[][]
2017-07-24 23:17:01,XTOLZ,RT @Edwardbani: Please Pray for our country. Flood is going on for a long time. https://t.co/M3ItGAbhwi,RT| Flood,"[37.2923509, -78.73277999999999]"

ALSO UPDATING THE placesdictionary.csv WHICH CONTAINS ALL THE PLACES' LAT-LONS WHICH ARE EXTRACTED SO THAT WE CAN REDUCE GOOGLE-API USAGE.


Run this code : 
-----------------
python extract-place.py kolkata 20170827
python extract-place.py mumbai 20170827
'''


import sys
import nltk
import pandas as pd
import numpy as np
import geocoder

location = str(sys.argv[1])
file_name = str(sys.argv[2])

input_file = "~/Documents/abhisek-workspace/codes/twitter/data-pull/dataset/flood/"+location+"/flood-"+location+"-1000km-tweets-with-geo-coords-"+file_name+".csv"
output_file = "flood-"+location+"-1000km-tweets-with-geo-coords-"+file_name+"-output.csv"
create_output = "Y"

proxies = '172.16.2.30:8080'
timeout=10.0



#EXTRACT NAMED ENTITIES
def extract_entity_names(t):
    entity_names = []

    if hasattr(t, 'label') and t.label:
        if t.label() == 'NE':
            entity_names.append(' '.join([child[0] for child in t]))
        else:
            for child in t:
                entity_names.extend(extract_entity_names(child))

    return entity_names





# extract place names from tweets
def get_place_names(line):
	sentences = nltk.sent_tokenize(line)
        tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
        tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
        chunked_sentences = nltk.ne_chunk_sents(tagged_sentences, binary=True)

        entities = []
        for tree in chunked_sentences:
            entities.extend(extract_entity_names(tree))   	    

        #print(entities)

	#data['extr-places'] = entities 
	return str(entities)

	
	
	


#query into the dictionary
def getLatLonFromDictionary(place, place_dict):
	try:

		place = place.replace(" ","")
		latlon = place_dict[place]
		#print "retrv - "+latlon
		return latlon
	except Exception,e:
		#print "oops " + str(e)
		return ""
	
	
	
	
	
	
#update the dictionary	
def updateDictionary(place, arr_latlon):
	latlon = str(arr_latlon)
	place_dict[place] = latlon	#added to dictionary place_dict
	
	if (len(arr_latlon)>0):
		with open('PlacesDictionary.csv', 'a') as f:
			#arr = np.array(latlon)
			f.write(place+","+str(arr_latlon[0])+","+str(arr_latlon[1])+"\n")
			f.close	
	






# read from csv to a dataframe
data = pd.read_csv(input_file, sep = "\t",
	header=0,
        index_col=["created-at", "username"], 
        usecols=["created-at", "username", "text","geo-loc","place-bbox","usr-loc"],
        parse_dates=["created-at"])
#print data.head()







print "Places name extraction started..."
entities_array=[]
# iterate through tweets
for row in data.itertuples():

	try:
		entities = get_place_names(row[1])
		entities = str(entities).replace("[", "")
		entities = str(entities).replace("]", "")
		entities = str(entities).replace("\"", "")
		entities = str(entities).replace(",", "|")
		entities = str(entities).replace("'", "")
		entities_array.append(entities)

	except Exception,e: 
		#print str(e)
		entities_array.append('#')		
		pass
		
		
data['extr-places'] = entities_array
#print data.head()

print "Places name extraction ended..."






print "Forward geocoding started..."

#populing the place_dict{} from PlacesDictionary.csv file
place_dict = {}
place = pd.read_csv("PlacesDictionary.csv", sep=",", header=0)
for row in place.itertuples():
	place_dict[row[1]] = '['+str(row[2]) +','+ str(row[3])+']'



latlon_array = []
latlon_str = ""
count_google=0
count_dictionary=0

# forward-geocoding each places and save to a new column
for row in data.itertuples():

	try:
		str_places = row[5]
		places = str_places.strip().split("|")
		
		for place in places:
			place = place.replace(" ","")
				
			if place in ("#","RT"):
				pass
				
			else:
				latlon = getLatLonFromDictionary(place, place_dict)				
				#print "hello - "+latlon
				if (latlon in ("")):
					g = geocoder.google(place)
					#g = geocoder.google(place, proxies=proxies, timeout=timeout)
					updateDictionary(place, g.latlng)
					latlon = str(g.latlng)
					print 'Google - '+ place + '\t' + latlon 
					count_google = count_google + 1
					
				else:
					print 'Dictionary - ' + place + '\t' + latlon 
					count_dictionary = count_dictionary + 1
				
				#print place + '\t' + latlon
				latlon_str = latlon_str + latlon

		latlon_array.append(latlon_str)
		#print latlon_str
		latlon_str = ""


	except Exception,e:
		print str(e)
		latlon_array.append("NA")
		pass




data['extr-latlon'] = latlon_array
#print data.head()

print "Forward geocoding ended..."

print "Request to Google : ",count_google
print "Request to Dictionary : ",count_dictionary

# save to a csv file
if create_output in ("Y"):
	data.to_csv(output_file)

