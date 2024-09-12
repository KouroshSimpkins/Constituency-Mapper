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
- Python 3.12

- MySQL server

- Poetry

## Installation Steps

**1. Clone the Repository:**
```
git clone https://github.com/KouroshSimpkins/Constituency-Mapper.git
cd constituency-mapper
```

**2. Install Dependencies:**

Ensure you have Poetry installed, then run:
```
poetry install
```

**3. Set Up MySQL Database:**

Ensure your MySQL server is running on localhost. 

**4. Initialize the Database:**

Start the Flask application.
```
flask -m app run
```
Then, open a browser and navigate to http://localhost:4000/initdb to initialize the database.

## Usage
- Access the application by navigating to http://localhost:4000 in your web browser.
- Use the default route to view and update the roads' visited status.
- Use the /map route to view the interactive map.

## Authors
- Kourosh Simpkins kouroshsimpkins@gmail.com
- Erdinc Mutlu erdincmutlu@gmail.com
