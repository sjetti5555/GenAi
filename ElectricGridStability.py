import networkx as nx
import matplotlib.pyplot as plt
import random

def create_electric_grid(num_nodes, connection_probability):
    # Create a random graph to represent the electric grid
    G = nx.erdos_renyi_graph(num_nodes, connection_probability)
    
    # Assign random capacities to edges (connections between stations)
    for (u, v) in G.edges():
        G[u][v]['capacity'] = random.uniform(50, 200)
    
    return G

def analyze_grid_stability(G):
    # Calculate eigenvector centrality
    centrality = nx.eigenvector_centrality(G, weight='capacity')
    
    # Identify the most critical nodes
    critical_nodes = sorted(centrality, key=centrality.get, reverse=True)[:5]
    
    return centrality, critical_nodes

def visualize_grid(G, centrality):
    pos = nx.spring_layout(G)
    plt.figure(figsize=(12, 8))
    
    # Draw the network
    nx.draw_networkx_edges(G, pos, alpha=0.2)
    
    # Create a mappable object for the colorbar
    node_colors = list(centrality.values())
    nodes = nx.draw_networkx_nodes(G, pos, node_size=100, node_color=node_colors, 
                                   cmap=plt.cm.viridis)
    
    # Add labels to nodes
    labels = {node: f"{node}\n{centrality[node]:.2f}" for node in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels, font_size=8)
    
    plt.title("Electric Grid Stability Analysis")
    plt.colorbar(nodes, label="Eigenvector Centrality")
    plt.axis('off')
    plt.tight_layout()
    plt.show()

# Main execution
num_nodes = 50
connection_probability = 0.1

# Create the electric grid
grid = create_electric_grid(num_nodes, connection_probability)

# Analyze grid stability
centrality, critical_nodes = analyze_grid_stability(grid)

# Print results
print("Top 5 critical nodes (stations/substations):")
for node in critical_nodes:
    print(f"Node {node}: Centrality = {centrality[node]:.4f}")

# Visualize the grid
visualize_grid(grid, centrality)

# Simulate failure of most critical node
most_critical_node = critical_nodes[0]
grid_after_failure = grid.copy()
grid_after_failure.remove_node(most_critical_node)

print(f"\nSimulating failure of node {most_critical_node}")
print(f"Number of connected components after failure: {nx.number_connected_components(grid_after_failure)}")
print(f"Largest component size: {len(max(nx.connected_components(grid_after_failure), key=len))}")

# Analyze and visualize grid after failure
centrality_after_failure, _ = analyze_grid_stability(grid_after_failure)
visualize_grid(grid_after_failure, centrality_after_failure)