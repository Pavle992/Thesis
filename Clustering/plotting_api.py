import matplotlib.pyplot as plt

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
