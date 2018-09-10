import json
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

# NOT WORKING...

#Enter Twitter API Key information
consumer_key = 'dWSksJ98HCFhBA8SCc9qsiTCv'
consumer_secret = 'BrZIrJ8VMWh40sqI7bKgdPpuPWEXdq4OnVKjol9FSOHNx9JHYS'
access_token = '399258420-0DQdayCWBMUjAMbUCRSBemHPgFm3A6DbMolUQGmi'
access_secret = 'k9eCGx6QPnU8yFrghsG5xE8RWsOoMtSejhj1kUsTKcItz'

file = open("flood-coords.csv", "w")
file.write("X,Y\n")

data_list = []
count = 0

class listener(StreamListener):

    def on_data(self, data):
        global count

        #How many tweets you want to find, could change to time based
        if count <= 2000:
            json_data = json.loads(data)

            coords = json_data["coordinates"]
            if coords is not None:
               print coords["coordinates"]
               lon = coords["coordinates"][0]
               lat = coords["coordinates"][1]

               data_list.append(json_data)

               file.write(str(lon) + ",")
               file.write(str(lat) + "\n")

               count += 1
            return True
        else:
            file.close()
            return False

    def on_error(self, status):
        print status

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
twitterStream = Stream(auth, listener())
#What you want to search for here
twitterStream.filter(track=["flood"])
