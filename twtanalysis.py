import tweepy
from datetime import datetime
from pprint import pprint
import pandas as pd
import sys
import re
import matplotlib.pyplot as plt
from nltk.corpus import twitter_samples
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import twitter_samples, stopwords, movie_reviews
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from nltk import FreqDist, classify, NaiveBayesClassifier

import re, string, random
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier


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

scrape the tweets and get bios from the tweeters

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
'''
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

            
            #xe/xir
            #it/its
            #he/they,she/theys
         
            
if pronouns == 0:  
    #now I need to find if there aren't pronouns in bio
        print("! no pronouns or neopronouns")
        
        #dont need regex to figureout if no pronouns in bio
          #  for i in re.finditer((r'^((?!\bhe\b).)*$' or r'^((?!\bhim\b).)*$' and r'^((?!\bshe\b).)*$' or r'^((?!\bher\b).)*$' or r'^((?!\bthey\b).)*$' or r'^((?!\bthem\b).)*$'), twt_bio):

  #  if re.search((r'\bshe\b' or r'\bher\b'), twt_bio):
   #         print("! Check Pronouns")
'''     

#pronouns = "she","her","him","his","they","them","bun","xe","xir" #figure out how to list multiple strings
      
#empty list for people who are possibly nonbinary (using that as a general catch all, will elaborate)
pro_they = []
pro_he = []
pro_she = []
pro_it = []
pro_xe = []
pro_ze = []
no_pronouns = []
authors = []
#no pronouns, but uses nb or genderqueer
nbgq = []
tweets = []

#terms we want to search for
#i dont want users with this in their screenname, just the tweet
query1 = "thembo"
query2 = "theydie"
query3 = "femboy"
query4 = "gentlethem"
query5 = "gays"
query6 = "gaydie"
query7 = "they/thems"
query8 = "girls, gays, and theys"
query9 = "theybie"
query10 = "himbo"
query11 = "bimbo"
query12 = "xembo"
#english language tweets
language = "en"
#can set number of tweets to pull - up to 100
numTweets = 100
#calling the user_timeline function with our parameters
thembo_res = api.search(q=query1, lang=language, count=numTweets)
theydies_res = api.search(q=query2, lang=language, count=numTweets)
femboy_res = api.search(q=query3, lang=language, count=numTweets)
gentlethem_res = api.search(q=query4, lang=language, count=numTweets)
gays_res = api.search(q=query5, lang=language, count=numTweets)
gaydies_res = api.search(q=query6, lang=language, count=numTweets)
theythems_res = api.search(q=query7, lang=language, count=numTweets)
phrase1_res = api.search(q=query8, lang=language, count=numTweets)
theybie_res = api.search(q=query9, lang=language, count=numTweets)
himbo_res = api.search(q=query10, lang=language, count=numTweets)
bimbo_res = api.search(q=query11, lang=language, count=numTweets)
xembo_res = api.search(q=query12, lang=language, count=numTweets)



#needs to not matter if they use caps or not
#function to search through tweets
#def searchTweet(x): 
for tweet in theydies_res:
        #prints the username, tweet w query, and bio description
        tweets.append(tweet.text)
        #print(tweet.user.screen_name,"Tweeted:",tweet.text,"| User Description:",tweet.user.description)
        authors.append(tweet.user.screen_name)
        #this searches for they/them
        if re.search((r'\bthey\b' or r'\bthem\b'), tweet.user.description, re.IGNORECASE):
            pro_they.append(tweet.user.screen_name) #searches for they/them
        if re.search((r'\bshe\b' or r'\bher\b'), tweet.user.description, re.IGNORECASE):
            pro_she.append(tweet.user.screen_name)
        if re.search((r'\bhe\b' or r'\bhim\b'), tweet.user.description, re.IGNORECASE):
            pro_he.append(tweet.user.screen_name)
        if re.search((r'\bit\b' or r'\bits\b'), tweet.user.description, re.IGNORECASE):
            pro_it.append(tweet.user.screen_name)
        if re.search((r'\bxe\b' or r'\bxir\b' or r'\bxem\b' or r'\bxey\b'), tweet.user.description, re.IGNORECASE):
            pro_xe.append(tweet.user.screen_name)
        if re.search((r'\bze\b' or r'\bzir\b' or r'\bzem\b'), tweet.user.description, re.IGNORECASE):
            pro_ze.append(tweet.user.screen_name)
            #de,dem
   #people who use words like genderqueer, nb
        if re.search((r'\bnonbinary\b' or r'\bgenderqueer\b'), tweet.user.description, re.IGNORECASE):
           nbgq.append(tweet.user.screen_name)
