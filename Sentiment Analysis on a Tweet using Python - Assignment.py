"""
Title: Sentiment Analysis by comparing the positive and negative words from a scrapped Tweet using Python

author: arvind
"""
# pip install tweepy
# pip install folium

import tweepy
import csv
import folium
import nltk


# setTerms = ['enter', 'your', 'search', 'terms', 'here'] 
setLang = ['en']

# location of the output file...
logFile = 'tmp.txt'
fileOut = open(logFile, "w")

# map of tweet locations
mapFile = 'osm.html'
map_osm = folium.Map(location=[45.372, -121.6972], zoom_start=2)



# Import +/- Words
posWords = []
negWords = []
with open('positive-words.txt', 'r') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
	for row in spamreader:
		if (row[0][0] != '%'):
			posWords.append(str(row[0]))

with open('negative-words.txt', 'r') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
	for row in spamreader:
		if (row[0][0] != '%'):
			negWords.append(str(row[0]))
			
# https://dev.twitter.com/overview/api/entities-in-twitter-objects
class StreamListener(tweepy.StreamListener):		
	def on_status(self,tweet):
		
		# Define Global Variables
		global numPos
		global numNeg
		global tweetWords

		# print tweet details:
		print(tweet.text)		
		'''
		print(tweet.geo)
		print(tweet.user.geo_enabled)
		print(tweet.user.location)
		
		print(tweet.created_at)
		print(tweet.id)
		print(tweet.geo)
		print(tweet.author.screen_name)
		print(tweet.source)
		print(tweet.place)
		#print(tweet.place['bounding_box'])
		print(tweet.user.geo_enabled)
		print(tweet.user.time_zone)
		print(tweet.user.location)
		'''		print tweet.coordinates

		# Splitting the tweet text into separate words
		myList = tweet.text.split()
		# myList = ['here', 'is', 'some', 'text']
		
		# Initializing some dummy counter variables:
		tmpPos = 0
		tmpNeg = 0
		
		# Loop over each word:
		for myWord in myList:
			# Convert each word to lower case:
			# Also, encode as utf-8
			myWord = myWord.encode('utf-8').lower()
			tweetWords.append(myWord)
			
			# For each word, see if it's positive or negative:
			if (myWord in posWords):
				tmpPos += 1
				numPos += 1
				print("found positive")
			if (myWord in negWords):
				tmpNeg += 1
				numNeg += 1
				print("found negative")
	
		# If the tweet contains GPS coordinates, placing a pin on the coordianted on map:
		if (tweet.coordinates != None):
			myLon = tweet.coordinates['coordinates'][0]		
			myLat = tweet.coordinates['coordinates'][1]	
			print("\t User at (%f,%f) -- %s" % (myLat, myLon, tweet.user.location))

			# Adding a pin to the map, color-coded based on sentiment
			if (tmpPos > tmpNeg):
				pinColor = 'green'
			elif (tmpPos < tmpNeg):
				pinColor = 'red'
			else:
				pinColor = 'blue'
				
			folium.Marker([myLat,myLon], icon = folium.Icon(color = pinColor), popup = tweet.text).add_to(map_osm)
			
			
		# saving info to the text file
		fileOut.write(str(tweet.text.encode('utf-8')) + "+" + str(tweet.created_at) + "+" + str(tweet.id) + "+" + str(tweet.geo) + "+" + str(setTerms) +  "\n")
	

class main_loop():
	def __init__(self):

		print("Starting the code")
				
		# http://dev.twitter.com and create an app. 
		# The consumer key and secret will be generated 
		consumer_key 	= 'lXZLrscZivh0OI9g8P0jAYAG2'		# <--- key
		consumer_secret	= '1HUieiYCXtE3cdjuccbX1Jo2NXguWBA7LuNWvk6pmXlpGxU94I'		# <--- secret 
		
		
		# Creating an access token 
		access_token 		= '1118147812305326082-pj6cE4lSeGWodVtuLiawt0kKkBBoXf'		# <---  token 
		access_token_secret = 'LiufawsDzUSsZxQWWKsnvV1XcRQsrwnrNGUcZpinPH18H'		# <--- token secret
		
		auth1 = tweepy.OAuthHandler(consumer_key, consumer_secret)
		auth1.set_access_token(access_token, access_token_secret)
		print("Access Code Validation a Success")

		l = StreamListener()
		streamer = tweepy.Stream(auth=auth1, listener=l)
		streamer.filter(track = setTerms, languages = setLang)
	

if __name__ == '__main__':
	try:
		numPos = 0
		numNeg = 0
		tweetWords = []
		main_loop()
	except KeyboardInterrupt:
		print("\nKeyboard Interrupt")
		fileOut.close()
		map_osm.save(mapFile)
		print("See %s and %s" % (mapFile, logFile))
		
		print("\nFound %d Positive words and %d Negative words" % (numPos, numNeg))
			
		# NLTK
		fdist = nltk.FreqDist(tweetWords)
		print("Frequency Distribution:")
		print(fdist.most_common(20))
		
		print("Bigrams:")
		myBigrams = list(nltk.bigrams(tweetWords))
		fdist = nltk.FreqDist(myBigrams)
		print(fdist.most_common(20))