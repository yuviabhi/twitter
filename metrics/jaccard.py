from osgeo import ogr
import pandas as pd

#wkt1 = "POLYGON ((1208064.271243039 624154.6783778917, 1208064.271243039 601260.9785661874, 1231345.9998651114 601260.9785661874, 1231345.9998651114 624154.6783778917, 1208064.271243039 624154.6783778917))"
#wkt2 = "POLYGON ((1199915.6662253144 633079.3410163528, 1199915.6662253144 614453.958118695, 1219317.1067437078 614453.958118695, 1219317.1067437078 633079.3410163528, 1199915.6662253144 633079.3410163528)))"


def jaccard_similarity_for_polygon_shapes (df, df_official, method):
	try:
		poly_count = 1
		total_jaccard = 0.0
		total_intersection_area = 0.0
		total_union_area = 0.0
		
		for row1 in df.itertuples():
			#print row1[1]
			wkt1 = row1[1]
			#print 'Polygon No. ',poly_count, '==================================================================================='
			poly_count = poly_count + 1
			
			for row2 in df_official.itertuples():
				#print row2[1]
				wkt2 = row2[1]
				#break
				#print 'b'
			
				try:
			
					poly1 = ogr.CreateGeometryFromWkt(wkt1)
					#print "Area = %d" % poly1.GetArea()
					poly2 = ogr.CreateGeometryFromWkt(wkt2)
			
					union = poly1.Union(poly2)
					u = ogr.CreateGeometryFromWkt(union.ExportToWkt())
					union_area = u.GetArea()
					#print union_area
					total_union_area = total_union_area + union_area
					#print "UNION = %d" % union_area

					intersection = poly1.Intersection(poly2)
					inter = ogr.CreateGeometryFromWkt(intersection.ExportToWkt())
					inter_area = inter.GetArea()
					#print inter_area
					total_intersection_area = total_intersection_area + inter_area
					#print "INTERSECTION = %d" % inter_area
					jaccard = (inter_area / union_area) * 100
					#print "Jaccard Similarity = %f" % jaccard ,"%"
					total_jaccard = total_jaccard + jaccard

				except :
					pass
	 				#print 'c'
			#break
		print "Jaccard Similarity by ", method, " = %f" % (total_jaccard/(poly_count - 1)) ,"%" 
		#print "Polygon Count = %d" % (poly_count - 1)
		#print total_intersection_area , " -- ", total_union_area
	except :
		pass
		
		
def jaccard_similarity_for_multipolygon_shapes (df, df_official, method):
	try:
		poly_count = 1
		total_jaccard = 0.0
		total_intersection_area = 0.0
		total_union_area = 0.0
		
		for row1 in df.itertuples():
			#print row1[1]
			wkt1 = row1[1]

			#print 'Polygon No. ',poly_count, '==================================================================================='
			poly_count = poly_count + 1
			
			for row2 in df_official.itertuples():
				#print row2[1]
				wkt2 = row2[1]
				#break
				#print 'b'
			
				try:
					#print wkt1
					poly1 = ogr.CreateGeometryFromWkt(wkt1)					
					#print "Area = %d" % poly1.GetArea()
					poly2 = ogr.CreateGeometryFromWkt(wkt2)
					
					union = poly1.Union(poly2)
					u = ogr.CreateGeometryFromWkt(union.ExportToWkt())
					union_area = u.GetArea()
					#print 'union_area ',union_area
					total_union_area = total_union_area + union_area
					#print "UNION = %d" % union_area

					intersection = poly1.Intersection(poly2)
					inter = ogr.CreateGeometryFromWkt(intersection.ExportToWkt())
					inter_area = inter.GetArea()
					#print 'intersection_area ',inter_area
					total_intersection_area = total_intersection_area + inter_area
					#print "INTERSECTION = %d" % inter_area
					jaccard = (inter_area / union_area) * 100
					#print "Jaccard Similarity = %f" % jaccard ,"%"
					total_jaccard = total_jaccard + jaccard

				except :
					pass
	 				#print 'c'
			#break
		print "Jaccard Similarity by ", method, " = %f" % (total_jaccard/(poly_count - 1)) ,"%" 
		#print "Polygon Count = %d" % (poly_count - 1)
		#print total_intersection_area , " -- ", total_union_area
	except :
		pass
		
def check(df) :
	for row in df.itertuples():
		wkt1 = row[1]
		poly1 = ogr.CreateGeometryFromWkt(wkt1)	
		#print poly1
		union = poly1.Intersection(poly1)
		
	
		
if __name__=='__main__':

	#WITH MULTI-POLYGON SHAPED DATA
	df_tweet = pd.read_csv('org/convex-hull-by-tweets-multipolygons.csv',sep = "\t",header=None)
	df_elev = pd.read_csv('org/convex-hull-by-elev-multipolygons.csv',sep = "\t",header=None)
	df_rbm = pd.read_csv('org/convex-hull-by-rbm-multipolygons.csv',sep = "\t",header=None)
	df_official = pd.read_csv('news-report-bihar-multipolygons2.csv',sep = "\t",header=None)	
	#check(df_official)
	jaccard_similarity_for_multipolygon_shapes(df_tweet, df_official, 'Tweets')	
	jaccard_similarity_for_multipolygon_shapes(df_elev, df_official, 'Elevation')
	jaccard_similarity_for_multipolygon_shapes(df_rbm, df_official, 'RBM')
	
	##############################################################################################
	
	#WITH POLYGON SHAPED DATA
	#df_tweet = pd.read_csv('tweek/convex-hull-by-tweets-multipolygons.csv',sep = "\t",header=None)
	#df_elev = pd.read_csv('tweek/convex-hull-by-elev-multipolygons.csv',sep = "\t",header=None)
	#df_rbm = pd.read_csv('tweek/convex-hull-by-rbm-multipolygons.csv',sep = "\t",header=None)
	#df_official = pd.read_csv('news-report-bihar-polygons.csv',sep = "\t",header=None)
	#jaccard_similarity_for_polygon_shapes(df_tweet, df_official, 'Tweets')	
	#jaccard_similarity_for_polygon_shapes(df_elev, df_official, 'Elevation')
	#jaccard_similarity_for_polygon_shapes(df_rbm, df_official, 'RBM')
	




######################## OUTPUT ########################
### WITH POLYGON SHAPED DATA ###
#Jaccard Similarity by  Tweets  = 37.486539 %
#Jaccard Similarity by  Elevation  = 42.500089 %
#Jaccard Similarity by  RBM  = 42.585572 %



