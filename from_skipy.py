from scipy.sparse import diags
import numpy as np
import networkx as nx

# Create a bipartite graph: Users and Movies
B = nx.Graph()
B.add_nodes_from(['User1', 'User2', 'User3'], bipartite=0)  # Users
B.add_nodes_from(['devara', 'avsr', 'simha'], bipartite=1)  # Movies

# Add edges based on ratings/interactions
B.add_edges_from([
    ('User1', 'devara'),
    ('User1', 'avsr'),
    ('User2', 'devara'),
    ('User3', 'simha'),
])

# Project onto the movie side (item similarity)
movie_graph = nx.bipartite.projected_graph(B, ['devara', 'avsr', 'simha'])

# Compute eigenvector centrality for movie recommendation
movie_rankings = nx.eigenvector_centrality_numpy(movie_graph)

print("Eigenvector Centrality (Movie Recommendation):")
for movie, score in movie_rankings.items():
    print(f"{movie}: {score:.4f}")
