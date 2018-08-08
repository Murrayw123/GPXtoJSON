#!/usr/bin/env python

import gpxpy
import gpxpy.gpx
import json
import os


print("GPX to GeoJSON")

gpx_file = open('FULL PATH TO GPX', 'r') #the gpx file you want to parse
parsed_file = open('FULL PATH TO JSON FILE', 'w') #final output file
tmp_file = open('gpxparse.tmp', 'w') # don't touch this
gpx = gpxpy.parse(gpx_file)
points = []
linestring = []

tmp_file.write(""" { "type": "FeatureCollection", "features":[ """) # follows GEOJSON spec. FeatureCollection -> Feature
for track in gpx.tracks:
    for i, segment in enumerate(track.segments): # loops through the different segments in a GPX track and assigns them to different features
        tmp_file.write(""" {{ "type": "Feature",  "properties": {{ "Segment ID": {0} }}, """.format(i))
        print("New Segment:", i)
        for l, point in enumerate(segment.points):
            linestring.append([point.longitude, point.latitude])
        tmp_file.write(""" "geometry": {{ "type": "LineString", "coordinates":{0} }} }}""".format(linestring))
        try: # if there is another segment, keep on adding them, catches an index error which means EOF
            if track.segments[i+1]:
                tmp_file.write(",")
        except IndexError:
            print("Segments Parsed")
            tmp_file.write("]")
        linestring = []
tmp_file.write("}")
tmp_file.close()
print("finished parsing coordinates")

print("now formatting JSON")
obj = None
with open('gpxparse.tmp') as f:
    obj = json.load(f)
parsed_file.write(json.dumps(obj, indent=4))
tmp_file.close()
os.remove("gpxparse.tmp")
print("File Parsed")



