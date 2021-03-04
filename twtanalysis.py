import tweepy
from datetime import datetime
from pprint import pprint
import pandas as pd
import sys
import re
'''
This program is taking in Twitter data, looking for key words, and then presenting their screen name,
the tweet with the key word, and their bio. 

Next steps: figuring out how we can get the pronouns in their bio to be inclusive if they use other
pronouns. Right now, I am testing this out with three twitter accounts that are of two binary trans
people and a non-binary trans person. [done]
I need to see if I can query more than one phrase.
Need to use pandas to place this in a dataframe for neat presentation and analysis.



Other words that incorporate the pronouns, neologisms based on pronouns
    before or after
    word longer than 5 letters including they and them
    
    people started w pronouns in their bios, expanded to create words
to include RT or to not........ maybe track seperately 

Do we want to scrape the tweets and get bios from the tweeters,

tracking pronouns, gender expression words, and thembo etc.  in tweets, looking for correlation
in people who use these wor ds in conjunction to being queer
only looking for people who use pronouns in their bio

do i need to tokenize the words? - not yet

look at levels of proximity, what's considered out group vs in group

comparing amounts of people that use more than two sets of pronouns
i want the specific word
look for new words
Add: 
    
Tweepy is only pulling 100 tweets. Need to figure out a way around this.
https://blog.finxter.com/how-to-match-an-exact-word-in-python-regex-answer-dont/
'''


#creating the authentication object
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
#setting your access token and secret
auth.set_access_token(access_token, access_token_secret)
#creating the API object while passing in auth information
api = tweepy.API(auth)

#account list for people we want to analyze
account_list = ['uwucien','notsumma','flowerhija','annaperng']
#this should be a function
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
 
    
#looks within description, sees pronouns and flags for possible gender marker, reg ex is used to determine each marker
pronouns = 0
    #unsure if each pronoun should have a number attributed to it
#this should be a function
if re.search((r'\bhe\b' or r'\bhim\b'), twt_bio):
            print('! likely masc')
            pronouns = 1            
if re.search((r'\bshe\b' or r'\bher\b'), twt_bio):
             print('! possibily fem')
             pronouns = 1
if re.search((r'\bthey\b' or r'\bthem\b'), twt_bio): #any pronouns, all pronouns
            print("! possibly nb")
            pronouns = 1
if pronouns == 0:  
    #now I need to find if there aren't pronouns in bio
        print("! no pronouns or neopronouns")
        
        #dont need regex to figureout if no pronouns in bio
          #  for i in re.finditer((r'^((?!\bhe\b).)*$' or r'^((?!\bhim\b).)*$' and r'^((?!\bshe\b).)*$' or r'^((?!\bher\b).)*$' or r'^((?!\bthey\b).)*$' or r'^((?!\bthem\b).)*$'), twt_bio):

  #  if re.search((r'\bshe\b' or r'\bher\b'), twt_bio):
   #         print("! Check Pronouns")
     

#pronouns = "she","her","him","his","they","them","bun","xe","xir" #figure out how to list multiple strings
      
#empty list for people who are possibly nonbinary (using that as a general catch all, will elaborate)
pos_nb = []
pos_masc = []
pos_fem = []
no_pronouns = []
#no pronouns, but uses nb or genderqueer
nbgq = []


#terms we want to search for
#i dont want users with this in their screenname, just the tweet
query1 = "thembo"
query2 = "theydie"
query3 = "femboy"
#english language tweets
language = "en"
#can set number of tweets to pull - up to 100
numTweets = 100
#calling the user_timeline function with our parameters
thembo_results = api.search(q=query1, lang=language, count=numTweets)
femboy_results = api.search(q=query2, lang=language, count=numTweets)


