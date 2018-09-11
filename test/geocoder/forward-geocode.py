#reference : https://github.com/DenisCarriere/geocoder

import geocoder
#g = geocoder.google('Mountain View, CA')
g = geocoder.google('Midnapore')

print('\nlatlng')
print(g.latlng)
#(37.3860517, -122.0838511)

#print('\ngeojson')
#print(g.geojson)

#print('\njson')
#print(g.json)

#print('\nwkt')
#print(g.wkt)

#print('\nosm')
#print(g.osm)
