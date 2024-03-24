# Acts as a go between for the database and the OpenStreetMap street names.

import sqlite3
import geojson

with open('test_data.geojson') as f:
    gj = geojson.load(f)


road_names = []
for feature in gj['features']:
    if 'name' in feature['properties']:
        road_names.append(feature['properties']['name'])


road_names = list(dict.fromkeys(road_names))

print(road_names)

conn = sqlite3.connect('ConstituencyMapperDB')
cursor = conn.cursor()

for name in road_names:
    # print(name)
    cursor.execute("INSERT INTO Roads (RoadName, Visited, VisitedBy) Values (?, 0, '')", (name, ))

conn.commit()
conn.close()
