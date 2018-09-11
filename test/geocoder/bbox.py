import geocoder

print('\nOTTAWA')
g = geocoder.google("Ottawa")
print(g.bbox)
#{"northeast": [45.53453, -75.2465979], "southwest": [44.962733, -76.3539158]}

print(g.geojson['bbox'])
#[-76.3539158, 44.962733, -75.2465979, 45.53453]

print(g.southwest)
#[44.962733, -76.3539158]


print('\nKHARAGPUR, INDIA')
g1 = geocoder.google("Kharagpur")
print(g1.bbox)
#{"northeast": [45.53453, -75.2465979], "southwest": [44.962733, -76.3539158]}

print(g1.geojson['bbox'])
#[-76.3539158, 44.962733, -75.2465979, 45.53453]

print(g1.southwest)
#[44.962733, -76.3539158]
