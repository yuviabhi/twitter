import numpy as np
fname = "/home/abhisek/Documents/abhisek-workspace/codes/twitter/dbscan/dbscan_clusters_kolkata_20170724-20170913-eps_0.2_minsamples_6.csv"
points = np.loadtxt(fname,dtype='float',skiprows=1,delimiter=',',usecols=(0,1))

print points


from scipy.spatial import Voronoi, voronoi_plot_2d

vor = Voronoi(points)

import matplotlib.pyplot as plt

voronoi_plot_2d(vor,show_vertices=False)

plt.show()



