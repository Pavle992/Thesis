import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt

df = pd.read_csv('user_social_clustered.csv', sep = '\t', index_col=0)

print(df.head())
# About city plot
fig, axes = plt.subplots(nrows=2, ncols=1)
df.loc[df[' cluster']==0,' about'].value_counts().plot(kind='bar', ax=axes[0])
df.loc[df[' cluster']==0,' country'].value_counts().plot(kind='bar', ax=axes[1])
fig, axes = plt.subplots(nrows=2, ncols=1)
df.loc[df[' cluster']==0,' city'].value_counts().plot(kind='bar', ax=axes[0])
df.loc[df[' cluster']==0,' category'].value_counts().plot(kind='bar', ax=axes[1])

#show distribuions

# plt.scatter(df[' about'], df[' city'], c=df[' cluster'], s=50)
# plt.xlabel('about')
# plt.ylabel('city')

plt.show()
