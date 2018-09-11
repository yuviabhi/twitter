
#### CONVERT SHAPE TO POLYGONS
# RUN(Creates polygon shapes) : python shape2polygons.py > a.csv


import fiona
from osgeo import ogr

shapefile = fiona.open("News_Flood_Report.shp")
#print shape.schema

poly = shapefile.next()
while(poly != ''):
		
	from shapely.geometry import shape
	shp_geom = shape(poly['geometry'])	
	type_ = str(type(shp_geom))
	#print type1
	if(type_ == "<class 'shapely.geometry.multipolygon.MultiPolygon'>"):
		multipoly_wkt = str(shp_geom)
		geom_multipoly = ogr.CreateGeometryFromWkt(multipoly_wkt)
		geom_poly = ogr.ForceToPolygon(geom_multipoly)
		wkt = geom_poly.ExportToWkt()
		print wkt
	else:
		print shp_geom	

	try :
		poly = shapefile.next()
	except :
		break