#needs to not matter if they use caps or not
#function to search through tweets
#def searchTweet(x): 
for tweet in thembo_results:
        #prints the username, tweet w query, and bio description
        #print(tweet.user.screen_name,"Tweeted:",tweet.text,"| User Description:",tweet.user.description)
        #this searches for they/them
        if re.search((r'\bthey\b' or r'\bthem\b'), tweet.user.description):
            
            pos_nb.append(tweet.user.screen_name)
           
        if re.search((r'\bshe\b' or r'\bher\b'), tweet.user.description):
            pos_fem.append(tweet.user.screen_name)
        if re.search((r'\bhe\b' or r'\bhim\b'), tweet.user.description):
            pos_masc.append(tweet.user.screen_name)
   #people who use words like genderqueer, nb
        if re.search((r'\bnonbinary\b' or r'\bGenderqueer\b'), tweet.user.description):
           nbgq.append(tweet.user.screen_name)
        else:
           for name in (pos_nb and pos_fem and pos_masc):
               if tweet.user.screen_name not in (pos_nb and pos_fem and pos_masc and nbgq):
                   no_pronouns.append(tweet.user.screen_name)
#removes duplicates - list(set(x))
print("Possibly nb:", list(set(pos_nb)), "\nNo pronouns, but possibly nb:", list(set(nbgq)), '\nPossibly fem:',list(set(pos_fem)), "\nPossibly masc:", list(set(pos_masc)), "\nno pronouns:",list(set(no_pronouns)))
    #Track people who use it in their bio
 
total = list(set(pos_fem)) + list(set(pos_nb)) + list(set(pos_masc)) + list(set(no_pronouns))
#percentage of people who do not have pronouns in their bios
print("Percentage of people with no pronouns:", len(set(no_pronouns)) / len(total))
#percentage of people who user she/her
print("Percentage of people with she/her pronouns:", len(set(pos_fem)) / len(total))
#percentage of people who user he/him
print("Percentage of people with he/him pronouns:", len(set(pos_masc)) / len(total))
#percentage of people who user they/them
print("Percentage of people with they/them pronouns:", len(set(pos_nb)) / len(total))
    
    
#searchTweet(thembo_results)

#Track amount of people who use both nb and binary pronouns, right now only tracks 2
he_multiple = []
she_multiple = []
nb = []
tweets = []
multi = 0
#now to compare how many users are multiple lists
for tweet in thembo_results:
    tweets.append(tweet.text)
    if re.search((r'\bthey\b' or r'\bthem\b'), tweet.user.description):
        nb.append(tweet.user.screen_name)
    if re.search((r'\bhe\b' or r'\bhe\b'), tweet.user.description):
        if tweet.user.screen_name in nb:
            he_multiple.append(tweet.user.screen_name)
    if re.search((r'\bshe\b' or r'\bher\b'), tweet.user.description):
        if tweet.user.screen_name in nb:
            she_multiple.append(tweet.user.screen_name)
        
    #print(tweet.user.screen_name,"Tweeted:",tweet.text,"| User Description:",tweet.user.description)          
print("He/they: ", he_multiple)
print("She/they: ", she_multiple)
#percentages of two sets of pronouns
print("Amount of people with both he and they pronouns: ", len(set(he_multiple)) / len(total))
print("Amount of people with both she and they pronouns: ", len(set(she_multiple)) / len(total))

#Print out the percentages of the pronouns/gender identities.

#search for them based neologisms
for tweet in thembo_results:
    if re.search((r'\bthem[a-zA-Z]*'), tweet.text):
        print(tweet.text)

#look at bigrams and tri grams of the words around it


#need to put all the variables in a dataframe
data = {"tweets" : [], 
        'screen_name' : []}


for t in thembo_results:
    data['tweets'].append(t['tweets'])
    data['screen_name'].append(t['screen_name'])
    
df = pd.DataFrame(data)
   #     {'tweets': [tweets],
    #     'screen_name': [tweet.user.screen_name],
     #    'description': [tweet.user.description]
      #   })

print(df)
#display this data in matplot (bar graphs, pie chart)
''' 
in my dataframe i want:
    title is: which search results they appeared from
    tweet (to tokenize for ngrams)
    user.screen_name
    user.description
    their pronouns
    if they use two sets of pronouns
    
'''
