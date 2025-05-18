import osmnx as ox
import networkx as nx
from shapely.geometry import Point

def get_shortest_path_between_segments(segment_coords):
    G = ox.graph_from_point(segment_coords[0], dist=20000, network_type='bike')

    full_path = []
    for i in range(len(segment_coords) - 1):
        start = ox.nearest_nodes(G, *segment_coords[i][::-1])
        end = ox.nearest_nodes(G, *segment_coords[i+1][::-1])
        path = nx.shortest_path(G, start, end, weight='length')
        full_path.extend(path)
    return full_path, G

def get_path_coordinates(path, G):
    return ([G.nodes[n]['x'], G.nodes[n]['y']] for n in path)
