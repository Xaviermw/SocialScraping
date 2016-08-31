
# coding: utf-8

# In[39]:

#Scrapes the Twitter API, looking for certain words and write to a file the occurences of these words
#the occurences of these words in the last 50 15 second increments

#Used to Authenticate with Twitter API
import oauth2 as oauth

#Used for basic HTTP Requesting
import urllib.request as urllib

#Converts twitter JSON into dictionaries
import json

#Used to calculate time increments
from datetime import datetime, timedelta

#Imports keywords to look for in twitter feed
tList = open('terrorismKeywords.txt', 'r')
combined = tList.read()
indWords = combined.split(", ")

#Twitter API info and key
api_key = "Hf1NgnH1NvMc8mQpAy6WFDFtE"
api_secret = "yKwAEsTMtCeHQQck3gtVyyFojtbpypPfJvV0FBdD9sWODh72kg"
access_token_key = "799378974-QaAc9CQvmr8Hhn5wlJNeAchAtIfk4l3pxd6qOHSy"
access_token_secret = "RHpiEOoy2qOl4Gp1Kp6FROKDVfD3IkD1bEZBYoSy2negv"

#idk what this does I just copied it with other stuff
_debug = 0

#Combines authentication information
oauth_token    = oauth.Token(key=access_token_key, secret=access_token_secret)
oauth_consumer = oauth.Consumer(key=api_key, secret=api_secret)
signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()

#Scraping Data
http_method = "GET"
http_handler  = urllib.HTTPHandler(debuglevel=_debug)
https_handler = urllib.HTTPSHandler(debuglevel=_debug)


#Twitter Request
def twitterreq(url, method, parameters):
    req = oauth.Request.from_consumer_and_token(oauth_consumer,
                                             token=oauth_token,
                                             http_method=http_method,
                                             http_url=url, 
                                             parameters=parameters)

    req.sign_request(signature_method_hmac_sha1, oauth_consumer, oauth_token)

    headers = req.to_header()

    if http_method == "POST":
        encoded_post_data = req.to_postdata()
    else:
        encoded_post_data = None
        url = req.to_url()
        opener = urllib.OpenerDirector()
        opener.add_handler(http_handler)
        opener.add_handler(https_handler)

    response = opener.open(url, encoded_post_data)

    return response

def fetchsamples():
    
    #Gets twitter request and response
    url = "https://stream.twitter.com/1.1/statuses/sample.json"
    parameters = []
    response = twitterreq(url, "GET", parameters)
    
    #Last 50 Increments
    history = [0]*50
    
    #Count for Current Increment
    counter = 0
    
    #Establishes period for increments, starts first increment
    period = timedelta(seconds = 15)
    startTime = datetime.now()
    nextTime = datetime.now() + period
    
    
    
    for line in response:
        
        #Opens file to make sure to keep running
        f = open('run.txt', 'r')
        if (f.read() != 'yes'):
            break
        
        #Checks if increment is done, if so posts and updates history
        if (datetime.now() >= nextTime):
            history = dataWriter(counter, history)
            counter = 0
            startTime = datetime.now()
            nextTime = datetime.now() + period
            
        #Loads JSON input into dictionary, decode needed for string values
        x = json.loads(line.decode())
        
        #Try finds if data element is a normal tweet that contains text, if not skips it
        try:
            
            #Gets individual tweet, initialize keyword to not finding any
            tweet = (x['text'])
            found = False
            
            #Checks each word in our keywords
            for word in indWords:
                
                #If a word is found counter for the period is increased, and we set found to true
                if (word in tweet and not found):
                    counter = counter + 1
                    found = True
        
        #Gets general exceptions, could be more precise
        except BaseException:
            pass
        
#Uodates the historical amounts, and writes them to a file
def dataWriter(count, hist):
    
    #Moves every element back 1
    for x in range (49, 0, -1):
        hist[x] = hist[x-1]
    
    #Puts current period count in first spot
    hist[0] = count
    
    #Open and clears the old historical data
    f = open('histoData.txt', 'w')
    f.truncate()
    
    #Writes the new historical data
    for y in range (0, 50):
        f.write(str(hist[y]) + "\n")
                
    #Returns updated historical data
    return hist
        
        
#Runs the program
if __name__ == '__main__':
    fetchsamples()

