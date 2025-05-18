import pandas as pd
import networkx as nx
from haversine import haversine, Unit

def connect_segments(segments):
    # Convert to graph based on proximity
    G = nx.Graph()

    for idx, seg in segments.iterrows():
        start = (seg['start_latlng_lat'], seg['start_latlng_lon'])
        end = (seg['end_latlng_lat'], seg['end_latlng_lon'])
        G.add_node(idx, segment=seg, coord=start)

    for i, s1 in segments.iterrows():
        end1 = (s1['end_latlng_lat'], s1['end_latlng_lon'])
        for j, s2 in segments.iterrows():
            if i != j:
                start2 = (s2['start_latlng_lat'], s2['start_latlng_lon'])
                dist = haversine(end1, start2, unit=Unit.METERS)
                if dist < 500:  # if within 500m
                    G.add_edge(i, j, weight=dist)

    if len(G.nodes) == 0:
        return pd.DataFrame()

    path = list(nx.dfs_preorder_nodes(G))
    route_segments = segments.loc[path]
    latlngs = []

    # build a path connecting segments
    #try:
    #    path = nx.approximation.traveling_salesman_problem(G, cycle=False)
    #    return [segments.iloc[i] for i in path]
    #except:
    #    return segments  # fallback if TSP fails

    for _, row in route_segments.iterrows():
        latlngs.append({
            "start_lat": row['start_latlng_lat'],
            "start_lon": row['start_latlng_lon'],
            "end_lat": row['end_latlng_lat'],
            "end_lon": row['end_latlng_lon'],
            "name": row['name']
        })

    return pd.DataFrame(latlngs)
