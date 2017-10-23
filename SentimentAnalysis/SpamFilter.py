#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 22 23:56:17 2017

@author: korda
"""
import pickle

from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk import WordNetLemmatizer

from sklearn.externals import joblib
import pandas as pd

import re

class SpamFilter:

    def __init__(self):
        with open ('./res/word_features', 'rb') as fp:
            self.word_features = pickle.load(fp)

        flt = ['[', ']', '.', ',', ':', ';', '(', ')', 'i', 'u']
        self.stop = stopwords.words('english')
        self.stop.extend(flt)

        self.tokenizer = RegexpTokenizer(r'\w+')
        self.lemmatizer = WordNetLemmatizer()

        self.classifier = joblib.load('./res/spam_classifier.joblib.pkl')

    def preprocess(self, sentence):
        return [self.lemmatizer.lemmatize(word.lower()) for word in self.tokenizer.tokenize(sentence) if word not in self.stop]

    def find_features(self, comment):
        features = {}
        for w in self.word_features:
            if w in set(self.preprocess(comment)):
                features[w] = 1
            else:
                features[w] = 0

        return features

    def checkSpamBayes(self, text):
        x = pd.Series(self.find_features(text))
        y = self.classifier.predict(x.values.reshape(-1,1))
        if y[0] == 0:
            return False
        else:
            return True

    def checkSpam(self, text):
        spam_pattern = "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
        result = re.findall(spam_pattern, text)
        if len(result) == 0:
            return self.checkSpamBayes(text)
        else:
            return True
