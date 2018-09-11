'''
CALCULATE DIFFERENCE BETWEEN TWO POLYGONS AND SAVE INTO A NEW FILE

INPUT: 
poly1.shp = News_Flood_Report.shp
bihar_adm2.shp = Bihar_adm2.shp
optimized.shp = Optimized Zone by Elevation

OUTPUT:
diff.shp
'''

import fiona
from shapely.geometry import shape
green = fiona.open("News_Flood_Report.shp")
blue = fiona.open("optimized.shp") 

#print list(green)
#for i,j in zip(list(green),list(blue)):	
#	print j
#print "\n\n\n\n"
#print list(blue)

# test the function difference between green and blue shapefiles
#[not shape(i['geometry']).difference(shape(j['geometry'])).is_empty for i,j in zip(list(green),list(blue))]
#[False, False, False, True]
# control
#for geom in [shape(i['geometry']).difference(shape(j['geometry'])) for i,j in zip(list(green),list(blue))]:
#     print geom
#GEOMETRYCOLLECTION EMPTY
#GEOMETRYCOLLECTION EMPTY
#GEOMETRYCOLLECTION EMPTY
#POLYGON ((-0.0806077747083538 0.6329375155131045, 0.0085568963219002 0.5081069760707490, -0.0816567708381215 0.6025166277498414, -0.1529885076623247 0.5437728444828506, -0.1292856235630944 0.6206937720158269, -0.0806077747083538 0.6329375155131045))

# test the function difference between blue and green shapefiles
#[not shape(i['geometry']).difference(shape(j['geometry'])).is_empty for i,j in zip(list(blue),list(green))]
#[True, False, False, False]
# control
#for geom in [shape(i['geometry']).difference(shape(j['geometry'])) for i,j in zip(list(blue),list(green))]:
#    print geom
#POLYGON ((0.2292711598746081 0.7386363636363635, 0.6691026645768023 0.6691026645768023, 0.2440830721003134 0.7205329153605015, 0.1074843260188087 0.3452978056426331, 0.2292711598746081 0.7386363636363635))
#GEOMETRYCOLLECTION EMPTY
#GEOMETRYCOLLECTION EMPTY
#GEOMETRYCOLLECTION EMPTY

# thus you can write a resulting shapefile withe the differences

from shapely.geometry import mapping
schema = {'geometry': 'Polygon','properties': {'test': 'int'}}
with fiona.open('diff.shp','w','ESRI Shapefile', schema) as e:
     for geom  in [shape(i['geometry']).difference(shape(j['geometry'])) for i,j in zip(list(green),list(blue))]:
         if not geom.is_empty:
		print geom
		e.write({'geometry':mapping(geom), 'properties':{'test':1}})
     '''for geom  in [shape(i['geometry']).difference(shape(j['geometry'])) for i,j in zip(list(blue),list(green))]:
         if not geom.is_empty:
         	print geom	
		e.write({'geometry':mapping(geom), 'properties':{'test':2}})
	'''	

		
