import osmnx as ox

def get_surface_type(start_lat, start_lon, end_lat, end_lon):
    ox.settings.useful_tags_way = ['surface']
    try:
        G = ox.graph_from_point((start_lat, start_lon), dist=100, network_type='bike')
        u, v, key = ox.distance.nearest_edges(G, float(start_lon), float(start_lat))
        edge = G[u][v][0]
        return edge.get('surface', 'unknown')
    except Exception as e:
        return 'unknown'
