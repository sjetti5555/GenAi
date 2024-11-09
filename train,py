from matplotlib import transforms
import networkx as nx
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Rectangle, Circle, Polygon
import numpy as np
import matplotlib.animation as animation
from matplotlib.transforms import Affine2D

# Create a more comprehensive Indian railway network
G = nx.Graph()
G.add_edges_from([
    ('Mumbai', 'Pune'), ('Pune', 'Hyderabad'), ('Hyderabad', 'Vijayawada'),
    ('Vijayawada', 'Chennai'), ('Chennai', 'Bangalore'), ('Bangalore', 'Mysore'),
    ('Mumbai', 'Ahmedabad'), ('Ahmedabad', 'Jaipur'), ('Jaipur', 'Delhi'),
    ('Delhi', 'Agra'), ('Agra', 'Kanpur'), ('Kanpur', 'Lucknow'),
    ('Lucknow', 'Varanasi'), ('Varanasi', 'Patna'), ('Patna', 'Kolkata'),
    ('Kolkata', 'Bhubaneswar'), ('Bhubaneswar', 'Visakhapatnam'),
    ('Visakhapatnam', 'Vijayawada'), ('Hyderabad', 'Nagpur'), ('Nagpur', 'Bhopal'),
    ('Bhopal', 'Jhansi'), ('Jhansi', 'Agra'), ('Mumbai', 'Surat'),
    ('Surat', 'Vadodara'), ('Vadodara', 'Ahmedabad'), ('Delhi', 'Chandigarh'),
    ('Chandigarh', 'Amritsar'), ('Amritsar', 'Jammu'), ('Delhi', 'Lucknow'),
    ('Lucknow', 'Gorakhpur'), ('Gorakhpur', 'Guwahati'), ('Guwahati', 'Kolkata'),
    ('Kolkata', 'Ranchi'), ('Ranchi', 'Raipur'), ('Raipur', 'Nagpur'),
    ('Nagpur', 'Pune'), ('Pune', 'Goa'), ('Goa', 'Mangalore'),
    ('Mangalore', 'Kochi'), ('Kochi', 'Thiruvananthapuram'), ('Thiruvananthapuram', 'Coimbatore'),
    ('Coimbatore', 'Chennai'), ('Chennai', 'Pondicherry'), ('Pondicherry', 'Trichy'),
    ('Trichy', 'Madurai'), ('Madurai', 'Coimbatore'), ('Bangalore', 'Coimbatore'),
    ('Hyderabad', 'Tirupati'), ('Tirupati', 'Chennai'), ('Delhi', 'Dehradun'),
    ('Dehradun', 'Haridwar'), ('Haridwar', 'Rishikesh'), ('Jaipur', 'Udaipur'),
    ('Udaipur', 'Ahmedabad'), ('Ahmedabad', 'Rajkot'), ('Rajkot', 'Dwarka'),
    ('Mumbai', 'Nashik'), ('Nashik', 'Aurangabad'), ('Aurangabad', 'Nanded'),
    ('Nanded', 'Hyderabad'), ('Bhopal', 'Indore'), ('Indore', 'Ujjain'),
    ('Ujjain', 'Ahmedabad'), ('Kolkata', 'Siliguri'), ('Siliguri', 'Darjeeling')
])

# Add some basic distance information (in km)
for (u, v) in G.edges():
    G[u][v]['distance'] = 500  # Simplified: assume 500km between each connected city

