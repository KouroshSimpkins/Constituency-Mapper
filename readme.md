# Leaflet Mapper
Constituency Mapper is a Flask-based application designed to manage and visualize constituency data using a MySQL database and Overpass API. The application allows users to mark roads as visited and track leafletters.

## Key Features
- **Interactive Map and Database Integration:** Visualize and manage constituency data, including roads and their visited status.
- **Leafletter Management:** Track activities of leafletters visiting various roads.

## Key Functionality

**1. Display Constituencies and Roads:**
The root route (/) displays a table of roads within a specified constituency. Users can mark roads as visited.

**2. Display Map:** The /map route displays an interactive map of the constituency, showing the roads and their statuses.

## Getting Started

### Prerequisites
- **Python 3.12**

- **MySQL server** - We recommend using Docker to run a MySQL server for development purposes.

- **Poetry**

## Installation Steps - Development

If you want to contribute to this project, please ensure you have the prerequisite software installed.

**1. Install Prerequisites:**

To ensure you can get developing as quickly as possible, ensure you have all the requirements installed as outlined in the
"prerequisites" section.

**2. Clone the Repository:**
```
git clone https://github.com/KouroshSimpkins/Constituency-Mapper.git
cd constituency-mapper
```

**3. Install Dependencies:**

The dependencies are different to the prerequisites, you can view them by looking at the pyproject.toml file.

Ensure you have Poetry installed, then run:
```
poetry install
```

**4. Set Up MySQL Database:**

Ensure your MySQL server is running on localhost.

>We highly recommend running Docker in a mysql container when developing.

**5. Initialize the Database:**

Start the Flask application.
```
python app.py
```
Then, open a browser and navigate to http://localhost:4000/inittestdb to initialize the database.

## future dev

The current upgrade focus is on moving the development containers to a single docker compose file to streamline development.
This feature should be ready by the end of October, so for ease and consistency, if you don't already have an environment set up it is best to wait before contributing!

After compose has been set up we will be deploying a development server to enable us to perform integration testing, as well as enabling some initial "field tests" of the software.

## Usage
- Access the application by navigating to http://localhost:4000 in your web browser.
- Use the default route to view and update the roads' visited status.
- Use the /map route to view the interactive map.

## Authors
- Kourosh Simpkins kouroshsimpkins@gmail.com
- Erdinc Mutlu erdincmutlu@gmail.com
