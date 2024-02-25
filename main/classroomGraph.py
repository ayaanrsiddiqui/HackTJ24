import networkx as nx

# Create a graph object
G = nx.Graph()

# Add edges with weights
G.add_edge(0, 9, weight=1)
G.add_edge(8, 9, weight=4)
G.add_edge(7, 8, weight=3)
G.add_edge(7, 6, weight=1)
G.add_edge(1, 6, weight=1)
G.add_edge(6, 5, weight=3)
G.add_edge(5, 4, weight=2)
G.add_edge(4, 3, weight=2)
G.add_edge(2, 3, weight=1)
G.add_edge(0, 11, weight=1)
G.add_edge(10, 12, weight=1)
G.add_edge(9, 10, weight=1)
G.add_edge(2, 12, weight=1)
G.add_edge(12, 13, weight=1)
G.add_edge(3, 13, weight=1)

all_pairs_shortest_paths = dict(nx.all_pairs_dijkstra_path_length(G))

nodes = sorted(G.nodes())

num_nodes = len(nodes)
distance_matrix = [[float('inf')] * num_nodes for _ in range(num_nodes)]

for i, node_i in enumerate(nodes):
    for j, node_j in enumerate(nodes):
        distance_matrix[i][j] = all_pairs_shortest_paths[node_i].get(node_j, float('inf'))

with open("distanceMatrixUpdated.txt", "w") as f:
    print(distance_matrix, file=f)