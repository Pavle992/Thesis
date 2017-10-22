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
import pickle

with open ('word_features', 'rb') as fp:
    word_features = pickle.load(fp)
        
import pandas as pd


from nltk import WordNetLemmatizer
from nltk.corpus import stopwords

import re

def checkSpam(text):
    spam_pattern = "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
    result = re.findall(spam_pattern, text)
    if len(result) == 0:
        return checkSpamBayes(text)
    else:
        return True


stop = stopwords.words('english')
flt = ['[', ']', '.', ',', ':', ';', '(', ')', 'i', 'u']
stop.extend(flt)

from nltk.tokenize import RegexpTokenizer

all_words = []
tokenizer = RegexpTokenizer(r'\w+')


def preprocess(sentence):

    lemmatizer = WordNetLemmatizer()
    return [lemmatizer.lemmatize(word.lower()) for word in tokenizer.tokenize(sentence) if word not in stop]


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
    if y[0] == 0:
        return False
    else:
        return True


print(checkSpam("Great performance"))
