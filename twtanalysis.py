import tweepy
from datetime import datetime
from pprint import pprint
from pandas import DataFrame as df
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
in people who use these words in conjunction to being queer
only looking for people who use pronouns in their bio

do i need to tokenize the words? - not yet

look at levels of proximity, what's considered out group vs in group

comparing amounts of people that use more than two sets of pronouns
i want the specific word
look for new words
Add: 
    
Tweepy is only pulling 100 tweets. Need to figure out a way around this.
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


#terms we want to search for
#i dont want users with this in their screenname, just the tweet
query = "thembo"
#english language tweets
language = "en"
#can set number of tweets to pull - up to 100
numTweets = 100
#calling the user_timeline function with our parameters
results = api.search(q=query, lang=language, count=numTweets)



#for each through all tweets pulled
for tweet in results:
   #prints the username, tweet w query, and bio description
   print(tweet.user.screen_name,"Tweeted:",tweet.text,"| User Description:",tweet.user.description)
   if re.search((r'\bthey\b' or r'\bthem\b'), tweet.user.description):
       pos_nb.append(tweet.user.screen_name)
   if re.search((r'\bshe\b' or r'\bher\b'), tweet.user.description):
       pos_fem.append(tweet.user.screen_name)
   if re.search((r'\bhe\b' or r'\bhim\b'), tweet.user.description):
       pos_masc.append(tweet.user.screen_name)
   else:
       for name in (pos_nb and pos_fem and pos_masc):
           if tweet.user.screen_name not in (pos_nb and pos_fem and pos_masc):
               no_pronouns.append(tweet.user.screen_name)
#this does not currently catch people who use multiple pronouns
#removes duplicates - list(set(x))
print("Possibly nb:", list(set(pos_nb)), '\nPossibly fem:',list(set(pos_fem)), "\nPossibly masc:", list(set(pos_masc)), "\nno pronouns:",list(set(no_pronouns)))

#people who use words like genderqueer, nb

#Track people who use it in their bio
total = list(set(pos_fem)) + list(set(pos_nb)) + list(set(pos_masc)) + list(set(no_pronouns))
#percentage of people who do not have pronouns in their bios
print(len(set(no_pronouns)) / len(total))


#Track amount of people who use both nb and binary pronouns BROKEN
multiple = []
#now to compare how many users are multiple lists
for name in pos_nb:
    if tweet.user.screen_name in pos_fem:
        if tweet.user.screen_name in pos_nb:
            multiple.append(tweet.user.screen_name)
    #elif tweet.user.screen_name in (pos_nb and pos_masc):
     #   multiple.append(tweet.user.screen_name)
#print("Users that have more than one set of pronouns: ", multiple)

#Print out the percentages of the pronouns/gender identities. 

#look at bigrams and tri grams of the words around it

#search for neologisms
'''
regex = re.compile('them.')
matches = [string for string in tweet.text if re.match(regex, string)]
print(matches)

for tweet in results:
    if 'thembo' in tweet.text:
        print(tweet.text)

    neologism = re.finditer(r"\w+them", tweet.text)
print(neologism)
'''