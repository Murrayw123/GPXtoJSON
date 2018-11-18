#!/usr/bin/env python

import gpxpy
import gpxpy.gpx
import json
import os


print("GPX to GeoJSON")

gpx_file = open('/home/murray/Downloads/mundabiddiwithelevation.gpx', 'r') #the gpx file you want to parse
network = open('network2.json', 'w') # don't touch this
gpx = gpxpy.parse(gpx_file)
points = []
linestring = []

network.write("""{"type":"FeatureCollection","features":[""") # follows GEOJSON spec. FeatureCollection -> Feature
for track in gpx.tracks:
    for i, segment in enumerate(track.segments): # loops through the different segments in a GPX track and assigns them to different features
        network.write(""" {{ "type":"Feature","properties":{{"ID":{0}}},""".format(i))
        print("New Segment:", i)
        for l, point in enumerate(segment.points):
            print(point)
            if l % 2 == 0 or segment.points[0] == point or segment.points[-1] == point:
                linestring.append([round(point.longitude, 5), round(point.latitude, 5), point.elevation])
        network.write(""" "geometry": {{ "type": "LineString", "coordinates":{0} }} }}""".format(linestring))
        try: # if there is another segment, keep on adding them, catches an index error which means EOF
            if track.segments[i+1]:
                network.write(",")
        except IndexError:
            print("Segments Parsed")
            network.write("]")
        linestring = []
network.write("}")
network.close()
print("finished parsing coordinates")



# print("now formatting JSON")
# obj = None
# with open('gpxparse.tmp') as f:
#     obj = json.load(f)
# parsed_file.write(json.dumps(obj, indent=4))
# tmp_file.close()
# os.remove("gpxparse.tmp")
# print("File Parsed")