#list of usernames
pro = pro_ze + pro_xe + pro_it + pro_he + pro_she + pro_they
set(pro)
for tweet in theydies_res:
    if tweet.user.screen_name not in pro:
        no_pronouns.append(tweet.user.screen_name)
print("length of set of pro: ", len(set(pro)))
#print(set(pro))
print(set(no_pronouns))

         
         #   
         #   print("num of tweets w no pro: ", len(tweet.text))
#print("if statement version: ", len(set(no_pronouns)))


#removes duplicates - list(set(x))
#nopronouns = (len(set(pro_they))+len(set(pro_he))+len(set(pro_she))+len(set(pro_xe))+len(set(pro_ze))+len(set(pro_it))) - (len(set(pro)))


#print("They/them:", list(set(pro_they)), '\nShe/her: ',list(set(pro_she)), "\nHe/him: ", list(set(pro_he)), "\nno pronouns:",nopronouns, "\nit: ", list(set(pro_it)), "\nxe: ", list(set(pro_xe)), "\nze: ", list(set(pro_ze)))
#print("People with no pronouns is:", nopronouns)


   #Track people who use it in their bio
 
    #search for neologisms within tweet
    #csv - data recording


'''
if tweet.user.screen_name in nbgq:
    print(tweet.user.screen_name, tweet.user.description)
print("nbgq:", len(nbgq))
print("nb:", len(pro_they))
'''
   
#searchTweet(thembo_results)

#Track amount of people who use both nb and binary pronouns, right now only tracks 2
he_they = []
she_they = []
nb = []
tweets = []
multi = 0
screennames = []
#now to compare how many users are multiple lists
#two sets of pronouns are still being counted in they, they need to be removed from the original list
for tweet in theydies_res:
    screennames.append(tweet.user.screen_name)
    if re.search((r'\bthey\b' or r'\bthem\b'), tweet.user.description, re.IGNORECASE):
        nb.append(tweet.user.screen_name)
    if re.search((r'\bhe\b' or r'\bhe\b'), tweet.user.description, re.IGNORECASE):
        if tweet.user.screen_name in nb:
            he_they.append(tweet.user.screen_name)
    if re.search((r'\bshe\b' or r'\bher\b'), tweet.user.description, re.IGNORECASE):
        if tweet.user.screen_name in nb:
            she_they.append(tweet.user.screen_name)
    #need to code for if someone is in both categories
'''   
#total = len(set(pro_they)) + len(set(pro_she))+ len(set(pro_he)) + nopronouns + len(set(pro_it)) + len(set(pro_xe))+ len(set(pro_ze)) +len(set(he_they)) + len(set(she_they))
#percentage of people who do not have pronouns in their bios
#print("Percentage of people with no pronouns:", nopronouns / total)
#percentage of people who use she/her
print("Total number of pronoun users: ", len(set(pro)))
print("Percentage of people with she/her pronouns:", len(set(pro_she)) / len(set(pro)))
print("Number of people with she/her: ", len(set(pro_she)))
#percentage of people who use he/him
print("Percentage of people with he/him pronouns:", len(set(pro_he)) / len(set(pro)))
print("Number of people with he/him: ", len(set(pro_he)))
#percentage of people who use they/them
print("Percentage of people with they/them pronouns:", len(set(pro_they)) / len(set(pro)))
print("Number of people with they/them: ", len(set(pro_they)))
#percentage of people who use they/them
print("Percentage of people with it/its pronouns:", len(set(pro_it)) / len(set(pro)))
print("Number of people with it/its: ", len(set(pro_it)))
#percentage of people who use they/them
print("Percentage of people with xe/xir pronouns:", len(set(pro_xe)) / len(set(pro)))
print("Number of people with xe/xir: ", len(set(pro_xe)))
#percentage of people who use they/them
#print("Percentage of people with ze/zir pronouns:", len(set(pro_ze)) / len(set(pro))) 
#print("Number of people with ze/him: ", len(set(pro_he)))
#percentage of people who use he/they
print("Amount of people with both he and they pronouns: ", len(set(he_they)) / len(set(pro)))
print("Number of people with both he and they pronouns: ", len(set(he_they))) 
#percentage of people who use she/they
print("Amount of people with both she and they pronouns: ", len(set(she_they)) / len(set(pro)))
print("Number of people with both she and they pronouns: ", len(set(she_they))) 
      
    #print(tweet.user.screen_name,"Tweeted:",tweet.text,"| User Description:",tweet.user.description)          
#print("He/they: ", list(set(he_they)))
#print("She/they: ", list(set(she_they)))

#percentages of two sets of pronouns


#graph of thembo to theydie screen name ratio
#graph of thembo to theydie name (like display name) ratio

labels = ["she/her","they/them", 'he/him', 'it/its','xe/xem','he/they','she/they']
sizes = [(len(set(pro_she)) / len(set(pro))),(len(set(pro_they)) / len(set(pro))), (len(set(pro_he)) / len(set(pro))),(len(set(pro_it)) / len(set(pro))),(len(set(pro_xe)) / len(set(pro))),(len(set(he_they)) / len(set(pro))), (len(set(she_they)) / len(set(pro)))]
plt.pie(sizes, labels=labels,explode= (0.01,0.01,0.01,0.01,0.01,0.01,0.01,), autopct='%1.1f%%')
plt.axis('equal')
plt.show()

'''
import time

