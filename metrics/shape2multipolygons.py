
#### CONVERT SHAPE TO MULTIPOLYGONS
# RUN(Creates multipolygon shapes) : python shape2multipolygons.py > a.csv


import fiona
from osgeo import ogr
import string

def convert():
	shapefile = fiona.open("News_Flood_Report.shp")
	#print shape.schema

	poly = shapefile.next()

	all_polygons = ''

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
			#print wkt
			all_polygons = all_polygons +	 str(wkt) + '\n'
		else:
			#print shp_geom
			all_polygons = all_polygons + str(shp_geom) + '\n'

		try :
			poly = shapefile.next()
		except :
			break
	
	#return all_polygons
	return convert_to_multipolygon(all_polygons)
		
		
def convert_to_multipolygon(poly_wkt):
	
	#print poly_wkt
	# Given a test polygon
	#poly_wkt = "POLYGON ((1179091.164690328761935 712782.883845978067257,1161053.021822647424415 667456.268434881232679,1214704.933941904921085 641092.828859039116651,1228580.428455505985767 682719.312399842427112,1218405.065812198445201 721108.180554138729349,1179091.164690328761935 712782.883845978067257))" + "\n" 
	#poly_wkt = poly_wkt + "POLYGON ((2179091.164 712782.883845978067251,1161053.021822647424415 667456.268434881232679,1214704.933941904921085 641092.828859039116651,1228580.428455505985767 682719.312399842427112,1218405.065812198445201 721108.180554138729349,2179091.164 712782.883845978067251))"
	
	multipolygon = ogr.Geometry(ogr.wkbMultiPolygon)
	
	pply_list = poly_wkt.split("POLYGON ((")
	for a_poly in pply_list :
		#print a_poly
		a_point = a_poly.split(", ")
		#print a_point

		ring1 = ogr.Geometry(ogr.wkbLinearRing)	

		for a_p in a_point:
			a_p = string.replace(a_p, '((', '')
			a_p = string.replace(a_p, '))', '')
			a_p = string.replace(a_p, '', '')						
			if(a_p != ''):
				#print a_p
				x = a_p.split(" ")
				try:
					ring1.AddPoint(float(x[0]), float(x[1]))
				except:
					pass
					#print x
		poly1 = ogr.Geometry(ogr.wkbPolygon)
		poly1.AddGeometry(ring1)
		multipolygon.AddGeometry(poly1)
		
		#if(a_p != ''):
		#	break
	
	return multipolygon.ExportToWkt()	
	
if __name__=='__main__':
	print convert()
	#try11()

