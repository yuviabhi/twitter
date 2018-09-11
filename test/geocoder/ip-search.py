import geocoder

#g = geocoder.ip('199.7.157.0')
g = geocoder.ip('me')
print(g.latlng)
print(g.city)
