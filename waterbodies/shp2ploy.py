
#Convert Waterbodies Shape to Polygons

import fiona
from shapely.geometry import shape
import string
from osgeo import gdal,ogr

def create_polygon(coords):          
	ring = ogr.Geometry(ogr.wkbLinearRing)
	for coord in coords:
		ring.AddPoint(coord[0], coord[1])

	# Create polygon
	poly = ogr.Geometry(ogr.wkbPolygon)
	poly.AddGeometry(ring)
	return poly.ExportToWkt()
    
    
with fiona.open('e083n24e.shp', 'r') as input:
	with open('e083n24e.txt', 'w') as output:
		for pt in input:
			type = pt['geometry']['type']
			if (type=='Polygon') :
				coords = pt['geometry']['coordinates']
				
				for each_coords in coords:
					polygons = create_polygon(each_coords)
					print polygons
					output.write(polygons + '\n')
				
				#id = pt['properties']['id']
				#cover = pt['properties']['cover']
				#x = str(shape(pt['geometry']).x)
				#y = str(shape(pt['geometry']).y)
				#output.write(id + ' ' + x + ' ' + y+ ' ' + cover + '\n')
