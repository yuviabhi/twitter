#!/usr/bin/python
import tweepy
import csv 
import time
import datetime as dt  
import os.path

def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            time.sleep(15 * 60)
            
def parseTweet(csvFile) :
	try:	
		#Use csv writer
		csvWriter = csv.writer(csvFile,delimiter="\t")
		
		for tweet in limit_handled(tweepy.Cursor(api.search, 
		q = "flood", 
		since = week_ago, 
		until = today, 
		geocode="21.1458,79.0882,2000km", 
		lang = "en").items()):
		
			if (tweet.place is None):
				tweet_place_bbox='NA'
			else:
				tweet_place_bbox = tweet.place.bounding_box.coordinates
			if tweet.geo is None:
				tweet_geo = 'NA'
			else:
				tweet_geo = tweet.geo
				
			# Write a row to the CSV file. I use encode UTF-8
			csvWriter.writerow([
			tweet.created_at, 
			tweet.text.encode('utf-8'), 
			tweet_geo, tweet_place_bbox, 
			tweet.user.location.encode('utf-8'), 
			tweet.user.screen_name, 
			tweet.user.friends_count, 
			tweet.retweet_count])
			
			print tweet.created_at, 
			tweet.text, 
			tweet_geo, 
			tweet_place_bbox, 
			tweet.user.location, 
			tweet.user.screen_name, 
			tweet.user.friends_count, 
			tweet.retweet_count
			#print tweet
			
	except tweepy.TweepError as e:
 		print(e)
 		
 		

if __name__ == "__main__":

	try:
		consumer_key = 'dWSksJ98HCFhBA8SCc9qsiTCv'  
		consumer_secret = 'BrZIrJ8VMWh40sqI7bKgdPpuPWEXdq4OnVKjol9FSOHNx9JHYS'  
		access_token = '399258420-0DQdayCWBMUjAMbUCRSBemHPgFm3A6DbMolUQGmi'  
		access_token_secret = 'k9eCGx6QPnU8yFrghsG5xE8RWsOoMtSejhj1kUsTKcItz'  

		# OAuth process, using the keys and tokens  
		auth = tweepy.OAuthHandler(consumer_key, consumer_secret)  
		auth.set_access_token(access_token, access_token_secret)  

		api = tweepy.API(auth)

		#auto run
		#today = dt.date.today()
		#week_ago = today - dt.timedelta(days=7)

		#manual run
		today='2018-07-08'
		week_ago = '2018-07-01'

		# Open/create a file to append data to
		projpath = os.path.abspath(os.path.join('', os.pardir))
		filepath = '/dataset/flood/kerala/flood-kerala-2000km-tweets-with-geo-coords-'+str(today).replace('-','')+'.csv'
		
		with open (projpath + filepath, 'w') as csvFile:
			csvFile.write("created-at\ttext\tgeo-loc\tplace-bbox\tusr-loc\tusername\tfriends\tretweet\n")
			parseTweet(csvFile)	

		# Flood		nagpur  geocode="21.1458,79.0882,2000km",    21.1458 N, 79.0882 E 
		# NAGPUR Since its the central point of india

	
				   
				   
	except Exception as e:
		print(e)
		#print 'Sleeping for 1 mins... ' +time.ctime()
		#time.sleep(1)
		#print 'Wake up ... ' +time.ctime()
		#parseTweet(csvWriter)
				   
				