# City coordinates (Latitude, Longitude)
city_coords = {
    'Mumbai': (19.0760, 72.8777), 'Pune': (18.5204, 73.8567),
    'Hyderabad': (17.3850, 78.4867), 'Vijayawada': (16.5062, 80.6480),
    'Chennai': (13.0827, 80.2707), 'Bangalore': (12.9716, 77.5946),
    'Mysore': (12.2958, 76.6394), 'Ahmedabad': (23.0225, 72.5714),
    'Jaipur': (26.9124, 75.7873), 'Delhi': (28.6139, 77.2090),
    'Agra': (27.1767, 78.0081), 'Kanpur': (26.4499, 80.3319),
    'Lucknow': (26.8467, 80.9462), 'Varanasi': (25.3176, 82.9739),
    'Patna': (25.5941, 85.1376), 'Kolkata': (22.5726, 88.3639),
    'Bhubaneswar': (20.2961, 85.8245), 'Visakhapatnam': (17.6868, 83.2185),
    'Nagpur': (21.1458, 79.0882), 'Bhopal': (23.2599, 77.4126),
    'Jhansi': (25.4484, 78.5685), 'Surat': (21.1702, 72.8311),
    'Vadodara': (22.3072, 73.1812), 'Chandigarh': (30.7333, 76.7794),
    'Amritsar': (31.6340, 74.8723), 'Jammu': (32.7266, 74.8570),
    'Gorakhpur': (26.7606, 83.3732), 'Guwahati': (26.1445, 91.7362),
    'Ranchi': (23.3441, 85.3096), 'Raipur': (21.2514, 81.6296),
    'Goa': (15.2993, 74.1240), 'Mangalore': (12.9141, 74.8560),
    'Kochi': (9.9312, 76.2673), 'Thiruvananthapuram': (8.5241, 76.9366),
    'Coimbatore': (11.0168, 76.9558), 'Pondicherry': (11.9416, 79.8083),
    'Trichy': (10.7905, 78.7047), 'Madurai': (9.9252, 78.1198),
    'Tirupati': (13.6288, 79.4192), 'Dehradun': (30.3165, 78.0322),
    'Haridwar': (29.9457, 78.1642), 'Rishikesh': (30.0869, 78.2676),
    'Udaipur': (24.5854, 73.7125), 'Rajkot': (22.3039, 70.8022),
    'Dwarka': (22.2442, 68.9685), 'Nashik': (19.9975, 73.7898),
    'Aurangabad': (19.8762, 75.3433), 'Nanded': (19.1383, 77.3210),
    'Indore': (22.7196, 75.8577), 'Ujjain': (23.1765, 75.7885),
    'Siliguri': (26.7271, 88.3953), 'Darjeeling': (27.0410, 88.2663)
}

def find_route(start, end):
    try:
        path = nx.shortest_path(G, start, end, weight='distance')
        distance = sum(G[path[i]][path[i+1]]['distance'] for i in range(len(path)-1))
        return path, distance
    except nx.NetworkXNoPath:
        return None, None

def create_train(ax, x, y, angle, num_bogies=2):
    train_parts = []
    
    # Create a composite transformation
    transform = ccrs.PlateCarree()._as_mpl_transform(ax) + Affine2D().rotate_around(x, y, angle)
    
    # Create engine
    engine = Polygon([(x, y), (x+0.1, y), (x+0.7, y+0.1), (x+0.1, y+0.1), (x, y+0.1)], 
                     facecolor='red', edgecolor='black', transform=transform)
    ax.add_patch(engine)
    train_parts.append(engine)
    
    # Create bogies
    for i in range(num_bogies):
        bogie = Rectangle((x - (i+1)*0.7, y-0.2), 0.6, 0.4, facecolor='blue', edgecolor='black', transform=transform)
        wheel1 = Circle((x - (i+1)*0.7 + 0.1, y - 0.3), 0.1, facecolor='black', transform=transform)
        wheel2 = Circle((x - (i+1)*0.7 + 0.5, y - 0.3), 0.1, facecolor='black', transform=transform)
        ax.add_patch(bogie)
        ax.add_patch(wheel1)
        ax.add_patch(wheel2)
        train_parts.extend([bogie, wheel1, wheel2])
    
    return train_parts

def draw_track(ax, x1, y1, x2, y2):
    ax.plot([x1, x2], [y1, y2], color='gray', linewidth=2, linestyle='-', transform=ccrs.PlateCarree())
    num_sleepers = int(np.sqrt((x2-x1)**2 + (y2-y1)**2) * 20)
    for i in range(num_sleepers):
        t = i / (num_sleepers - 1)
        x = x1 + t * (x2 - x1)
        y = y1 + t * (y2 - y1)
        sleeper = Rectangle((x-0.1, y-0.05), 0.2, 0.1, facecolor='brown', edgecolor='none', 
                            transform=ccrs.PlateCarree())
        ax.add_patch(sleeper)

