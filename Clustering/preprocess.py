#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  8 12:12:54 2017

@author: korda
"""

import numpy as np
import pandas as pd


dataset = pd.read_csv('user_social.csv', sep='\t')

#remove index
dataset = dataset.iloc[:, 1:]
#remove last three columns (birthday)
dataset = dataset.iloc[:, :-3]
#remove email column
dataset = dataset.drop(' emails', 1)

#filling missing values
dataset.info()

#majority = fashion
countAbout = dataset[' about'].value_counts()
#majority = Milan
countCity = dataset[' city'].value_counts()
#majority = Italy
countCountry = dataset[' country'].value_counts()
#majority = Community
countCategory = dataset[' category'].value_counts()
#majority = fashion
countDescription = dataset[' description'].value_counts()

#filling with most frequent ones
#TODO: fill from distribution
dataset[' about'] = dataset[' about'].fillna('fashion', axis = 0)
dataset[' city'] = dataset[' city'].fillna('Milan', axis = 0)
dataset[' country'] = dataset[' country'].fillna('Italy', axis = 0)
dataset[' category'] = dataset[' category'].fillna('Community', axis = 0)
dataset[' description'] = dataset[' description'].fillna('fashion', axis = 0)

datasetCategorical = dataset

#encoding categorical values
from sklearn.preprocessing import LabelEncoder, OneHotEncoder

labelEncoder = LabelEncoder()
dataset.iloc[:, 0] = labelEncoder.fit_transform(dataset.iloc[:, 0]).flatten()
dataset.iloc[:, 1] = labelEncoder.fit_transform(dataset.iloc[:, 1]).flatten()
dataset.iloc[:, 2] = labelEncoder.fit_transform(dataset.iloc[:, 2]).flatten()
dataset.iloc[:, 3] = labelEncoder.fit_transform(dataset.iloc[:, 3]).flatten()
dataset.iloc[:, 4] = labelEncoder.fit_transform(dataset.iloc[:, 4]).flatten()

oneHotEncoder = OneHotEncoder(categorical_features=[0, 1, 2, 3, 4])
X = oneHotEncoder.fit_transform(dataset.values).toarray()
#maybe delete first ones

#clustering KMeans
from sklearn.cluster import KMeans

kmeans = KMeans(n_clusters=5, random_state=0).fit(X)
labels = kmeans.labels_


#append cluster labels to datasetCategorical
datasetCategorical.loc[:, ' cluster'] = labels


#plotting
import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(111)
scatter = ax.scatter(datasetCategorical[' about'],datasetCategorical[' country'],c=datasetCategorical[' cluster'],s=50)
ax.set_xlabel('about')
ax.set_ylabel('country')
plt.colorbar(scatter)

fig.show()








