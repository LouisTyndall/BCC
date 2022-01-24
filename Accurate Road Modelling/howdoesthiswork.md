How does this work?
-------------------


* OSMnetwork/osmlinks.py gets the accurate road network data from overpass server and turns the osm data into a graph(?) of nodes and ways (or links) (with data about road type / one way/ length attached)
* BCMnetwork/createnetworklink.py file grabs data from the shape file model and puts it into an easy to use form
* closest.py file finds the closest points on the real network to those on the map
		* finds the nearest point but only the ones going in a similar direction (within 80 degrees) and weighted towards major roads
		* removes raods that are too long or with no matches
		* calculates the shortest paths - this is the actual work. runs dijkstra's shortest path algorithm to find the roads. (only does first 200 at the moemnt as we are still testing)
* drawit.py plots it all out, (offsetting the lines on 2 way roads nearly, it's ok)
	*  with folium (test.html)
	*  maybe just as a png (not done this yet)


