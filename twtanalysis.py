import tweepy
from datetime import datetime
from pprint import pprint
from pandas import DataFrame as df
import sys
'''
This program is taking in Twitter data, looking for key words, and then presenting their screen name,
the tweet with the key word, and their bio. 

Next steps: figuring out how we can get the pronouns in their bio to be inclusive if they use other
pronouns. Right now, I am testing this out with three twitter accounts that are of two binary trans
people and a non-binary trans person.
I need to see if I can query more than one phrase.
Need to use pandas to place this in a dataframe for neat presentation and analysis.
'''

consumer_key = "4OTRrIDSPFnWHZqNEprsIRHGu"
consumer_secret = "Ls89ANMIs0nuELYyOe2RdMzVOM6xoNfY8BYfjSlsx2VAdhe4Us"
access_token = "1066552856-WpKelzP4cA0LjxX8uJ8ooPDLq3uBLbMAaWVOMI0"
access_token_secret = "HpSZ522nR1D9nE3HQVWxwugEdIxAZ8C8SLzVmbC69WSLK"

#creating the authentication object
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
#setting your access token and secret
auth.set_access_token(access_token, access_token_secret)
#creating the API object while passing in auth information
api = tweepy.API(auth)

#account list for people we want to analyze
account_list = ['uwucien','notsumma','flowerhija']

if len(account_list) > 0:
  for target in account_list:
    item = api.get_user(target)
    twt_bio = item.description
    print("Getting data for " + target)
    print("name: " + item.name)
    print("screen_name: " + item.screen_name)
    print("location: " + item.location)
    print("description: " + item.description)
    print("statuses_count: " + str(item.statuses_count))
    #looks within description, sees pronouns and flags for possible gender markers
    if 'he/him' in twt_bio:
        print('! likely masc')
    elif 'she' in twt_bio:
        print('! possibily fem')
    elif 'they' in twt_bio:
        print("! possibly nb")
    else:
        print("neopronouns? manually check the pronouns.")
#empty list for people who are possibly nonbinary (using that as a general catch all, will elaborate)
pos_nb = []

#terms we want to search for
query = "thembos"
#english language tweets
language = "en"
#can set number of tweets to pull
numTweets = 30
#calling the user_timeline function wi our parameters
results = api.search(q=query, lang=language, count=numTweets)
#for each through all tweets pulled
for tweet in results:
   #prints the username, tweet w query, and bio description
   print(tweet.user.screen_name,"Tweeted:",tweet.text,"| User Description:",tweet.user.description)
   if 'they/them' in tweet.user.description:
       pos_nb.append(tweet.user.screen_name)
#this does not currently catch people who use multiple pronouns
print(pos_nb)