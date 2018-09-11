
#### CONVERT GEOJSON TO POLYGONS

import pygeoj
import string

testfile = pygeoj.load(filepath="news-report-bihar.geojson")

for feature in testfile:
	multipolygon = feature.geometry.coordinates
	for polygon in multipolygon :
		for p in polygon :
			p = str(p)
			p = string.replace(p, '[[', '((')
			p = string.replace(p, ']]', '))')
			p = string.replace(p, ',', '#')
			p = string.replace(p, ']#', ',')
			p = string.replace(p, '[', ' ')
			p = string.replace(p, '#', ' ')			
			print 'POLYGON',p
	#break

