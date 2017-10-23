import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np

class Plotter(object):

	def __init__(self, df):		
		self.df = df

	def plot(self, columns, clusterNum, rows=2, cols=1):

		if len(columns) == 2:
			self.fig, self.axes = plt.subplots(nrows=rows, ncols=cols)
			# Column 1
			self.df.loc[self.df[' cluster']==clusterNum, columns[0]].value_counts().plot(kind='bar', ax=self.axes[0])
			self.axes[0].set_ylabel(columns[0])
			# Column 2
			self.df.loc[self.df[' cluster']==clusterNum,columns[1]].value_counts().plot(kind='bar', ax=self.axes[1])
			self.axes[1].set_ylabel(columns[1])
		elif len(columns) == 1:
			self.fig, self.axes = plt.subplots(nrows=1, ncols=1)
			self.df.loc[self.df[' cluster']==clusterNum,columns[0]].value_counts().plot(kind='bar', ax=self.axes)
			self.axes.set_ylabel(columns[0])
		else:
			raise ValueError('Cluster number should be 1 or 2')

		plt.suptitle('Cluster ' + str(clusterNum))
		plt.show()
		plt.close()

	def setRowsCols(self, rows, cols):
		self.fig, self.axes = plt.subplots(nrows=rows, ncols=cols)

	def scatter(self, c_data, x_label='x', y_label='y'):

		fig = plt.figure()
		ax = fig.add_subplot(111)
		scatter = ax.scatter(self.df[:, 0], self.df[:, 1], c=c_data, cmap=ListedColormap(('red', 'green', 'blue')), s=50)
		ax.set_xlabel(x_label)
		ax.set_ylabel(y_label)
		plt.show(fig)

from scipy.spatial.distance import cdist, pdist
from sklearn.cluster import KMeans

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