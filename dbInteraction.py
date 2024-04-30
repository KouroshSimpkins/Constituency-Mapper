# Acts as a go between for the database and the OpenStreetMap street names.

import mysql.connector
import geojson
from GEOJSONtoPOLYGON import generate_overpass_queries
import requests


all_queries = generate_overpass_queries('Geojson_data/2010_constituencies___england__south_.geojson')
london_westminster_query = list(filter(lambda q: q['Name'] == 'Cities of London & Westminster', all_queries))


def query_overpass_api(overpass_query):
    """
    Query the Overpass API and return the results.

    :param: overpass_query (str): The Overpass API query to be executed.

    :return: The JSON response from the Overpass API.
    :rtype: dict
    """

    # Preparing the Overpass API endpoint
    overpass_url = 'https://overpass-api.de/api/interpreter'

    response = requests.get(overpass_url, data={'data': overpass_query})

    if response.status_code != 200:
        raise Exception(f"Error querying Overpass API: {response.status_code}")

    return response.json()


def extract_street_names(overpass_response):
    """
    Extracts street names from an Overpass API response.

    :param overpass_response: The response dictionary from the Overpass API.

    :return: A list of street names.
    :rtype: List
    """

    street_names_set = set()

    for element in overpass_response.get("elements", []):
        if element.get("tags", {}).get("highway"):
            street_name = element.get("tags", {}).get("name")
            street_names_set.add(street_name)

    return list(street_names_set)


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
