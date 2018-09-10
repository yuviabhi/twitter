#This code is used to save the all the convex hull into a shape files

#not working 

'''
ERROR 1: polygon.shp is not a directory.

'NoneType' object has no attribute 'CreateLayer'

'''

from osgeo import gdal,ogr

def create_polygon(coords):          
    ring = ogr.Geometry(ogr.wkbLinearRing)
    for coord in coords:
        ring.AddPoint(coord[0], coord[1])

    # Create polygon
    poly = ogr.Geometry(ogr.wkbPolygon)
    poly.AddGeometry(ring)
    return poly.ExportToWkt()

def write_shapefile(poly, out_shp):
    """
    https://gis.stackexchange.com/a/52708/8104
    """
    try:
			# Now convert it to a shapefile with OGR    
			driver = ogr.GetDriverByName('ESRI Shapefile')
			
			ds = driver.CreateDataSource(out_shp)
			layer = ds.CreateLayer('', None, ogr.wkbPolygon)


			# Add one attribute
			layer.CreateField(ogr.FieldDefn('id', ogr.OFTInteger))
			defn = layer.GetLayerDefn()

			## If there are multiple geometries, put the "for" loop here

			# Create a new feature (attribute and geometry)
			feat = ogr.Feature(defn)
			feat.SetField('id', 123)

			# Make a geometry, from Shapely object
			#geom = ogr.CreateGeometryFromWkb(poly.wkb)
			geom = ogr.CreateGeometryFromWkt(poly)
			feat.SetGeometry(geom)

			layer.CreateFeature(feat)
			feat = geom = None  # destroy these

			# Save and close everything
			ds = layer = feat = geom = None

    except Exception,e:
  		print e
  		pass
def main(coords, out_shp):
    poly = create_polygon(coords)
    write_shapefile(poly, out_shp)

if __name__ == "__main__":
    coords = [(-106.6472953, 24.0370137), (-106.4933356, 24.05293569), (-106.4941789, 24.01969175), (-106.4927777, 23.98804445), (-106.4922614, 23.95582128), (-106.4925834, 23.92302327), (-106.4924068, 23.89048039), (-106.4925695, 23.85771361), (-106.4932479, 23.82457675), (-106.4928676, 23.7922049), (-106.4925072, 23.75980241), (-106.492388, 23.72722475), (-106.4922574, 23.69464296), (-106.4921181, 23.6620529), (-106.4922734, 23.62926733), (-106.4917201, 23.59697561), (-106.4914134, 23.56449628), (-106.4912558, 23.5319045), (-106.491146, 23.49926362), (-106.4911734, 23.46653561), (-106.4910181, 23.43392476), (-106.4910156, 23.40119976), (-106.4909501, 23.3685223), (-106.4908165, 23.33586566), (-106.4907735, 23.30314904), (-106.4906954, 23.27044931), (-106.4906366, 23.23771759), (-106.4905894, 23.20499124), (-106.4905432, 23.17226022), (-106.4904748, 23.1395177), (-106.4904187, 23.10676788), (-106.4903676, 23.07401321), (-106.4903098, 23.04126832), (-106.4902512, 23.00849426), (-106.4901979, 22.97572025), (-106.490196, 22.97401001), (-106.6481193, 22.95609832), (-106.6481156, 22.95801668), (-106.6480697, 22.99082052), (-106.6480307, 23.02362441), (-106.6479937, 23.0563977), (-106.6479473, 23.0891833), (-106.647902, 23.12196713), (-106.6478733, 23.15474057), (-106.6478237, 23.18750353), (-106.6477752, 23.22026138), (-106.6477389, 23.25302505), (-106.647701, 23.28577123), (-106.6476562, 23.31851549), (-106.6476211, 23.3512557), (-106.6475745, 23.38397935), (-106.6475231, 23.41671055), (-106.6474863, 23.44942382), (-106.6474432, 23.48213255), (-106.6474017, 23.51484861), (-106.6474626, 23.54747418), (-106.647766, 23.57991134), (-106.6482374, 23.61220905), (-106.6484783, 23.64467084), (-106.6482308, 23.6775148), (-106.6479338, 23.7103854), (-106.6478395, 23.74309074), (-106.6472376, 23.77618646), (-106.6472982, 23.80876072), (-106.647127, 23.84151129), (-106.6471277, 23.8741312), (-106.6473995, 23.90656505), (-106.6473138, 23.93916488), (-106.6473408, 23.97172031), (-106.6473796, 24.00435261), (-106.6472953, 24.0370137)]
    out_shp = r'polygon.shp'
    main(coords, out_shp)
