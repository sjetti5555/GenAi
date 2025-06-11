import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from itertools import islice

# Load the airports data
airports = {
    'New York': ('JFK', -73.7781, 40.6413), 'London': ('LHR', -0.4614, 51.4700),
    'Paris': ('CDG', 2.5479, 49.0097), 'Frankfurt': ('FRA', 8.5622, 50.0379),
    'Amsterdam': ('AMS', 4.7683, 52.3105), 'Dubai': ('DXB', 55.3647, 25.2532),
    'Singapore': ('SIN', 103.9915, 1.3644), 'Hong Kong': ('HKG', 113.9145, 22.3080),
    'Tokyo': ('NRT', 140.3929, 35.7720), 'Sydney': ('SYD', 151.1772, -33.9462),
    'Los Angeles': ('LAX', -118.4085, 33.9416), 'Chicago': ('ORD', -87.9073, 41.9742),
    'Toronto': ('YYZ', -79.6248, 43.6777), 'Madrid': ('MAD', -3.5673, 40.4839),
    'Rome': ('FCO', 12.2389, 41.8003), 'Istanbul': ('IST', 28.8141, 40.9769),
    'Bangkok': ('BKK', 100.7501, 13.6900), 'Delhi': ('DEL', 77.1025, 28.5562),
    'Johannesburg': ('JNB', 28.2460, -26.1367), 'Sao Paulo': ('GRU', -46.4730, -23.4356),
    'Mexico City': ('MEX', -99.0721, 19.4361), 'Beijing': ('PEK', 116.5975, 40.0801),
    'Moscow': ('SVO', 37.4146, 55.9726), 'Jakarta': ('CGK', 106.6558, -6.1256),
    'Manila': ('MNL', 121.0198, 14.5086), 'Cairo': ('CAI', 31.4056, 30.1219),
    'Kuala Lumpur': ('KUL', 101.7101, 2.7456), 'Lagos': ('LOS', 3.3212, 6.5774),
    'Barcelona': ('BCN', 2.0785, 41.2971), 'Munich': ('MUC', 11.7861, 48.3537),
    'Zurich': ('ZRH', 8.5491, 47.4647), 'Vienna': ('VIE', 16.5697, 48.1102),
    'Copenhagen': ('CPH', 12.6561, 55.6181), 'Oslo': ('OSL', 11.1003, 60.1975),
    'Stockholm': ('ARN', 17.9237, 59.6498), 'Helsinki': ('HEL', 24.9675, 60.3172),
    'Warsaw': ('WAW', 20.9679, 52.1672), 'Budapest': ('BUD', 19.2556, 47.4390),
    'Athens': ('ATH', 23.9445, 37.9364), 'Lisbon': ('LIS', -9.1359, 38.7813),
    'Prague': ('PRG', 14.2632, 50.1008), 'Brussels': ('BRU', 4.4844, 50.9014),
    'Geneva': ('GVA', 6.1092, 46.2370), 'Edinburgh': ('EDI', -3.3725, 55.9501),
    'Manchester': ('MAN', -2.2750, 53.3619), 'Dublin': ('DUB', -6.2499, 53.4264),
    'Hamburg': ('HAM', 9.9917, 53.6332), 'Stuttgart': ('STR', 9.2216, 48.6862)
}

# Create a case-insensitive lookup for city names
city_lookup = {city.lower(): city for city in airports.keys()}

# Read the CSV file
df = pd.read_csv('data/FlightDatabase.csv')

# Create a set of unique cities in the database
db_cities = set(df['Source'].unique()) | set(df['Destination'].unique())

# Update city_lookup with cities from the database
for city in db_cities:
    city_lookup[city.lower()] = city

# Create a graph
G = nx.from_pandas_edgelist(df, 'Source', 'Destination', ['Airline', 'Flight', 'Departure Time', 'Duration (mins)', 'Price ($)', 'Stops'], create_using=nx.DiGraph())

def find_routes(G, origin, destination, max_stops=3, max_routes=5):
    paths = nx.shortest_simple_paths(G, origin, destination)
    routes = list(islice((p for p in paths if len(p) <= max_stops + 2), max_routes))
    return routes

