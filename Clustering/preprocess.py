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
# dataset[' about'] = dataset[' about'].fillna('fashion', axis = 0)
# dataset[' city'] = dataset[' city'].fillna('Milan', axis = 0)
# dataset[' country'] = dataset[' country'].fillna('Italy', axis = 0)
# dataset[' category'] = dataset[' category'].fillna('Community', axis = 0)
# dataset[' description'] = dataset[' description'].fillna('fashion', axis = 0)

# Fill About From Distribution
s = dataset[' about'].value_counts(normalize=True)
missing = dataset[' about'].isnull()
dataset.loc[missing,' about'] = np.random.choice(s.index, size=len(dataset[missing]),p=s.values)

# Fill City From Distribution
s = dataset[' city'].value_counts(normalize=True)
missing = dataset[' city'].isnull()
dataset.loc[missing,' city'] = np.random.choice(s.index, size=len(dataset[missing]),p=s.values)

# Fill Country From Distribution
s = dataset[' country'].value_counts(normalize=True)
missing = dataset[' country'].isnull()
dataset.loc[missing,' country'] = np.random.choice(s.index, size=len(dataset[missing]),p=s.values)

# Fill Category From Distribution
s = dataset[' category'].value_counts(normalize=True)
missing = dataset[' category'].isnull()
dataset.loc[missing,' category'] = np.random.choice(s.index, size=len(dataset[missing]),p=s.values)

# Fill Description From Distribution
s = dataset[' description'].value_counts(normalize=True)
missing = dataset[' description'].isnull()
dataset.loc[missing,' description'] = np.random.choice(s.index, size=len(dataset[missing]),p=s.values)

datasetCategorical = dataset
df = dataset.copy()

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


# PCA Analysis
from sklearn.decomposition import PCA
pca = PCA(n_components = 2) # First try with n_components = 2
X_transformed = pca.fit_transform(X)
# explained_variance = pca.explained_variance_

from scipy.spatial.distance import cdist, pdist
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

def KneeElbowAnalysis(x,max_k=11):
    k_values = range(1,max_k)
    clusterings = [KMeans(n_clusters=k, random_state=0).fit(x) for k in k_values]
    centroids = [clustering.cluster_centers_ for clustering in clusterings]

    D_k = [cdist(x, cent, 'euclidean') for cent in centroids]
    cIdx = [np.argmin(D,axis=1) for D in D_k]
    dist = [np.min(D,axis=1) for D in D_k]
    avgWithinSS = [sum(d)/x.shape[0] for d in dist]

    # Total with-in sum of square
    wcss = [sum(d**2) for d in dist]

    tss = sum(pdist(x)**2)/x.shape[0]
    bss = tss-wcss

    kIdx = 10-1
    
    #
    # elbow curve
    #
    fig = plt.figure()
    font = {'family' : 'sans', 'size'   : 12}
    plt.rc('font', **font)
    plt.plot(k_values, wcss, 'bo-', color='red', label='WCSS')
    plt.plot(k_values, bss, 'bo-', color='blue', label='BCSS')
    plt.grid(True)
    plt.xlabel('Number of clusters')
    plt.legend()
    plt.title('Knee for KMeans clustering');

    plt.show()

# KneeElbowAnalysis(X_transformed)



#clustering KMeans

kmeans = KMeans(n_clusters=4, init='k-means++', n_init=10, random_state=0).fit(X_transformed)
labels = kmeans.labels_


#append cluster labels to datasetCategorical
datasetCategorical.loc[:, ' cluster'] = labels
df.loc[:, ' cluster'] = labels

print(datasetCategorical.head(20))

#plotting
from matplotlib.colors import ListedColormap

fig = plt.figure()
ax = fig.add_subplot(111)
scatter = ax.scatter(X_transformed[:, 0], X_transformed[:, 1], c=labels, cmap=ListedColormap(('red', 'green', 'blue')), s=50)
ax.set_xlabel('PC1')
ax.set_ylabel('PC2')
# plt.colorbar(scatter)

# fig.show()
plt.show(fig)

# datasetCategorical.to_csv('user_social_categorical_clustered.csv', sep='\t', encoding='utf-8')
# df.to_csv('user_social_clustered.csv', sep='\t', encoding='utf-8')







