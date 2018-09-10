
#Create Buffer area of waterbodies

from shapely.geometry import mapping, shape
from fiona import collection

def create_buffer(f_input, f_output, buffer_amount) :
	with collection(f_input, "r") as input:
	    #schema = input.schema.copy()
	    schema = { 'geometry': 'Polygon', 'properties': { 'name': 'str' } }
	    with collection(
		  f_output, "w", "ESRI Shapefile", schema) as output:
		  for polygon in input:
		  	#print shape(polygon['geometry'])
		      output.write({
		          'properties': {
		              'name': polygon['properties']
		          },
		          'geometry': mapping(shape(polygon['geometry']).buffer(buffer_amount))
		      })
		)
            
            
if __name__ == '__main__' :
	
	testing = 1
	
	if(testing == 1):	
		#TEST FILE
		f_input = "e083n24e.shp"
		f_output = "e083n24e-buffer.shp"
	else :
		#Bihar Waterbodies 
		f_input = "/home/abhisek/Documents/abhisek-workspace/codes/twitter/data-pull/dataset/water_bodies/Bihar Waterbodies/water_bodies_bihar.shp"
		f_output = "water_bodies_bihar-buffer.shp"
	
	create_buffer(f_input, f_output, buffer_amount = 0.009)

