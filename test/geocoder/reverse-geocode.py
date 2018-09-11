import geocoder
g = geocoder.google([22.3145, 87.3091], method='reverse')

print('\ncity')
print(g.city)

print('\nstate')
print(g.state)

print('\nstate_long')
print(g.state_long)

print('\ncountry')
print(g.country)

print('\ncountry_long')
print(g.country_long)
