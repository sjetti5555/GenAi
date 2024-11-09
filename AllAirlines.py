import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# Load international airports data
airports_df = pd.read_csv('https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports.dat', 
                          header=None, 
                          names=['ID', 'Name', 'City', 'Country', 'IATA', 'ICAO', 'Latitude', 'Longitude', 'Altitude', 'Timezone', 'DST', 'Tz database time zone', 'Type', 'Source'])

# Filter for international airports with IATA codes
airports_df = airports_df[(airports_df['Type'] == 'airport') & (airports_df['IATA'].notna())]

# Create airports dictionary
airports = dict(zip(airports_df['IATA'], zip(airports_df['City'], airports_df['Longitude'], airports_df['Latitude'])))

# Load airlines data
airlines_df = pd.read_csv('https://raw.githubusercontent.com/jpatokal/openflights/master/data/airlines.dat', 
                          header=None, 
                          names=['ID', 'Name', 'Alias', 'IATA', 'ICAO', 'Callsign', 'Country', 'Active'])

# Filter for active airlines with IATA codes
airlines_df = airlines_df[(airlines_df['Active'] == 'Y') & (airlines_df['IATA'].notna())]

# Create airlines list
airlines = airlines_df['Name'].tolist()

# Generate 10000 rows of flight data
np.random.seed(42)
data = []
for _ in range(10000):
    airline = random.choice(airlines)
    source, dest = random.sample(list(airports.keys()), 2)
    flight_num = f"{airline[:2].upper()}{random.randint(1000, 9999)}"
    data.append([airline, flight_num, source, dest])

df = pd.DataFrame(data, columns=['Airline', 'Flight', 'Source', 'Destination'])

# Create a graph
G = nx.from_pandas_edgelist(df, 'Source', 'Destination', ['Airline', 'Flight'], create_using=nx.DiGraph())

# Calculate eigenvector centrality
centrality = nx.eigenvector_centrality(G)

def find_routes(G, origin, destination, num_routes=6):
    all_paths = []
    for path in nx.all_simple_paths(G, origin, destination, cutoff=5):  # Limit to 4 stops max
        if len(path) >= 3:  # Ensure at least one stop
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

    # Plot origin, destination, and stopover airports
    airports_to_plot = set([origin, destination])
    for route in routes:
        for start, end, _, _ in route:
            airports_to_plot.add(start)
            airports_to_plot.add(end)

    for code in airports_to_plot:
        city, lon, lat = airports[code]
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

# Save the flight database as an Excel file
df.to_excel('international_flight_database.xlsx', index=False)
print("Flight database saved as 'international_flight_database.xlsx'")

# Main program
while True:
    origin = input("Enter origin airport code (or 'quit' to exit): ").upper()
    if origin == 'QUIT':
        break
    destination = input("Enter destination airport code: ").upper()
    plot_route(origin, destination)

print("Thank you for using the international flight route planner!")