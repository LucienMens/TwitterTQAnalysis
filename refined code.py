# -*- coding: utf-8 -*-
"""
Created on Sun Apr 25 16:37:05 2021

@author: pando
"""
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
user_features_list = ["screen_name", "name", "location", "bio", "tweet",
                      "he/him", "she/her", "they/them",
                      "it/its", "xe/xem", "ze/zir"]

query_list = ["thembo","bimbo","himbo","theydies","ladies", "gentlethem", "gentlemen", "theybie", "transgender","transwoman","transman"]


#english language tweets
language = "en"
#can set number of tweets to pull - up to 100
numTweets = 100
#calling the user_timeline function with our parameters
def createcsv(date_str):
    df_dict = {}    
    for query in query_list:
        print("Getting res for ")
        res = api.search(q=query, lang=language, count=numTweets)
        users_df = pd.DataFrame(columns = user_features_list)
        for tweet in res:
            # Create empty dict
            user_features = {}
            # Get user data
            user_features['bio'] = tweet.user.description
            user_features['screen_name'] = tweet.user.screen_name
            user_features['name'] = tweet.user.name
            user_features['tweet'] = tweet.text
            user_features['location'] = tweet.user.location
            user = pd.DataFrame(user_features, index = [0])
            users_df = pd.concat([users_df, user], ignore_index = True)
        filename = 'raw_%s_%s.csv' % (query, date_str)   
        users_df.to_csv(filename, encoding='utf-8', index=False)
createcsv('4_25')
'''    
pandas apply 
search for files 
for query in query_list:   
    users_df = pd.DataFrame(columns = user_features_list)
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
    for tweet in res_dict[query]:
        #prints the username, tweet w query, and bio description
        tweets.append(tweet.text)
        #print(tweet.user.screen_name,"Tweeted:",tweet.text,"| User Description:",tweet.user.description)
        authors.append(tweet.user.screen_name)
        #this searches for they/themm
       
        if re.search((r'\bshe\b' or r'\bher\b'), tweet.user.description, re.IGNORECASE):
            pro_she.append(tweet.user.screen_name)
        if re.search((r'\bshe\b' or r'\bher\b'), tweet.user.location, re.IGNORECASE):
            pro_she.append(tweet.user.screen_name)
        if re.search((r'\bhe\b' or r'\bhim\b'), tweet.user.description, re.IGNORECASE):
            pro_he.append(tweet.user.screen_name)
        if re.search((r'\bhe\b' or r'\bhim\b'), tweet.user.location, re.IGNORECASE):
            pro_he.append(tweet.user.screen_name)
        if re.search((r'\bit\b' or r'\bits\b'), tweet.user.description, re.IGNORECASE):
            pro_it.append(tweet.user.screen_name)
        if re.search((r'\bit\b' or r'\bits\b'), tweet.user.location, re.IGNORECASE):
            pro_it.append(tweet.user.screen_name)
        if re.search((r'\bxe\b' or r'\bxir\b' or r'\bxem\b' or r'\bxey\b'), tweet.user.description, re.IGNORECASE):
            pro_xe.append(tweet.user.screen_name)
        if re.search((r'\bxe\b' or r'\bxir\b' or r'\bxem\b' or r'\bxey\b'), tweet.user.location, re.IGNORECASE):
            pro_xe.append(tweet.user.screen_name)
        if re.search((r'\bze\b' or r'\bzir\b' or r'\bzem\b'), tweet.user.description, re.IGNORECASE):
            pro_ze.append(tweet.user.screen_name)
        if re.search((r'\bze\b' or r'\bzir\b' or r'\bzem\b'), tweet.user.location, re.IGNORECASE):
            pro_ze.append(tweet.user.screen_name)
            #de,dem           
    for tweet in res_dict[query]:
        
    # Create empty dict
        user_features = {}
    # Get user data
    #if user in pro:
   # item = api.get_user(user)
        user_features['bio'] = tweet.user.description
        user_features['screen_name'] = tweet.user.screen_name
        user_features['name'] = tweet.user.name
        user_features['tweet'] = tweet.text
        user_features['location'] = tweet.user.location
        #fills in the yeses
        if re.search((r'\bthey\b' or r'\bthem\b'), tweet.user.description, re.IGNORECASE):
            user_features['they/them'] = 'yes'
        if re.search((r'\bthey\b' or r'\bthem\b'), tweet.user.location, re.IGNORECASE):
             user_features['they/them'] = 'yes'
        if tweet.user.screen_name in pro_he:
            user_features['he/him'] = 'yes'
        if tweet.user.screen_name in pro_she:
            user_features['she/her'] = 'yes'
        if tweet.user.screen_name in pro_it:
            user_features['it/its'] = 'yes'
        if tweet.user.screen_name in pro_xe:
            user_features['xe/xem'] = 'yes'
        if tweet.user.screen_name in pro_ze:
            user_features['ze/zem'] = 'yes'
        #fills in the nos
        if tweet.user.screen_name not in pro_he:
            user_features['he/him'] = 'no'
        if tweet.user.screen_name not in pro_she:
            user_features['she/her'] = 'no'
        if tweet.user.screen_name not in pro_xe:
            user_features['xe/xem'] = 'no'
        if tweet.user.screen_name not in pro_they:
            user_features['they/them'] = 'no'
        if tweet.user.screen_name not in pro_it:
            user_features['it/its'] = 'no'
        if tweet.user.screen_name not in pro_ze:
            user_features['ze/zir'] = 'no'
        # Concat the dfs
        user = pd.DataFrame(user_features, index = [0])
        users_df = pd.concat([users_df, user], ignore_index = True)
    date_string = '4_24'
    filename = '%s_%s.csv' % (query, date_string)   
    users_df.to_csv(filename, encoding='utf-8', index=False)
   # return pro_ze, pro_xe, pro_it, pro_he, pro_she, pro_they
#list of usernames
    pro = pro_ze + pro_xe + pro_it + pro_he + pro_she + pro_they
    print(query," length of set of pro: ", len(set(pro)))
'''