#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 21:02:47 2017

@author: korda
"""

import pandas as pd
import numpy as np

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

dataset1 = dataset1.iloc[:,3:]
dataset2 = dataset2.iloc[:,3:]
dataset3 = dataset3.iloc[:,3:]
dataset4 = dataset4.iloc[:,3:]
dataset5 = dataset5.iloc[:,3:]

# Remove links
dataset1 = dataset1[dataset1['CONTENT'].map(checkSpam) == False]
dataset2 = dataset1[dataset2['CONTENT'].map(checkSpam) == False]
dataset3 = dataset1[dataset3['CONTENT'].map(checkSpam) == False]
dataset4 = dataset1[dataset4['CONTENT'].map(checkSpam) == False]
dataset5 = dataset1[dataset5['CONTENT'].map(checkSpam) == False]

dataset = pd.concat([dataset1, dataset2, dataset3, dataset4, dataset5])

dataset['CLASS'].value_counts()