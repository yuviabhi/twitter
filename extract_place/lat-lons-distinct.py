
'''
Count distinct lat lons with frequency from file latlons-kolkata-20170724-20170823.csv

Run : python lat-lons-distinct.py
'''

import sys
import pandas as pd

#location = str(sys.argv[1])
#file_name = str(sys.argv[2])

x = pd.read_csv('latlons-kolkata-20170724-20170913.csv')
output_file = 'latlons-distinct-20170724-20170913.csv'

#print x.head()

##################################################
#### COUNTING FREQUENCIES OF DISTINCT LATLONS ####
##################################################

dis = pd.DataFrame()
dis = x['lat'].map(str) + ',' + x['lon'].map(str)
#print dis.head()

dis_values = dis.value_counts()
print dis_values

new = pd.DataFrame()
new['count'] = dis_values

new.to_csv(output_file,encoding='utf-8',index=False)



