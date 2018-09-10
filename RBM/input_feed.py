"""
Generating inputs feed for RBM
Dataset : using extracted lat-lons-kolkata-20170724-20170913 from twitter
"""
import geopandas as gpd
from shapely.geometry import Point
from shapely.geometry import Polygon
import gdal
from gdalconst import *
import numpy as np
import pandas as pd
from osgeo import ogr
			

		
			
def map_coordinate_to_elevation(x, y, filename):
	try:
		dataset = gdal.Open(filename, GA_ReadOnly)
		transform = dataset.GetGeoTransform()
		#print transform
		xOrigin = transform[0]
		yOrigin = transform[3]
		pixelWidth = transform[1]
		pixelHeight = transform[5]
		band = dataset.GetRasterBand(1)
		bandtype = gdal.GetDataTypeName(band.DataType)
		x_off = int((x - xOrigin)/pixelWidth)
		y_off = int((y - yOrigin)/pixelHeight)
		try:
			data = band.ReadAsArray(x_off, y_off, 1, 1)
			#print "The elevation for co-ordinate ",x," and ",y," is ", data[0,0]
			return data[0,0]
		except:
			print "NAN"
			return 999999
	except: 
		pass	
		
	

def getPointsElevation(x,y):
	a = str(x).split(".")[0]
	b = str(y).split(".")[0]
	#print a,b
	if (int(a)<89 and int(a)>82 and int(b)<28 and int(b)>23) :
		#Reading elevation tiff dataset
		filename = "/home/abhisek/Documents/abhisek-workspace/codes/twitter/data-pull/dataset/elevation/srtm files/n"+b+"_e0"+a+"_1arc_v3.tif"	
		return map_coordinate_to_elevation(x, y, filename)
	else :
		#print 'Co-ordinate out of range'
		return 999999
		
		
#code incomplete  
def traverseTiffFile(dataset):
	transform = dataset.GetGeoTransform()
	xOrigin = transform[0]
	yOrigin = transform[3]
	pixelWidth = abs(transform[1])
	pixelHeight = abs(transform[5])
	band = dataset.GetRasterBand(1)
	data = band.ReadAsArray(0, 0, dataset.RasterXSize, dataset.RasterYSize)
	print xOrigin, yOrigin, pixelWidth, pixelHeight, dataset.RasterXSize/36, dataset.RasterYSize/36, data[0][1]
	for i in range(dataset.RasterXSize/36):
		for j in range(dataset.RasterYSize/36):
			print i,j, xOrigin, yOrigin, data[i][j] 
			xOrigin = xOrigin + (pixelWidth*100) #update X coordinate
		yOrigin = yOrigin - (pixelHeight*100)  #update Y coordinate
		xOrigin = transform[0]  #Resetting X coordinate
	return 0 
	
	
def findNeighbourhood(r,c,factor):
	neighbors = []
	neighbors.append(Point(r-factor,c-factor)) # Upper left.  r = row, c = column.
	neighbors.append(Point(r-factor,c)) # Upper middle.
	neighbors.append(Point(r-factor,c+factor)) # Upper right.
	neighbors.append(Point(r,c-factor)) # left.
	neighbors.append(Point(r,c+factor)) # right.
	neighbors.append(Point(r+factor,c+factor)) # Lowerleft.
	neighbors.append(Point(r+factor,c)) # lower middle.
	neighbors.append(Point(r+factor,c-factor)) # Lower left.
	return neighbors

#Returns the nearest distance of a point from the waterbodies
def getDistanceFromWaterbodies(point, filename):
	shapefile = gpd.read_file(filename)
	#point = Point(lat,lon)
	return point.distance(shapefile.geometry[0])	

#Returns the geometry of a file
def getGeom(filename):
	shapefile = gpd.read_file(filename)
	return shapefile.geometry[0]

#Creates buffer around a geometry feature	
def getBuffer(geom):
	from osgeo import ogr
	#wkt = "POINT (1198054.34 648493.09)"
	wkt = str(geom)
	pt = ogr.CreateGeometryFromWkt(wkt)
	bufferDistance = 0.00001
	poly = pt.Buffer(bufferDistance)
	#print "%s buffered by %d is %s" % (pt.ExportToWkt(), bufferDistance, poly.ExportToWkt())
	return poly.ExportToWkt()

		





