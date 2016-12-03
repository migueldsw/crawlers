import numpy as np;
from scipy import stats
import scipy.cluster.hierarchy as hac
import matplotlib.pyplot as plt


def calc_cluster(D):
	return hac.linkage(D, 'single')


# Plot the dendrogram
def plot_dendrogram(Z):
	print 'Z:',Z
	plt.figure(figsize=(25, 10))
	plt.title('Hierarchical Clustering Dendrogram')
	plt.xlabel('Document index')
	plt.ylabel('Relative Levenshtein Distance')
	hac.dendrogram(
	    Z,
	    leaf_rotation=90.,  # rotates the x axis labels (90 or 0 )
	    leaf_font_size=8.,  # font size for the x axis labels
	)
	#set y axis plot range
	p_range = np.max(Z[:,2]) - np.min(Z[:,2])
	alfa = p_range/10
	axes = plt.gca()
	axes.set_ylim([np.min(Z[:,2])-alfa,np.max(Z[:,2])+alfa])
	#axes.set_xlim([xmin,xmax])
	#plt.show()
	plt.savefig('plots/dendrogram.png')


# D = [0    , 1    , 0.8   ,  0.2  ,        
# 	1	,     0  ,    0.9    ,    0.33   ,
# 	 0.8   ,    0.9   ,   0     ,  0.75     ,
# 	  0.2  ,    0.33   ,      0.75  ,   0	 ]
# D = np.array(D).reshape(4,4)
# Z = calc_cluster(D)
# plot_dendrogram(Z)