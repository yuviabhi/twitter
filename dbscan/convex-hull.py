#convex hull

'''
Run code : python convex-hull.py > convex_hull_boundary_kolkata_20170803-eps_0.01.csv

Change the Constants value accordingly for each run
'''

import pandas as pd
import numpy as np
from scipy.spatial import ConvexHull
import matplotlib.pyplot as plt
from osgeo import ogr

#Constants
eps = '0.2'
minsamples = '6'
dataset = '20170724-20170913'
place = 'kolkata'

df = pd.read_csv('~/Documents/abhisek-workspace/codes/twitter/dbscan/dbscan_clusters_rellocated_'+place+'_'+dataset+'-eps_'+eps+'_minsamples_'+minsamples+'.csv',
	usecols=["lat", "lon", "cluster"])

output_file ='convex_hull_boundary_rellocated'+place+'_'+dataset+'-eps_'+eps+'_minsamples_'+minsamples+'.csv'

def convert3Dto2D(poly):
	json_geom = poly.ExportToJson()

	# convert json format to a Python dictionary
	import json
	geom = json.loads(json_geom)

	# slice the coordinates to eliminate 3D
	new_coords =  [[i[:2] for i in geom['coordinates'][0]]]

	new = { "type": "Polygon",'coordinates': new_coords}

	# recreate the ogr geometry
	poly = ogr.CreateGeometryFromJson(json.dumps(new))
	return poly


if __name__ == "__main__":

	convexhull_count = 0
	
	multipolygon = ogr.Geometry(ogr.wkbMultiPolygon)
	
	no_of_cluster = np.unique(df['cluster'].values).shape[0]
	
	polygon = ''
	
	for i in range(no_of_cluster):
		
		i = i+1
		
		cluster = df['cluster'] == i

		df1 =	df[cluster]

		df1 = df1[['lat','lon']]

		df1 = df1.values
		
		try:
			
			hull = ConvexHull(df1)
			
			if hull != '':
				convexhull_count = convexhull_count + 1	
			
			#PLOTTING ALL POINTS
			plt.plot(df1[:,0], df1[:,1], 'o')
			
			#print hull.vertices
			
			# Create ring #1
			ring = ogr.Geometry(ogr.wkbLinearRing)
				
			for vertex in hull.vertices:
				#print df1[vertex, 1],df1[vertex, 0]
				ring.AddPoint(df1[vertex, 1], df1[vertex, 0])
				
			# Create polygon #1
			poly = ogr.Geometry(ogr.wkbPolygon)
			poly.AddGeometry(ring)
			#print ring
			print convert3Dto2D(poly).ExportToWkt()
			polygon += convert3Dto2D(poly).ExportToWkt()
			#multipolygon.AddGeometry(poly)				
				
			# PLOTTING THE POLYGON	
			for simplex in hull.simplices:			
				plt.plot(df1[simplex, 0], df1[simplex, 1], 'k-')				
				#print df1[simplex, 0], df1[simplex, 1]							
				#plt.plot(df1[hull.vertices,0], df1[hull.vertices,1], 'r--', lw=2)
				#plt.plot(df1[hull.vertices[0],0], df1[hull.vertices[0],1], 'ro')
				
				

									
		except:
			
			pass

	#print multipolygon.ExportToWkt()
	#print multipolygon.ExportToKML()

	
	#print 'No. of convex hull : '+ str(convexhull_count)			
	#plt.show()
	
	with open(output_file, "w") as file:
		file.write(polygon.replace('))','))\n'))


		


	
	
	