'''
SAMPLE CURSOR IN JSON

{
    "created_at": "Thu Jul 28 00:08:39 +0000 2016",
    "in_reply_to_status_id": null,
    "id_str": "758454081656467456",
    "retweeted": false,
    "entities": {
        "hashtags": [
            {
                "text": "30secLL_bot",
                "indices": [
                    25,
                    37
                ]
            }
        ],
        "urls": [],
        "symbols": [],
        "media": [
            {
                "url": "https://t.co/oQjf1qKsDC",
                "id_str": "680158074653442048",
                "source_status_id": 680158389477875700,
                "source_user_id": 4017736032,
                "source_user_id_str": "4017736032",
                "media_url_https": "https://pbs.twimg.com/ext_tw_video_thumb/680158074653442048/pu/img/UkJ-B_AqbC_vEOcY.jpg",
                "source_status_id_str": "680158389477875712",
                "sizes": {
                    "medium": {
                        "w": 600,
                        "h": 338,
                        "resize": "fit"
                    },
                    "small": {
                        "w": 340,
                        "h": 191,
                        "resize": "fit"
                    },
                    "thumb": {
                        "w": 150,
                        "h": 150,
                        "resize": "crop"
                    },
                    "large": {
                        "w": 1024,
                        "h": 576,
                        "resize": "fit"
                    }
                },
                "display_url": "pic.twitter.com/oQjf1qKsDC",
                "type": "photo",
                "id": 680158074653442000,
                "indices": [
                    38,
                    61
                ],
                "expanded_url": "http://twitter.com/30seclovelive/status/680158389477875712/video/1",
                "media_url": "http://pbs.twimg.com/ext_tw_video_thumb/680158074653442048/pu/img/UkJ-B_AqbC_vEOcY.jpg"
            }
        ],
        "user_mentions": []
    },
    "possibly_sensitive": false,
    "in_reply_to_user_id_str": null,
    "coordinates": null,
    "retweet_count": 153,
    "contributors": null,
    "favorite_count": 228,
    "favorited": false,
    "in_reply_to_status_id_str": null,
    "source": "<a href=\"http://twittbot.net/\" rel=\"nofollow\">twittbot.net</a>",
    "in_reply_to_user_id": null,
    "user": {
        "default_profile": false,
        "id_str": "4017736032",
        "profile_background_tile": false,
        "following": false,
        "description": "30+ sec video bot / 30+ 秒 ビデオ bot | Love Live! • Love Live! Sunshine!! • μ's & Aqours seiyuu/声優 | This account no longer accepts requests | ENG only!",
        "name": "30+ sec of ラブライブ!",
        "profile_sidebar_border_color": "000000",
        "entities": {
            "description": {
                "urls": []
            }
        },
        "utc_offset": null,
        "statuses_count": 2821,
        "notifications": false,
        "verified": false,
        "profile_background_image_url_https": "https://abs.twimg.com/images/themes/theme1/bg.png",
        "profile_image_url": "http://pbs.twimg.com/profile_images/751165343968555009/DGbWpedO_normal.jpg",
        "default_profile_image": false,
        "profile_image_url_https": "https://pbs.twimg.com/profile_images/751165343968555009/DGbWpedO_normal.jpg",
        "geo_enabled": false,
        "follow_request_sent": false,
        "is_translation_enabled": false,
        "profile_use_background_image": false,
        "protected": false,
        "favourites_count": 0,
        "url": null,
        "followers_count": 31794,
        "profile_background_image_url": "http://abs.twimg.com/images/themes/theme1/bg.png",
        "profile_link_color": "E81C4F",
        "profile_text_color": "000000",
        "profile_banner_url": "https://pbs.twimg.com/profile_banners/4017736032/1464317692",
        "has_extended_profile": false,
        "is_translator": false,
        "profile_sidebar_fill_color": "000000",
        "created_at": "Sun Oct 25 22:20:47 +0000 2015",
        "contributors_enabled": false,
        "friends_count": 6,
        "id": 4017736032,
        "profile_background_color": "000000",
        "location": "音ノ木坂学院 / 浦の星女学院 ",
        "time_zone": null,
        "screen_name": "30seclovelive",
        "listed_count": 228,
        "lang": "en"
    },
    "place": null,
    "geo": null,
    "truncated": false,
    "in_reply_to_screen_name": null,
    "is_quote_status": false,
    "id": 758454081656467500,
    "text": "movie - hanayo vs. bread #30secLL_bot https://t.co/oQjf1qKsDC",
    "extended_entities": {
        "media": [
            {
                "url": "https://t.co/oQjf1qKsDC",
                "id_str": "680158074653442048",
                "source_status_id": 680158389477875700,
                "source_user_id": 4017736032,
                "source_user_id_str": "4017736032",
                "media_url_https": "https://pbs.twimg.com/ext_tw_video_thumb/680158074653442048/pu/img/UkJ-B_AqbC_vEOcY.jpg",
                "source_status_id_str": "680158389477875712",
                "sizes": {
                    "medium": {
                        "w": 600,
                        "h": 338,
                        "resize": "fit"
                    },
                    "small": {
                        "w": 340,
                        "h": 191,
                        "resize": "fit"
                    },
                    "thumb": {
                        "w": 150,
                        "h": 150,
                        "resize": "crop"
                    },
                    "large": {
                        "w": 1024,
                        "h": 576,
                        "resize": "fit"
                    }
                },
                "display_url": "pic.twitter.com/oQjf1qKsDC",
                "type": "video",
                "id": 680158074653442000,
                "indices": [
                    38,
                    61
                ],
                "additional_media_info": {
                    "monetizable": false,
                    "source_user": {
                        "default_profile": false,
                        "id_str": "4017736032",
                        "profile_background_tile": false,
                        "following": false,
                        "description": "30+ sec video bot / 30+ 秒 ビデオ bot | Love Live! • Love Live! Sunshine!! • μ's & Aqours seiyuu/声優 | This account no longer accepts requests | ENG only!",
                        "name": "30+ sec of ラブライブ!",
                        "profile_sidebar_border_color": "000000",
                        "entities": {
                            "description": {
                                "urls": []
                            }
                        },
                        "utc_offset": null,
                        "statuses_count": 2821,
                        "notifications": false,
                        "verified": false,
                        "profile_background_image_url_https": "https://abs.twimg.com/images/themes/theme1/bg.png",
                        "profile_image_url": "http://pbs.twimg.com/profile_images/751165343968555009/DGbWpedO_normal.jpg",
                        "default_profile_image": false,
                        "profile_image_url_https": "https://pbs.twimg.com/profile_images/751165343968555009/DGbWpedO_normal.jpg",
                        "geo_enabled": false,
                        "follow_request_sent": false,
                        "is_translation_enabled": false,
                        "profile_use_background_image": false,
                        "protected": false,
                        "favourites_count": 0,
                        "url": null,
                        "followers_count": 31794,
                        "profile_background_image_url": "http://abs.twimg.com/images/themes/theme1/bg.png",
                        "profile_link_color": "E81C4F",
                        "profile_text_color": "000000",
                        "profile_banner_url": "https://pbs.twimg.com/profile_banners/4017736032/1464317692",
                        "has_extended_profile": false,
                        "is_translator": false,
                        "profile_sidebar_fill_color": "000000",
                        "created_at": "Sun Oct 25 22:20:47 +0000 2015",
                        "contributors_enabled": false,
                        "friends_count": 6,
                        "id": 4017736032,
                        "profile_background_color": "000000",
                        "location": "音ノ木坂学院 / 浦の星女学院 ",
                        "time_zone": null,
                        "screen_name": "30seclovelive",
                        "listed_count": 228,
                        "lang": "en"
                    }
                },
                "video_info": {
                    "duration_millis": 30000,
                    "variants": [
                        {
                            "url": "https://video.twimg.com/ext_tw_video/680158074653442048/pu/pl/yOBp87ckwBL35I8e.m3u8",
                            "content_type": "application/x-mpegURL"
                        },
                        {
                            "url": "https://video.twimg.com/ext_tw_video/680158074653442048/pu/pl/yOBp87ckwBL35I8e.mpd",
                            "content_type": "application/dash+xml"
                        },
                        {
                            "url": "https://video.twimg.com/ext_tw_video/680158074653442048/pu/vid/1280x720/cZN0XuT_6u12nwak.mp4",
                            "content_type": "video/mp4",
                            "bitrate": 2176000
                        },
                        {
                            "url": "https://video.twimg.com/ext_tw_video/680158074653442048/pu/vid/640x360/-6cs96ywIwtM7-JP.mp4",
                            "content_type": "video/mp4",
                            "bitrate": 832000
                        },
                        {
                            "url": "https://video.twimg.com/ext_tw_video/680158074653442048/pu/vid/320x180/Spqi13GJkXZpU_zv.mp4",
                            "content_type": "video/mp4",
                            "bitrate": 320000
                        }
                    ],
                    "aspect_ratio": [
                        16,
                        9
                    ]
                },
                "expanded_url": "http://twitter.com/30seclovelive/status/680158389477875712/video/1",
                "media_url": "http://pbs.twimg.com/ext_tw_video_thumb/680158074653442048/pu/img/UkJ-B_AqbC_vEOcY.jpg"
            }
        ]
    },
    "lang": "in"
}
'''

