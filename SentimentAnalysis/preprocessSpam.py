#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 22 22:05:54 2017

@author: korda
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 21:02:47 2017

@author: korda
"""

import pandas as pd
import numpy as np

from nltk import word_tokenize, WordNetLemmatizer
from nltk.corpus import stopwords

import re

def checkSpam(text):
    spam_pattern = "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
    result = re.findall(spam_pattern, text)
    if len(result) == 0:
        return False
    else:
        return True

dataset1 = pd.read_csv('./YouTube-Spam-Collection-v1/Youtube01-Psy.csv', sep=',')
dataset2 = pd.read_csv('./YouTube-Spam-Collection-v1/Youtube02-KatyPerry.csv', sep=',')
dataset3 = pd.read_csv('./YouTube-Spam-Collection-v1/Youtube03-LMFAO.csv', sep=',')
dataset4 = pd.read_csv('./YouTube-Spam-Collection-v1/Youtube04-Eminem.csv', sep=',')
dataset5 = pd.read_csv('./YouTube-Spam-Collection-v1/Youtube05-Shakira.csv', sep=',')

dataset = pd.concat([dataset1, dataset2, dataset3, dataset4, dataset5])
dataset = dataset.iloc[:, 3:]
dataset = dataset1[dataset1['CONTENT'].map(checkSpam) == False]

stop = stopwords.words('english')
flt = ['[', ']', '.', ',', ':', ';', '(', ')', 'i', 'u']
stop.extend(flt)

from nltk.tokenize import RegexpTokenizer

all_words = []
tokenizer = RegexpTokenizer(r'\w+')


def preprocess(sentence):

    lemmatizer = WordNetLemmatizer()
    return [lemmatizer.lemmatize(word.lower()) for word in tokenizer.tokenize(sentence) if word not in stop]



import nltk

for comment in dataset.iloc[:, 0]:
    all_words.extend(preprocess(comment))


all_words = nltk.FreqDist(all_words)
word_features = list(all_words.keys())[:100]


def find_features(comment):
    features = {}

    for w in word_features:
        if w in set(preprocess(comment)):
            features[w] = 1
        else:
            features[w] = 0

    return features

from sklearn.externals import joblib

def checkSpamBayes(text):
    classifier = joblib.load('spam_classifier.joblib.pkl')
    x = pd.Series(find_features(text))
    y = classifier.predict(x)
    print(y)


checkSpamBayes("Great video!!")