def inside_polygon(x, y, points):
    """
    Return True if a coordinate (x, y) is inside a polygon defined by
    a list of verticies [(x1, y1), (x2, x2), ... , (xN, yN)].

    Reference: http://www.ariel.com.au/a/python-point-int-poly.html
    """
    n = len(points)
    inside = False
    p1x, p1y = points[0]
    for i in range(1, n + 1):
        p2x, p2y = points[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside
	
	
	

def getRainfall(x, y, file_rainfall):

	shape_rainfall = gpd.read_file(file_rainfall)
	district_name = np.array(shape_rainfall.NAME_2)
	rainfall = np.array(shape_rainfall.rainfall)
	geometries = np.array(shape_rainfall.geometry)	
	df_rainfall = pd.DataFrame({"Dist Name" : district_name, "Rainfall(mm)" : rainfall, "Geometry" : geometries})
	j=1
	for row in df_rainfall.itertuples():
		#print x,y,' searching in polygon no ',j
		poly = ogr.CreateGeometryFromWkt(str(row[2]))
		#print row[3] #its contains the rain fall amount
		rainfall_amount = row[3]
		district_name = row[1]
		#print poly,'\n\n'
		ring = poly.GetGeometryRef(0)
		#print ring
		points = ring.GetPointCount()
		#print points
		
		coords = []
		
		#adding all coords of a polygon to an array
		for i in range(0, ring.GetPointCount()):
			pt = ring.GetPoint(i)
			#print int(i+1), pt[1], pt[0] 			
			coords.append((pt[1], pt[0]))
			#x = pt[1] #float(25.5) 
			#y = pt[0] #float(84.7) 
				
		#coords = [(24.950899, 60.169158), (24.953492, 60.169158), (24.953510, 60.170104), (24.950958, 60.169990)]
		#print coords
		
		################# Using inline ################# 
		point = Point(x,y)
		from shapely.geometry import Polygon
		try:
			polly = Polygon(coords)
			#print 'Using onliner: ', point, polly.contains(point)
			is_inside = polly.contains(point)
			
			if (is_inside == True):
				#print point, is_inside, 'Found in polygon no',j
				break
		except:
			pass
		j+=1
	if (is_inside == True):
		return rainfall_amount, district_name
	else:
		return 0, 'NA'
		
		################# Using method calling ################# 
		#is_inside = inside_polygon(x, y, coords)
		#print 'Using method: ', x, y , is_inside
		
		#break
		

		
def main():

	file_waterbody = '/home/abhisek/Documents/abhisek-workspace/codes/twitter/data-pull/dataset/water_bodies/Bihar Waterbodies/water_bodies_bihar.shp'
	
	file_latlons = '/home/abhisek/Documents/abhisek-workspace/codes/twitter/extract_place/latlons-kolkata-20170724-20170913.csv'
	df_latlon = pd.read_csv(file_latlons)
	
	file_rainfall = '/home/abhisek/Documents/abhisek-workspace/codes/twitter/data-pull/dataset/Rainfall Data Collection/shape/bihar-rainfall-2017.shp'	
	
	#df_rainfall.to_csv("/home/abhisek/Documents/abhisek-workspace/codes/twitter/data-pull/dataset/Rainfall Data Collection/shape/bihar-rainfall-aug17-processed.csv", index=False)	
	
	print 'x, y, distance, elevation, rainfall, district'
	
	for row in df_latlon.itertuples():
		#print row[1] , row[2]
		neighborhoods = findNeighbourhood(row[1], row[2], 0.034)
		for n in neighborhoods:
			p = ogr.CreateGeometryFromWkt(str(n))
			#print p
			elev = getPointsElevation(p.GetY(), p.GetX())
			if(elev != 999999) :
				dist = getDistanceFromWaterbodies(n, file_waterbody)
				rainfall_amount , district_name = getRainfall(p.GetX(), p.GetY(), file_rainfall)
				print p.GetX() ,',', p.GetY() ,',', dist,',', elev , ',' , rainfall_amount , ',', district_name
			else:
				pass
				#print elev




if __name__=='__main__':

	main()
	
	

	
	
	
	
	
	
	
	


	

