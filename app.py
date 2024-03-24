from flask import Flask, flash, redirect, render_template, request, session, abort
from flask import Flask
import sqlite3
import os

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def test_app_root():
    """
    Default table route, shows the database with tickboxes to mark visited roads.

    :return: A rendered HTML template with the database data.
    :rtype: flask.Response
    """
    conn = sqlite3.connect('ConstituencyMapperDB')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    if request.method == 'POST':
        updated_roads = request.form.getlist('visited_roads')
        cursor.execute("UPDATE Roads SET Visited = 0")
        for road_id in updated_roads:
            cursor.execute("UPDATE Roads SET Visited = 1 WHERE id = ?", (road_id,))
        conn.commit()

    cursor.execute("SELECT * FROM Roads")
    rows = cursor.fetchall()
    conn.close()

    return render_template('index.html', rows=rows)


# The route for showing an interactive map that draws from the database in the previous page.
@app.route('/map')
def test_app_map():
    return "Map page"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4000)
