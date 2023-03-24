#!/usr/bin/python
import tweepy
import csv 

consumer_key = ''  
consumer_secret = ''  
access_token = ''  
access_token_secret = '' 

# OAuth process, using the keys and tokens  
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)  
auth.set_access_token(access_token, access_token_secret)  

api = tweepy.API(auth)

# Open/create a file to append data to
csvFile = open('dataset/flood/world/flood-world-tweets-with-geo-coords-20170823.csv', 'w')
csvFile.write("created-at\ttext\tgeo-loc\tplace-bbox\tusr-loc\tusername\tfriends\tretweet\n")

#Use csv writer
csvWriter = csv.writer(csvFile,delimiter="\t")

#q=hashtag
#geocode = co-ordinates + radius
#tweepy.Cursor(api.search, q='cricket', geocode="22.5726,88.3639,200km").items():
#	Flood		kolkata  geocode="22.5726,88.3639,150km",

for tweet in tweepy.Cursor(api.search,
                           q = "flood",
                           since = "2017-08-16",
                           until = "2017-08-23",
			   lang = "en").items():

	try:
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
		    
csvFile.close()



