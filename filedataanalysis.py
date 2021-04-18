# -*- coding: utf-8 -*-
"""
Created on Sat Apr 17 20:38:46 2021

@author: Lucien
"""
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

x = input("Enter a file name: ")
#data needs to be a global var for plots
dataset = pd.read_csv(x)

#this gives us the numbers of nos and yeses within a certain category
#if i put something in the value_counts, it gives me a percentage
multi =  dataset['he/him'].value_counts()
num_he = multi[1]
print(multi)
multi =  dataset['she/her'].value_counts()
num_she = multi[1]
print(multi)
multi =  dataset['they/them'].value_counts()
num_they = multi[1]
print(multi)
print(num_they,num_he,num_she)