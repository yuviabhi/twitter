#!/usr/bin/python
import tweepy
import csv 
import time
import datetime as dt  

consumer_key = 'dWSksJ98HCFhBA8SCc9qsiTCv'  
consumer_secret = 'BrZIrJ8VMWh40sqI7bKgdPpuPWEXdq4OnVKjol9FSOHNx9JHYS'  
access_token = '399258420-0DQdayCWBMUjAMbUCRSBemHPgFm3A6DbMolUQGmi'  
access_token_secret = 'k9eCGx6QPnU8yFrghsG5xE8RWsOoMtSejhj1kUsTKcItz'  

# OAuth process, using the keys and tokens  
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)  
auth.set_access_token(access_token, access_token_secret)  

api = tweepy.API(auth)

#auto run
today = dt.date.today()
week_ago = today - dt.timedelta(days=7)

#manual run
#today='2017-08-02'
#week_ago = '2017-09-29'

# Open/create a file to append data to
csvFile = open('dataset/earthquake/mexico/quake-mexico-500km-tweets-with-geo-coords-'+str(today).replace('-','')+'.csv', 'w')
csvFile.write("created-at\ttext\tgeo-loc\tplace-bbox\tusr-loc\tusername\tfriends\tretweet\n")

#Use csv writer
csvWriter = csv.writer(csvFile,delimiter="\t")

#q=hashtag
#geocode = co-ordinates + radius
#tweepy.Cursor(api.search, q='cricket', geocode="22.5726,88.3639,200km").items():

#	Flood		kolkata  geocode="22.5726,88.3639,150km"
#	Earthquake		Mexico  geocode="19.4326, 99.1332,500km"

def parseTweet() :
	try:	
		for tweet in tweepy.Cursor(api.search,
				                   q = "FuerzaMexico",
				                   since = week_ago,
				                   until = today,
					   			   geocode="23.6345,102.5528,500km",
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
		

	except tweepy.TweepError as e:
 		print(e.reason)


try:
	parseTweet()			   
			   
except Exception,e:
	print(e.reason)
	print 'Sleeping for 1 mins... ' +time.ctime()
	time.sleep(1)
	print 'Wake up ... ' +time.ctime()
	#parseTweet()
			   
		    
csvFile.close()



