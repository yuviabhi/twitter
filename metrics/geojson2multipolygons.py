
#### CONVERT GEOJSON TO MULTIPOLYGON
#INCOMPLETE
import pygeoj
import string
from osgeo import ogr


def geojson_to_multipolygon(filepath):
	gson_input = pygeoj.load(filepath=filepath)
	new_multipolygon = ogr.Geometry(ogr.wkbMultiPolygon)
	for feature in gson_input:
		multipolygon = feature.geometry.coordinates
		poly1 = ogr.Geometry(ogr.wkbPolygon)			
		for polygon in multipolygon:
			ring1 = ogr.Geometry(ogr.wkbLinearRing)
			for pnt in polygon:
				try:
					ring1.AddPoint(float(pnt[1]), float(pnt[0]))
				except:
					pass
			poly1.AddGeometry(ring1)
		new_multipolygon.AddGeometry(poly1)	
		print new_multipolygon.ExportToWkt()			
			


if __name__ == '__main__' :
	geojson_to_multipolygon("org/convex-hull-rellocated-multipolygon.geojson")
	
	
	
