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
people and a non-binary trans person. [done]
I need to see if I can query more than one phrase.
Need to use pandas to place this in a dataframe for neat presentation and analysis.

Print out the percentages of the pronouns/gender identities. 
Track amount of people who use both nb and binary pronouns
Track people who use it in their bio [done]

Other words that incorporate the pronouns, neologisms based on pronouns
    before or after
    word longer than 5 letters including they and them
    
    people started w pronouns in their bios, expanded to create words
to include RT or to not........ maybe track seperately 

Do we want to scrape the tweets and get bios from the tweeters, or have specific account bios and 
read their tweets

Add: 
'''



#creating the authentication object
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
#setting your access token and secret
auth.set_access_token(access_token, access_token_secret)
#creating the API object while passing in auth information
api = tweepy.API(auth)

#account list for people we want to analyze
account_list = ['uwucien','notsumma','flowerhija']
#this should be a function
#make a list that contains pronoun type
nb_pronouns = ['they', ]
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
    #looks within description, sees pronouns and flags for possible gender marker


    if "him" in twt_bio:
        print('! likely masc')
    elif "her" in twt_bio:
        print('! possibily fem')
    elif "they" in twt_bio: #any pronouns, all pronouns
        print("! possibly nb")
    else:
        print("! Check Pronouns")
#pronouns = "she","her","him","his","they","them","bun","xe","xir" #figure out how to list multiple strings
      
#empty list for people who are possibly nonbinary (using that as a general catch all, will elaborate)
pos_nb = []

#terms we want to search for
query = "thembo"
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
   if 'they' in tweet.user.description:
       pos_nb.append(tweet.user.screen_name)
#this does not currently catch people who use multiple pronouns
print(pos_nb)

counter = 0
for tweet in results:
    if '/' in tweet.user.description:
        counter += 1
print(round((counter/(numTweets)),2))

#if the same person tweets, it records them seperately, so make sure to ask for distinct values
import re
regex = re.compile('them.')
matches = [string for string in tweet.text if re.match(regex, string)]
print(matches)

for tweet in results:
    if 'thembo' in tweet.text:
        print(tweet.text)
'''
    neologism = re.search('^them', tweet.text)
print(neologism)
'''