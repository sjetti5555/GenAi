import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# Define airports
airports = {
    'JFK': ('New York', -73.7781, 40.6413), 'LHR': ('London', -0.4614, 51.4700),
    'CDG': ('Paris', 2.5479, 49.0097), 'FRA': ('Frankfurt', 8.5622, 50.0379),
    'AMS': ('Amsterdam', 4.7683, 52.3105), 'DXB': ('Dubai', 55.3647, 25.2532),
    'SIN': ('Singapore', 103.9915, 1.3644), 'HKG': ('Hong Kong', 113.9145, 22.3080),
    'NRT': ('Tokyo', 140.3929, 35.7720), 'SYD': ('Sydney', 151.1772, -33.9462),
    'LAX': ('Los Angeles', -118.4085, 33.9416), 'ORD': ('Chicago', -87.9073, 41.9742),
    'YYZ': ('Toronto', -79.6248, 43.6777), 'MAD': ('Madrid', -3.5673, 40.4839),
    'FCO': ('Rome', 12.2389, 41.8003), 'IST': ('Istanbul', 28.8141, 40.9769),
    'BKK': ('Bangkok', 100.7501, 13.6900), 'DEL': ('Delhi', 77.1025, 28.5562),
    'JNB': ('Johannesburg', 28.2460, -26.1367), 'GRU': ('Sao Paulo', -46.4730, -23.4356)
}

# Define airlines
airlines = [
    'Delta', 'American', 'United', 'Lufthansa', 'Air France', 'British Airways',
    'Emirates', 'Singapore Airlines', 'Cathay Pacific', 'Qantas', 'Air Canada',
    'KLM', 'Turkish Airlines', 'Qatar Airways', 'Etihad', 'ANA', 'Air China',
    'EVA Air', 'Virgin Atlantic', 'LATAM'
]

# Generate 100 rows of flight data
np.random.seed(42)
data = []
for _ in range(100):
    airline = random.choice(airlines)
    source, dest = random.sample(list(airports.keys()), 2)  # Sample 2 distinct airport codes
    flight_num = f"{airline[:2].upper()}{random.randint(1000, 9999)}"
    data.append([airline, flight_num, source, dest])

df = pd.DataFrame(data, columns=['Airline', 'Flight', 'Source', 'Destination'])

# Create a graph
G = nx.from_pandas_edgelist(df, 'Source', 'Destination', ['Airline', 'Flight'], create_using=nx.DiGraph())

# Calculate eigenvector centrality
centrality = nx.eigenvector_centrality(G)

def find_routes(G, origin, destination, num_routes=5):
    all_paths = []
    for path in nx.all_simple_paths(G, origin, destination):
        if len(path) >= 2:  # Ensure at least one stop
            all_paths.append(path)
    
    # Sort paths by length (number of stops)
    all_paths.sort(key=len)
    
    # Select up to num_routes paths, ensuring diversity in the number of stops
    selected_paths = []
    for i in range(min(num_routes, len(all_paths))):
        if i == 0 or len(selected_paths) < num_routes:
            selected_paths.append(all_paths[i])
        elif len(all_paths[i]) > len(selected_paths[-1]):
            selected_paths.append(all_paths[i])
        
        if len(selected_paths) == num_routes:
            break
    
    routes = []
    for path in selected_paths:
        route = []
        for i in range(len(path) - 1):
            edge_data = G.get_edge_data(path[i], path[i+1])
            route.append((path[i], path[i+1], edge_data['Airline'], edge_data['Flight']))
        routes.append(route)
    return routes

def plot_route(origin, destination):
    if origin not in airports or destination not in airports:
        print("Invalid airport code(s)")
        return

    routes = find_routes(G, origin, destination)
    if not routes:
        print(f"No route found from {origin} to {destination}")
        return

    # Find the route with the least stops
    best_route = min(routes, key=len)

    # Print route information in the terminal
    print(f"\nFlight Routes from {origin} to {destination}")
    print("\nBest Route (Least Stops):")
    for start, end, airline, flight in best_route:
        print(f"{start} -> {end}: {airline} {flight}")
    print(f"Total Stops: {len(best_route) - 1}")

    print("\nAll Routes:")
    for i, route in enumerate(routes, 1):
        print(f"\nRoute {i} (Stops: {len(route) - 1}):")
        for start, end, airline, flight in route:
            print(f"  {start} -> {end}: {airline} {flight}")

    fig = plt.figure(figsize=(20, 10))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.Robinson())

    ax.set_global()
    ax.add_feature(cfeature.LAND)
    ax.add_feature(cfeature.OCEAN)
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS, linestyle=':')

    # Plot all airports
    for code, (city, lon, lat) in airports.items():
        ax.text(lon, lat, f"{code}\n{city}", fontsize=8, ha='center', va='center', transform=ccrs.Geodetic(),
                bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))

    # Plot all routes
    colors = plt.cm.Set2(np.linspace(0, 1, len(routes)))
    for i, (route, color) in enumerate(zip(routes, colors)):
        route_coords = [airports[leg[0]][1:] for leg in route] + [airports[route[-1][1]][1:]]
        line, = ax.plot([coord[0] for coord in route_coords], [coord[1] for coord in route_coords], 
                color=color, linewidth=2, alpha=0.6, transform=ccrs.Geodetic())
        
        # Add flight information for all routes
        for j, (start, end, airline, flight) in enumerate(route):
            start_coords = airports[start][1:]
            end_coords = airports[end][1:]
            mid_lon = (start_coords[0] + end_coords[0]) / 2
            mid_lat = (start_coords[1] + end_coords[1]) / 2
            ax.text(mid_lon, mid_lat, f"Route {i+1}\n{airline}\n{flight}", fontsize=7, ha='center', va='center', 
                    bbox=dict(facecolor=color, alpha=0.7, edgecolor='none'),
                    transform=ccrs.Geodetic())

    # Highlight the best route
    best_route_coords = [airports[leg[0]][1:] for leg in best_route] + [airports[best_route[-1][1]][1:]]
    ax.plot([coord[0] for coord in best_route_coords], [coord[1] for coord in best_route_coords], 
            color='red', linewidth=3, marker='o', transform=ccrs.Geodetic(), label='Best Route')

    plt.title(f"Flight Routes from {origin} to {destination}")
    
    # Add route details
    route_details = "Best Route (Least Stops):\n"
    for start, end, airline, flight in best_route:
        route_details += f"{start} -> {end}: {airline} {flight}\n"
    route_details += f"\nTotal Stops: {len(best_route) - 1}\n\n"
    
    route_details += "All Routes:\n"
    for i, route in enumerate(routes, 1):
        route_details += f"Route {i} (Stops: {len(route) - 1}):\n"
        for start, end, airline, flight in route:
            route_details += f"  {start} -> {end}: {airline} {flight}\n"
        route_details += "\n"
    
    plt.figtext(0.02, 0.02, route_details, fontsize=8, va="bottom", ha="left",
                bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))
    
    # Add legend
    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys(), loc='upper left')
    
    plt.tight_layout()
    plt.show()

# Main program
while True:
    origin = input("Enter origin airport code (or 'quit' to exit): ").upper()
    if origin == 'QUIT':
        break
    destination = input("Enter destination airport code: ").upper()
    plot_route(origin, destination)

print("Thank you for using the flight route planner!")