def visualize_route(path):
    fig = plt.figure(figsize=(20, 15))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    
    # Add map features
    ax.add_feature(cfeature.LAND, facecolor='lightgreen')
    ax.add_feature(cfeature.OCEAN, facecolor='lightblue')
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    ax.add_feature(cfeature.LAKES, alpha=0.5)
    ax.add_feature(cfeature.RIVERS)
    
    ax.set_extent([68, 97, 8, 37], crs=ccrs.PlateCarree())
    
    # Plot railway network and draw tracks
    for (u, v) in G.edges():
        x1, y1 = city_coords[u]
        x2, y2 = city_coords[v]
        draw_track(ax, y1, x1, y2, x2)
    
    # Plot the route
    route_x, route_y = [], []
    for city in path:
        x, y = city_coords[city]
        route_y.append(x)
        route_x.append(y)
    ax.plot(route_x, route_y, color='red', linewidth=3, transform=ccrs.PlateCarree())
    
    # Plot cities
    for city, (lat, lon) in city_coords.items():
        ax.plot(lon, lat, 'ko', markersize=5, transform=ccrs.PlateCarree())
        ax.text(lon, lat, city, fontsize=8, ha='right', va='bottom', transform=ccrs.PlateCarree())
    
    # Highlight start and end
    start, end = path[0], path[-1]
    ax.plot(city_coords[start][1], city_coords[start][0], 'go', markersize=10, transform=ccrs.PlateCarree())
    ax.plot(city_coords[end][1], city_coords[end][0], 'ro', markersize=10, transform=ccrs.PlateCarree())
    
    plt.title(f"Train Route from {start} to {end}")
    
    # Create train
    train = create_train(ax, route_x[0], route_y[0], 0)
    
    # Calculate total distance
    total_distance = sum(np.sqrt((route_x[i+1]-route_x[i])**2 + (route_y[i+1]-route_y[i])**2) for i in range(len(route_x)-1))
    
    def animate(frame):
        # Calculate position along the route
        distance = (frame / 100) * total_distance
        current_distance = 0
        for i in range(len(route_x) - 1):
            segment_distance = np.sqrt((route_x[i+1]-route_x[i])**2 + (route_y[i+1]-route_y[i])**2)
            if current_distance + segment_distance > distance:
                ratio = (distance - current_distance) / segment_distance
                x = route_x[i] + ratio * (route_x[i+1] - route_x[i])
                y = route_y[i] + ratio * (route_y[i+1] - route_y[i])
                angle = np.arctan2(route_y[i+1] - route_y[i], route_x[i+1] - route_x[i])
                break
            current_distance += segment_distance
        
        # Update train position and orientation
        transform = ccrs.PlateCarree()._as_mpl_transform(ax) + Affine2D().translate(x - route_x[0], y - route_y[0]).rotate_around(x, y, angle)
        for part in train:
            part.set_transform(transform)
        return train

    # Create animation
    anim = animation.FuncAnimation(fig, animate, frames=100, interval=50, blit=True)
    
    plt.tight_layout()
    plt.show()

# Example usage
while True:
    start_city = input("Enter start city: ").title()
    if start_city not in G.nodes():
        print(f"Sorry, {start_city} is not in our network. Available cities are: {', '.join(sorted(G.nodes()))}")
        continue
    
    end_city = input("Enter destination city: ").title()
    if end_city not in G.nodes():
        print(f"Sorry, {end_city} is not in our network. Available cities are: {', '.join(sorted(G.nodes()))}")
        continue
    
    break

path, distance = find_route(start_city, end_city)

if path:
    print(f"Route: {' -> '.join(path)}")
    print(f"Approximate distance: {distance} km")
    print(f"Number of stops: {len(path) - 2}")
    visualize_route(path)
else:
    print("No route found.")