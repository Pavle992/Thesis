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

dataset1 = dataset1.iloc[:, 3:]
dataset2 = dataset2.iloc[:, 3:]
dataset3 = dataset3.iloc[:, 3:]
dataset4 = dataset4.iloc[:, 3:]
dataset5 = dataset5.iloc[:, 3:]

# Remove links
dataset1 = dataset1[dataset1['CONTENT'].map(checkSpam) == False]
dataset2 = dataset1[dataset2['CONTENT'].map(checkSpam) == False]
dataset3 = dataset1[dataset3['CONTENT'].map(checkSpam) == False]
dataset4 = dataset1[dataset4['CONTENT'].map(checkSpam) == False]
dataset5 = dataset1[dataset5['CONTENT'].map(checkSpam) == False]

dataset = pd.concat([dataset1, dataset2, dataset3, dataset4, dataset5])

dataset['CLASS'].value_counts()

stop = stopwords.words('english')
flt = ['[', ']', '.', ',', ':', ';', '(', ')', 'i', 'u']
stop.extend(flt)

from nltk.tokenize import RegexpTokenizer

all_words = []
tokenizer = RegexpTokenizer(r'\w+')


def preprocess(sentence):

    lemmatizer = WordNetLemmatizer()
    return [lemmatizer.lemmatize(word.lower()) for word in tokenizer.tokenize(sentence) if word not in stop]


# print(preprocess(dataset.iloc[1, 0]))
import nltk

for comment in dataset.iloc[:, 0]:
    all_words.extend(preprocess(comment))

# print(all_words[:100])
all_words = nltk.FreqDist(all_words)
#
word_features = list(all_words.keys())[:100]
print(word_features)

import pickle

with open('word_features', 'wb') as fp:
    pickle.dump(word_features, fp)


def find_features(comment):
    features = {}

    for w in word_features:
        if w in set(preprocess(comment)):
            features[w] = 1
        else:
            features[w] = 0

    return features


# print(find_features(dataset.iloc[0, 0]))

X_train = pd.DataFrame(0, index=np.arange(dataset.shape[0]), columns=word_features)
print(X_train.shape)
# X_train.iloc[0, 0] = pd.DataFrame(find_features(dataset.iloc[0, 0]))
i = 0

for row in dataset.iloc[:, 0]:
    feature_vect = find_features(row)
    X_train.iloc[i, :] = pd.Series(feature_vect)
    i += 1

Y_train = dataset.iloc[:, 1]

# Fitting classifier to the Training set
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X_train, Y_train, test_size=0.25, random_state=0, stratify=Y_train)

models = {
    'NaiveBayes': GaussianNB()
}

classifier = models['NaiveBayes']
classifier = classifier.fit(X_train, y_train)

y_pred = classifier.predict(X_test)
print(y_pred)

from sklearn.metrics import confusion_matrix, f1_score, precision_score
cm = confusion_matrix(y_test, y_pred)
f1 = f1_score(y_test, y_pred, average='binary', pos_label=1)
prec = precision_score(y_test, y_pred)


print(cm)
print(f1)
print(prec)

from sklearn.externals import joblib

joblib.dump(classifier, 'spam_classifier.joblib.pkl', compress=9)
