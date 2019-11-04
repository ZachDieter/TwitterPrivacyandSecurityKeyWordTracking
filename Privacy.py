#Sources:
#   1) Used the "Twitter API with Python" youtube tutorials to help write my code
#   2) https://stackoverflow.com/questions/26890605/filter-twitter-feeds-only-by-language

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import json

APIKey = "QMxJRubfz0QT1HUclrI689YER"
APISECRETKey = "asr2WDm572Rjcqrc7TeeEZOZaXCcTJmueUyF0X1wHWrX9NyVKL"
ACCESSToken = "1083509663512043520-QCkLv3nZkNbHGzKsFeqBNxrTi5KKW8"
ACCESSTOKENSECRET = "baePC6AiSM5e79ugWvYw5zRl5uizR8hi7kylO72uUUJJR"

keywords = ["VPN", "ProtonVPN", "NordVPN", "IP", "StartPage", "FireFox", "Cookies", "Trackers", "Google" 
, "DuckDuckGo", "Amazon", "2FA", "MFA", "Tracking me", "My Privacy", "My Data", "Access to my Data"]

wordCloud = {}
users = {}
tweets ={}

def check(sentence, words): 
    for i in words:
        for j in sentence:
            if(i == j):
                return i
    return -1

def checkForWord(word):
    if(word != -1):
        if(word in wordCloud):
            wordCloud[word] += 1
        else:
            wordCloud[word] = 1

def unqiueTweet(tweet):
    if(tweet in tweets):
        tweets[tweet] += 1
    else:
        tweets[tweet] = 1

def removeStopWords(tweet):
    stop_words = set(stopwords.words('english')) 
    filtered_sentence = [w for w in tweet if not w in stop_words] 
    filtered_sentence = [] 
    for w in tweet: 
        if w not in stop_words: 
            filtered_sentence.append(w) 
    return filtered_sentence

class tweetListener(StreamListener):

    def on_data(self, data):
        try:
            tweet = json.loads(data)
            #tweetUser = tweet['screen_name']
            tweetTextList = removeStopWords(tweet['text'].split(" "))
            checkForWord(check(tweetTextList, keywords))
            return True
        except:
            print("Something failed")
            with open("P5.txt", 'w+') as f:
                f.write(json.dumps(wordCloud))
            return False
    def on_error(self, status):
        print(status)
        


def createStream():
    listener = tweetListener()
    auth = OAuthHandler(APIKey, APISECRETKey)
    auth.set_access_token(ACCESSToken, ACCESSTOKENSECRET)
    stream = Stream(auth,listener)
    return stream

def main():
    twitterStream = createStream()
    try:
        twitterStream.filter(languages=['en'], track=keywords)
    except(KeyboardInterrupt, SystemExit):
        print("ctr c pressed")
        with open("P5.txt", 'w+') as f:
            f.write(json.dumps(wordCloud))


if __name__ == "__main__":
    main()
