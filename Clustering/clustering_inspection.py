import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt

df = pd.read_csv('user_social_clustered.csv', sep = '\t', index_col=0)

print(df.head())

from plotting_api import Plotter

plotter = Plotter(df=df)

# Cluster 0 Plot
plotter.plot(columns=[' about', ' country'], clusterNum=0)
plotter.plot(columns=[' city', ' category'], clusterNum=0)
plotter.plot(columns=[' description'], clusterNum=0)

# Cluster 1 Plot
plotter.plot(columns=[' about', ' country'], clusterNum=1)
plotter.plot(columns=[' city', ' category'], clusterNum=1)
plotter.plot(columns=[' description'], clusterNum=1)

# Cluster 2 Plot
plotter.plot(columns=[' about', ' country'], clusterNum=2)
plotter.plot(columns=[' city', ' category'], clusterNum=2)
plotter.plot(columns=[' description'], clusterNum=2)

# Cluster 3 Plot
plotter.plot(columns=[' about', ' country'], clusterNum=3)
plotter.plot(columns=[' city', ' category'], clusterNum=3)
plotter.plot(columns=[' description'], clusterNum=3)


# # Cluster 0
# about : Fashion
# country: Italy, United States
# city: Milan, Madrid, London
# category: Personal Blog
# description: Fashion

# # Cluster 1
# about : Fashion
# country: United States
# city: Los Angeles, New York
# category: Community
# description: Design

# # Cluster 2
# about : Accessories
# country: Italy
# city: Milan
# category: Clothing (Brand)
# description: Fashion

# # Cluster 3
# about : Accessories
# country: Italy
# city: Rome
# category: Website
# description: Design