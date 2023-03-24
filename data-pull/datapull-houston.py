#!/usr/bin/python
import tweepy
import csv 
import time
import datetime as dt  

consumer_key = ''  
consumer_secret = ''  
access_token = ''  
access_token_secret = ''  

# OAuth process, using the keys and tokens  
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)  
auth.set_access_token(access_token, access_token_secret)  

api = tweepy.API(auth)

#today = dt.datetime.today().strftime("%Y-%m-%d")
#print (time.strftime("%d/%m/%Y"))

today = dt.date.today()
week_ago = today - dt.timedelta(days=7)


# Open/create a file to append data to
csvFile = open('dataset/storm/houston/hurricane-houston-1000km-tweets-with-geo-coords-'+str(today).replace('-','')+'-#hurricaneharvey-2.csv', 'w')
csvFile.write("created-at\ttext\tgeo-loc\tplace-bbox\tusr-loc\tusername\tfriends\tretweet\n")

#Use csv writer
csvWriter = csv.writer(csvFile,delimiter="\t")

#	hurrycane		texas  geocode=31.9686 N, 99.9018 W
#	hurrycane		houston  geocode=29.7604 N, 95.3698 W
 

def parseTweet() :
	
	for tweet in tweepy.Cursor(api.search,
			                   q = "hurricaneharvey",
			                   since = week_ago,
			                   until = today,
				   			   geocode="29.7604,95.3698,1000km",
			                   lang = "en").items():
	
		if (tweet.place is None):
			tweet_place_bbox='NA'
		else:
			tweet_place_bbox = tweet.place.bounding_box.coordinates

		#if (tweet.coordinates is None):
		#	tweet_coords='-'

		#if "coordinates" in tweet_coords :		

		if tweet.geo is None:
			tweet_geo = 'NA'
		else:
			tweet_geo = tweet.geo

		# Write a row to the CSV file. I use encode UTF-8
		csvWriter.writerow([tweet.created_at, tweet.text.encode('utf-8'), tweet_geo, tweet_place_bbox, tweet.user.location.encode('utf-8'), tweet.user.screen_name, tweet.user.friends_count, tweet.retweet_count])

		print tweet.created_at, tweet.text, tweet_geo, tweet_place_bbox, tweet.user.location, tweet.user.screen_name, tweet.user.friends_count, tweet.retweet_count
	

try:
	parseTweet()			   
			   
except Exception,e:
	print(e.reason)
	csvFile.close()
	#print 'Dummy : Sleeping for 24 hours ... ' +time.ctime()
	#time.sleep(86400)
	#print 'Waked up ... ' +time.ctime()
	#parseTweet()
	
finally:	
	csvFile.close()	   
	#print 'Dummy : Sleeping for 24 hours ... ' +time.ctime()
	#time.sleep(86400)
	#print 'Waked up ... ' +time.ctime()
	#parseTweet()
		    