# Create empty dataframe
user_features_list = ["screen_name", "name", "location", "bio",
                      "he/him", "she/her", "they/them",
                      "it/its", "xe/xem", "ze/zir"]
# features such as "he/him", etc. and "theybie", etc. can or could be represented by 1s and 0s (or Yes's and No's if you prefer)
# You could also just have a column called "pronouns" and have it be an array (with 0 or more elements) of what pronouns are in a bio
# just my two cents though, take whatever you wanna use!

#need to remove duplicates
users_df = pd.DataFrame(columns = user_features_list)

# account list for people we want to analyze
account_list = ['uwucien','notsumma','flowerhija','annaperng']

# Loop through each user in the list of users, extract features and append the features to users_df
for user in screennames:
    # Create empty dict
    user_features = {}
    # Get user data
    if user in pro:
        item = api.get_user(user)
        user_features['bio'] = item.description
        user_features['screen_name'] = item.screen_name
        user_features['name'] = item.name
        user_features['location'] = item.location
        user_features['bio'] = item.description
        #fills in the yeses
        if user in pro_they:
            user_features['they/them'] = 'yes'
        if user in pro_he:
            user_features['he/him'] = 'yes'
        if user in pro_she:
            user_features['she/her'] = 'yes'
        if user in pro_it:
            user_features['it/its'] = 'yes'
        if user in pro_xe:
            user_features['xe/xem'] = 'yes'
        if user in pro_ze:
            user_features['ze/zem'] = 'yes'
        #fills in the nos
        if user not in pro_he:
            user_features['he/him'] = 'no'
        if user not in pro_she:
            user_features['she/her'] = 'no'
        if user not in pro_xe:
            user_features['xe/xem'] = 'no'
        if user not in pro_they:
            user_features['they/them'] = 'no'
        if user not in pro_it:
            user_features['it/its'] = 'no'
        if user not in pro_ze:
            user_features['ze/zir'] = 'no'
        
    # Concat the dfs
    user = pd.DataFrame(user_features, index = [0])
    users_df = pd.concat([users_df, user], ignore_index = True)
    # Sleep for 5 seconds to avoid rate-limiting
    # Number of seconds can be tweaked as needed (through trial and error)
    #time.sleep(5)
    
users_df.dropna(subset=["screen_name"], inplace=True)
users_df.to_csv('theydies_415.csv', encoding='utf-8', index=False)



