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

# PCA Analysis
from sklearn.decomposition import PCA
pca = PCA(n_components = 2)
X_transformed = pca.fit_transform(X)

# KneeElbowAnalysis to determin number of clusters 
import matplotlib.pyplot as plt
from plotting_api import KneeElbowAnalysis

KneeElbowAnalysis(X_transformed)

#clustering KMeans
from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=4, init='k-means++', n_init=10, random_state=0).fit(X_transformed)
labels = kmeans.labels_

#append cluster labels to datasetCategorical
datasetCategorical.loc[:, ' cluster'] = labels
df.loc[:, ' cluster'] = labels

# print(datasetCategorical.head(20))

from plotting_api import Plotter

plotter = Plotter(X_transformed)
plotter.scatter(c_data=labels, x_label='PC1', y_label='PC2')

# datasetCategorical.to_csv('user_social_categorical_clustered.csv', sep='\t', encoding='utf-8')
# df.to_csv('user_social_clustered.csv', sep='\t', encoding='utf-8')







