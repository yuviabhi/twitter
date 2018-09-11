

from osgeo import ogr

fname = '/home/abhisek/Documents/abhisek-workspace/codes/twitter/dbscan/convex_hull_boundary_kolkata_20170724-20170913-eps_0.1_minsamples_6.csv'


with open(fname, "r") as file:
    lines = file.read().split("\n")
    #print lines


for line in lines:

	poly = ogr.CreateGeometryFromWkt(line)
	print poly

	ring = poly.GetGeometryRef(0)
	#print ring.GetGeometryName()
	#print ring.GetPointCount()
	for i in range(0,ring.GetPointCount()) :
		pt= ring.GetPoint(i)
		print "%i). POINT (%f %f)" %(i, pt[0], pt[1])

	#break





