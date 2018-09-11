#!/usr/bin/python
import tweepy
import csv 

consumer_key = 'dWSksJ98HCFhBA8SCc9qsiTCv'  
consumer_secret = 'BrZIrJ8VMWh40sqI7bKgdPpuPWEXdq4OnVKjol9FSOHNx9JHYS'  
access_token = '399258420-0DQdayCWBMUjAMbUCRSBemHPgFm3A6DbMolUQGmi'  
access_token_secret = 'k9eCGx6QPnU8yFrghsG5xE8RWsOoMtSejhj1kUsTKcItz' 


# OAuth process, using the keys and tokens  
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)  
auth.set_access_token(access_token, access_token_secret) 
api = tweepy.API(auth)

# Only iterate through the first 200 statuses
for status in tweepy.Cursor(api.user_timeline, id="abhisekyuvraj").items(200):
    print status 
