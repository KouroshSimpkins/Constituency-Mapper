import geojson


def generate_overpass_queries(file_path):
    """
    Generates Overpass API queries for each constituency described in a GeoJSON file.

    :argument: file_path (str): The path to the GeoJSON file.

    :return: List of dictionaries containing constituency names and Overpass API queries.
    :rtype: List[dict]
    """

    # Load the GeoJSON file
    with open(file_path, 'r') as f:
        geojson_data = geojson.load(f)

    # List to store the parsed constituencies and queries
    constituencies = []

    for feature in geojson_data['features']:
        properties = feature['properties']
        geometry = feature['geometry']

        # Store constituency information
        constituency_data = {
            'Name': properties.get('Name'),
            'geometry_type': geometry['type'],
            'coordinates': geometry['coordinates']
        }

        constituencies.append(constituency_data)

    # List to store Overpass queries
    overpass_queries = []

    for constituency in constituencies:
        # Adjust based on the structure of the GeoJSON geometry data
        polygon_coordinates = constituency['coordinates'][0][0]

        # Convert coordinates to Overpass API format
        polygon_string = " ".join(f"{lat} {lon}" for lon, lat in polygon_coordinates)

        # Format the Overpass object
        overpass_query = f"""
        [out:json];
        way(poly:"{polygon_string}")[highway];
        (._;>;);
        out body;
        """

        overpass_data = {
            'Name': constituency['Name'],
            'object': overpass_query
        }

        overpass_queries.append(overpass_data)

    return overpass_queries

# Example usage:
# queries = generate_overpass_queries('/path/to/geojson/file')
# for q in queries:
#     print(q)