def get_route_details(G, route):
    details = []
    total_duration = 0
    total_price = 0
    stops = len(route) - 2
    for i in range(len(route) - 1):
        edge_data = G.get_edge_data(route[i], route[i+1])
        details.append(f"{route[i]} -> {route[i+1]}: {edge_data['Airline']} {edge_data['Flight']}")
        details.append(f"  Departure: {edge_data['Departure Time']}")
        details.append(f"  Duration: {edge_data['Duration (mins)']} mins")
        details.append(f"  Price: ${edge_data['Price ($)']}")
        total_duration += edge_data['Duration (mins)']
        total_price += edge_data['Price ($)']
    details.append(f"Total Duration: {total_duration} mins")
    details.append(f"Total Price: ${total_price}")
    return details, total_duration, total_price, stops

def plot_routes(origin, destination):
    routes = find_routes(G, origin, destination)
    
    fig = plt.figure(figsize=(20, 10))
    
    # Map subplot
    ax_map = fig.add_subplot(1, 2, 1, projection=ccrs.Robinson())
    ax_map.set_global()
    ax_map.add_feature(cfeature.LAND)
    ax_map.add_feature(cfeature.OCEAN)
    ax_map.add_feature(cfeature.COASTLINE)
    ax_map.add_feature(cfeature.BORDERS, linestyle=':')

    # Plot all airports
    for code, (city, lon, lat) in airports.items():
        ax_map.plot(lon, lat, 'ro', markersize=5, transform=ccrs.Geodetic())
        ax_map.text(lon, lat, code, fontsize=8, ha='right', va='bottom', transform=ccrs.Geodetic())

    # Plot routes
    colors = ['r', 'g', 'b', 'c', 'm']
    route_info = []
    for i, route in enumerate(routes):
        route_coords = [airports[airport][1:] for airport in route]
        ax_map.plot([coord[0] for coord in route_coords], [coord[1] for coord in route_coords], 
                color=colors[i], linewidth=2, transform=ccrs.Geodetic(), 
                label=f'Route {i+1} ({len(route)-1} stops)')

        # Add intermediate airport labels
        for airport in route[1:-1]:
            lon, lat = airports[airport][1:]
            ax_map.text(lon, lat, airport, fontsize=8, ha='left', va='bottom', transform=ccrs.Geodetic())
        
        details, duration, price, stops = get_route_details(G, route)
        route_info.append((i+1, duration, price, stops, details))

    ax_map.set_title(f'Flight Routes from {origin} to {destination}')
    ax_map.legend()

    # Route details subplot
    ax_details = fig.add_subplot(1, 2, 2)
    ax_details.axis('off')
    
    details_text = f"Routes from {origin} to {destination}:\n\n"
    
    # Find the cheapest, fastest, and least stops routes
    cheapest = min(route_info, key=lambda x: x[2])
    fastest = min(route_info, key=lambda x: x[1])
    least_stops = min(route_info, key=lambda x: x[3])
    
    highlights = {
        "Cheapest": cheapest,
        "Fastest": fastest,
        "Least Stops": least_stops
    }
    
    for label, (route_num, duration, price, stops, details) in highlights.items():
        details_text += f"{label} Route (Route {route_num}):\n"
        details_text += f"  Duration: {duration} mins\n"
        details_text += f"  Price: ${price}\n"
        details_text += f"  Stops: {stops}\n\n"
    
    details_text += "All Routes:\n\n"
    for route_num, duration, price, stops, details in route_info:
        details_text += f"Route {route_num} ({stops} stops):\n"
        details_text += "\n".join(details)
        details_text += "\n\n"
    
    ax_details.text(0, 1, details_text, va='top', ha='left', fontsize=8)

    plt.tight_layout()
    plt.show()

# Get user input
origin_city = input("Enter origin city: ").lower()
destination_city = input("Enter destination city: ").lower()

# Validate input and get correct city names
origin = city_lookup.get(origin_city)
destination = city_lookup.get(destination_city)

# Validate input
if origin is None or destination is None:
    print("Invalid city name(s). Please enter valid city names.")
else:
    if origin not in G.nodes() or destination not in G.nodes():
        print(f"No routes found between {origin} and {destination}.")
    else:
        plot_routes(origin, destination)