import osmnx as ox
import geopandas as gpd
from shapely.geometry import LineString

def detect_surface_type(latlng_start, latlng_end):
    center_point = ((latlng_start[0] + latlng_end[0]) / 2,
                    (latlng_start[1] + latlng_end[1]) / 2)
    G = ox.graph_from_point(center_point, dist=500, network_type='bike')
    edges = ox.graph_to_gdfs(G, nodes=False, edges=True)
    
    # Get edges close to the line
    seg_line = LineString([latlng_start[::-1], latlng_end[::-1]])
    edges['distance'] = edges.geometry.distance(seg_line)
    near_edges = edges[edges['distance'] < 0.0005]

    if not near_edges.empty:
        surface = near_edges.iloc[0].get('surface', 'unknown')
    else:
        surface = 'unknown'
    return surface
