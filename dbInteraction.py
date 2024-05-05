# Acts as a go between for the database and the OpenStreetMap street names.

import mysql.connector
from mysql.connector import errorcode
from GEOJSONtoPOLYGON import generate_overpass_queries
import requests


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


# This is redundant as of new database decisions,
# but I'll keep it here for now as it can help me generate test databases.
def generate_constituency_database(test_db_name):
    """
    Generates a database with the name of the constituency,
    to help isolate the data for each parliamentary constituency.

    :param test_db_name:
    :return:
    """

    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='change-me',
        )
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Invalid username or password")
        else:
            print(f"Error connecting to the MySQL server: {err}")
        exit(1)

    cursor = conn.cursor()

    db_name = str(test_db_name)
    try:
        cursor.execute(f"DROP DATABASE {db_name}")
        cursor.execute(f"CREATE DATABASE {db_name}")
        print(f"Database '{db_name}' created successfully.")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_DB_CREATE_EXISTS:
            print(f"Database '{db_name}' already exists.")
        else:
            print(f"Error creating database: {err}")

    cursor.execute(f"USE {db_name}")

    table_queries = [
        "CREATE TABLE Leafletters (user_id CHAR(36) PRIMARY KEY DEFAULT (UUID()), username VARCHAR(40), email_address VARCHAR(100), phone_number VARCHAR(20));" # noqa
        "CREATE TABLE Constituencies (constituency_id CHAR(36) PRIMARY KEY DEFAULT (UUID()), name VARCHAR(255) UNIQUE NOT NULL);" # noqa
        "CREATE TABLE Roads (road_id CHAR(36) PRIMARY KEY DEFAULT (UUID()), road_name VARCHAR(255), last_visited DATETIME, visited BOOLEAN, visited_by CHAR(36), constituency_id CHAR(36), FOREIGN KEY (visited_by) REFERENCES Leafletters(user_id), FOREIGN KEY (constituency_id) REFERENCES Constituencies(constituency_id));" # noqa
        "CREATE TABLE Road_visits (visit_id CHAR(36) PRIMARY KEY DEFAULT (UUID()), road_id CHAR(36) NOT NULL, user_id CHAR(36) NOT NULL, visit_date DATETIME NOT NULL, constituency_id CHAR(36), FOREIGN KEY (road_id) REFERENCES Roads(road_id), FOREIGN KEY (user_id) REFERENCES Leafletters(user_id), FOREIGN KEY (constituency_id) REFERENCES Constituencies(constituency_id));" # noqa
    ]

    for table_query in table_queries:
        try:
            cursor.execute(table_query)
            print(f"Table created successfully.")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print(f"Table already exists.")
            else:
                print(f"Error creating table: {err}")

    cursor.close()
    conn.close()


def connect_to_database(db_name):
    """
    Connect to the specified database.

    :param db_name: The name of the database to connect to.
    :return: The connection and cursor objects.
    """

    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='change-me',
            database=db_name
        )
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Invalid username or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print(f"Database '{db_name}' does not exist")
        else:
            print(f"Error connecting to the MySQL server: {err}")
        exit(1)

    cursor = conn.cursor(buffered=True)

    return conn, cursor


def load_constituencies_to_database(db_name, region_file_path):
    """
    Load the constituencies into the database. Generally this is just done once per region,
    but the function is here for maintenance purposes.

    :param db_name: The name of the database to load the constituencies into.
    :param region_file_path: The path to a geojson file containing the constituency boundaries.
    :return:
    """

    conn, cursor = connect_to_database(db_name)
    queries = generate_overpass_queries(region_file_path)

    constituency_names = set()

    for query in queries:
        constituency_names.add(query['Name'])

    for constituency_name in constituency_names:
        cursor.execute("INSERT INTO Constituencies (name) VALUES (%s)", (constituency_name,)) # noqa
        print(cursor.rowcount, "record inserted.")

    conn.commit()
    cursor.close()

def create_leafletters(db_name, names):
    """
    Create leafletters in the database

    :param db_name: The name of the database
    :param names: The list of names of leafletters
    :return:
    """

    conn, cursor = connect_to_database(db_name)
    for name in names:
        cursor.execute("INSERT INTO Leafletters (username) VALUES (%s)", (name,))
        print(cursor.rowcount, "record inserted.")

    conn.commit()
    cursor.close()

if __name__ == '__main__':
    all_queries = generate_overpass_queries('Geojson_data/2010_constituencies___england__south_.geojson')
    london_westminster_query = list(filter(lambda q: q['Name'] == 'Cities of London & Westminster', all_queries))

    overpass_response_ = query_overpass_api(london_westminster_query[0]['object'])
    street_names_list = extract_street_names(overpass_response_)

    conn, cursor = connect_to_database('Test_DB_Zero')
    print(conn)

    cursor.execute("SELECT constituency_id FROM Constituencies WHERE name = 'Cities of London & Westminster'") # noqa
    constituency_id = cursor.fetchone()[0]
    print(constituency_id)

    for road_name in street_names_list:
        cursor.execute("INSERT INTO Roads (road_name, constituency_id) VALUES (%s, %s)", (road_name, constituency_id)) # noqa
        print(cursor.rowcount, "record inserted.")
        print(cursor.lastrowid)

    conn.commit()
    cursor.close()

def init_db():
    region_file_path = 'Geojson_data/2010_constituencies___england__south_.geojson'
    db_name= 'Test_DB_Zero'
    generate_constituency_database(db_name)
    load_constituencies_to_database(db_name, region_file_path)

    leafletters_names = ['alice', 'bob', 'charlie']
    create_leafletters(db_name, leafletters_names)

    all_queries = generate_overpass_queries('Geojson_data/2010_constituencies___england__south_.geojson')
    london_westminster_query = list(filter(lambda q: q['Name'] == 'Cities of London & Westminster', all_queries))

    overpass_response_ = query_overpass_api(london_westminster_query[0]['object'])
    street_names_list = extract_street_names(overpass_response_)

    conn, cursor = connect_to_database('Test_DB_Zero')

    cursor.execute("SELECT constituency_id FROM Constituencies WHERE name = 'Cities of London & Westminster'") # noqa
    constituency_id = cursor.fetchone()[0]

    for road_name in street_names_list:
        cursor.execute("INSERT INTO Roads (road_name, constituency_id) VALUES (%s, %s)", (road_name, constituency_id)) # noqa
        print(cursor.rowcount, "record inserted.")
        print(cursor.lastrowid)

    conn.commit()
    cursor.close()
