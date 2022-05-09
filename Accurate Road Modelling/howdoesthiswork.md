How does this work?
-------------------


* OSMnetwork/osmlinks.py gets the accurate road network data from overpass server and turns the osm data into a graph(?) of nodes and ways (or links) (with data about road type / one way/ length attached)
* BCMnetwork/createnetworklink.py file grabs data from the shape file model and puts it into an easy to use form
* closest.py file finds the closest points on the real network to those on the map
		* Uses pythagoras theorum to find closest (mostly) nodes on the OSM maps to the ones on the BCM map. Did this a very lazy way, so it's slow - could be sped up signifincaly with an r-tree
		* filters the data to only use the ones going in a similar direction (within 80 degrees) and weights the results slightly towards major roads towards major roads
		* removes roads that are too long or too far away (100m) from the base map.
		* calculates the shortest paths - this is the actual work. runs dijkstra's shortest path algorithm to find the roads.
* drawit.py plots it all out, (offsetting the lines on 2 way roads a bit so they don't cover each other)
	*  with folium (test.html)
	*  maybe just as a png (not done this yet)
* get data from original files and match


