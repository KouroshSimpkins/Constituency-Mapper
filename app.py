from flask import Flask, render_template, request, jsonify
from flask import Flask
import mysql.connector
from mysql.connector import errorcode
from dbInteraction import init_db

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def test_app_root():
    """
    Default table route, shows the database with tickboxes to mark visited roads.

    :return: A rendered HTML template with the database Geojson_data.
    :rtype: flask.Response
    """

    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='change-me',
            database='Test_DB_Zero',
        )
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Invalid username or password")
        else:
            print(f"Error connecting to the MySQL server: {err}")
        exit(1)

    cursor = conn.cursor()

    if request.method == 'POST':
        updated_roads = request.form.getlist('visited')
        visited_by = request.form.getlist('leafletter')[0]
        print("POST called: ", updated_roads, flush=True)
        print("visited_by: ", visited_by, flush=True)

        # cursor.execute("UPDATE Roads SET Visited = 0")
        for road_id in updated_roads:
            print("road_id:", road_id, flush=True)
            cursor.execute("UPDATE Roads SET visited = true, visited_by=%s WHERE road_id = %s", (visited_by, road_id,))
        conn.commit()

    query = ("SELECT r.road_id, r.road_name, "
    "CASE WHEN r.visited = 1 THEN 'Yes' ELSE 'No' END AS visited, "
    "COALESCE(l.username, '-') AS username "
    "FROM Roads as r "
    "LEFT JOIN Leafletters as l "
    "ON l.user_id = r.visited_by "
    "ORDER BY r.road_name")
    cursor.execute(query)
    rows = cursor.fetchall()

    cursor.execute("SELECT * from Leafletters")
    leafletters = cursor.fetchall()
    conn.close()
    return render_template('index.html', rows=rows, leafletters=leafletters)


# The route for showing an interactive map that draws from the database in the previous page.
@app.route('/map')
def test_app_map():
    return "Map page"

# Initialize the database
@app.route('/initdb', methods=['POST'])
def post_endpoint():
    init_db()
    return jsonify({'message': 'Success'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4000)
