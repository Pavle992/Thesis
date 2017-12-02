from SentimentCalculator import SentimentCalculator
import db_helper as db
import pandas as pd


df = pd.read_csv("user_social_clustered_new.csv", sep="\t", index_col=0)

clusters = df[' cluster'].unique()
clusters = sorted(clusters)

dct = dict((el, set()) for el in clusters)

# Create {cluster: set of users} hashtable
def groupUserToCluster(dct, row):
    cluster = row[' cluster']
    user_id = row[' user_id']
    dct[cluster].add(user_id)

df.apply(lambda x: groupUserToCluster(dct, x), axis=1)


# Calculate summed sentiment for clusters
cluster_sentiment_dct = dict((el, []) for el in clusters)

s = SentimentCalculator()
conn = db.db_connect()

# Create {cluster: list_of_sentiment_values}
for cluster in clusters:
    for userId in list(dct[cluster]):
        listOfCom = db.getAllCommentsForUser(userId)
        sent = s.calcSummedSentiment(listOfCom)
        cluster_sentiment_dct[cluster].append(sent)

print(cluster_sentiment_dct)
# Calculate cluster sentiments
res = dict((el, 0) for el in clusters)

for key, val in cluster_sentiment_dct.items():
    suma = sum(x['combined'] for x in val)
    res[key] = suma/len(val)

print(res)

import matplotlib.pyplot as plt

# dictionary = {0: 0.33, 1: 0.38, 2: 0.43, 3: 0.40}
plt.bar(list(res.keys()), res.values(), color=['purple', 'orange', 'blue', 'green'])
plt.xticks(list(res.keys()))
plt.xlabel('Clusters')
plt.ylabel('Average Sentiment Value')
plt.title('Sentiment Analysis of Clusters')
plt.show()