'''plt.hist(multi, bins = 30)
plt.title("Amount of pronouns")
plt.xlabel("Number of Hosts with Multiple Listings")
plt.ylabel("Frequency")
plt.show()

#Print out the percentages of the pronouns/gender identities.

#search for them based neologisms
for tweet in theythems_res:
    if re.search((r'\bboy[a-zA-Z]*'), tweet.text):
       print(tweet.text)
#tokenize without dataframe?

#graphs - bar graph will better illustrate overlapping pronouns

#look at bigrams and tri grams of the words around it

#perhaps we need sentiment analysis of these words


#need to put all the variables in a dataframe
data = {"tweets" : [], 
        'screen_name' : []}


for t in thembo_results:
    data['tweets'].append(t['tweets'])
    data['screen_name'].append(t['screen_name'])
    
#df = pd.DataFrame(data)
   #     {'tweets': [tweets],
    #     'screen_name': [tweet.user.screen_name],
     #    'description': [tweet.user.description]
      #   })

#print(df)
#display this data in matplot (bar graphs, pie chart)

in my dataframe i want:
    title is: which search results they appeared from
    tweet (to tokenize for ngrams)
    user.screen_name
    user.description
    their pronouns
    if they use two sets of pronouns
    

def remove_noise(tweet_tokens, stop_words = ()):

    cleaned_tokens = []

    for token, tag in pos_tag(tweet_tokens):
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)
        token = re.sub("(@[A-Za-z0-9_]+)","", token)

        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'

        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)

        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            cleaned_tokens.append(token.lower())
    return cleaned_tokens

def get_all_words(cleaned_tokens_list):
    for tokens in cleaned_tokens_list:
        for token in tokens:
            yield token

def get_tweets_for_model(cleaned_tokens_list):
    for tweet_tokens in cleaned_tokens_list:
        yield dict([token, True] for token in tweet_tokens)

if __name__ == "__main__":

    positive_tweets = twitter_samples.strings('positive_tweets.json')
    negative_tweets = twitter_samples.strings('negative_tweets.json')
    text = twitter_samples.strings('tweets.20150430-223406.json')
    tweet_tokens = twitter_samples.tokenized('positive_tweets.json')[0]

    stop_words = stopwords.words('english')

    positive_tweet_tokens = twitter_samples.tokenized('positive_tweets.json')
    negative_tweet_tokens = twitter_samples.tokenized('negative_tweets.json')

    positive_cleaned_tokens_list = []
    negative_cleaned_tokens_list = []

    for tokens in positive_tweet_tokens:
        positive_cleaned_tokens_list.append(remove_noise(tokens, stop_words))

    for tokens in negative_tweet_tokens:
        negative_cleaned_tokens_list.append(remove_noise(tokens, stop_words))

    all_pos_words = get_all_words(positive_cleaned_tokens_list)

    freq_dist_pos = FreqDist(all_pos_words)
    print(freq_dist_pos.most_common(10))

    positive_tokens_for_model = get_tweets_for_model(positive_cleaned_tokens_list)
    negative_tokens_for_model = get_tweets_for_model(negative_cleaned_tokens_list)

    positive_dataset = [(tweet_dict, "Positive")
                         for tweet_dict in positive_tokens_for_model]

    negative_dataset = [(tweet_dict, "Negative")
                         for tweet_dict in negative_tokens_for_model]

    dataset = positive_dataset + negative_dataset

    random.shuffle(dataset)

    train_data = dataset[:7000]
    test_data = dataset[7000:]

    classifier = NaiveBayesClassifier.train(train_data)

    print("Accuracy is:", classify.accuracy(classifier, test_data))

    print(classifier.show_most_informative_features(10))

    for tweet in tweets:
       print("\ntweet: "), tweet
       probdist = classifier.prob_classify(extract_features(tweet.split()))
       pred_sentiment = probdist.max()
        
     # custom_tokens = remove_noise(word_tokenize(tweets))

    #print(tweets, classifier.classify(dict([token, True] for token in custom_tokens)))
   
def extract_features(word_list):
    return dict([(word, True) for word in word_list])

if __name__=='__main__':
   # Load positive and negative reviews  
   positive_fileids = movie_reviews.fileids('pos')
   negative_fileids = movie_reviews.fileids('neg')
   features_positive = [(extract_features(movie_reviews.words(fileids=[f])), 
           'Positive') for f in positive_fileids]
   features_negative = [(extract_features(movie_reviews.words(fileids=[f])), 
           'Negative') for f in negative_fileids]
   #Split the data into train and test (80/20)
   threshold_factor = 0.8
   threshold_positive = int(threshold_factor * len(features_positive))
   threshold_negative = int(threshold_factor * len(features_negative))
   features_train = features_positive[:threshold_positive] + features_negative[:threshold_negative]
   features_test = features_positive[threshold_positive:] + features_negative[threshold_negative:]  
   print("\nNumber of training datapoints:"), len(features_train)
   print("Number of test datapoints:"), len(features_test)
   # Train a Naive Bayes classifier
   classifier = NaiveBayesClassifier.train(features_train)
   print("\nAccuracy of the classifier:"), nltk.classify.util.accuracy(classifier, features_test)
   print("\nTop 10 most informative words:")
   for item in classifier.most_informative_features()[:10]:
       print(item[0])
   print("\nPredictions:")
   for review in tweets:
       print("\nReview:", review)
       probdist = classifier.prob_classify(extract_features(review.split()))
       pred_sentiment = probdist.max()
       print("Predicted sentiment:", pred_sentiment)
       print("Probability:", round(probdist.prob(pred_sentiment), 2))
      '''