import networkx as nx
import numpy as np
import sqlite3

def create_database():
    conn = sqlite3.connect('social_network.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS followers
                 (follower TEXT, followed TEXT)''')
    
    # Sample data
    followers_data = [
        ('UserA', 'UserB'),
        ('UserB', 'UserC'),
        ('UserC', 'UserA'),
        ('UserA', 'UserD'),
        ('UserD', 'UserB'),
        ('UserE', 'UserB'),
        ('UserE', 'UserD')
    ]
    
    c.executemany('INSERT INTO followers VALUES (?,?)', followers_data)
    conn.commit()
    conn.close()

def get_followers_from_db():
    conn = sqlite3.connect('social_network.db')
    c = conn.cursor()
    c.execute('SELECT * FROM followers')
    followers = c.fetchall()
    conn.close()
    return followers

# Create the database and populate it with sample data
create_database()

# Create a directed graph to represent a social network
G = nx.DiGraph()

# Add edges (follower relationships) from the database
G.add_edges_from(get_followers_from_db())

# Compute eigenvector centrality
eigenvector_centrality = nx.eigenvector_centrality_numpy(G)

# Output the influence scores (higher score means more influence)
print("Eigenvector Centrality (Influence Ranking):")
for user, score in eigenvector_centrality.items():
    print(f"{user}: {score:.4f}")