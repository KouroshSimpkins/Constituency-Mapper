# Acts as a go between for the database and the OpenStreetMap street names.

import mysql.connector
import geojson


with open('test_data.geojson') as f:
    gj = geojson.load(f)


road_names = []
for feature in gj['features']:
    if 'name' in feature['properties']:
        road_names.append(feature['properties']['name'])


road_names = list(dict.fromkeys(road_names))

print(road_names)

try:
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='change-me',
        database='mysql'
    )
    print("Connected to MySQL server")
except mysql.connector.Error as e:
    print(f"Error connecting to MySQL database: {e}")


cursor = conn.cursor()
cursor.execute("SELECT * FROM Roads")
results = cursor.fetchall()
for row in results:
    print(row)

cursor.close()
conn.close()
