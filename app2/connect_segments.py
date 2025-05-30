import osmnx as ox
import networkx as nx
import pandas as pd

def connect_segments(segments, region_name="Slovenia"):
    try:
        G = ox.graph_from_place(region_name, network_type='bike', simplify=True)
    except Exception as e:
        print(f"Napaka pri prenosu omrežja: {e}")
        return pd.DataFrame()

    segment_list = segments.to_dict('records')
    full_route = []

    for i in range(len(segment_list) - 1):
        seg1 = segment_list[i]
        seg2 = segment_list[i + 1]

        end_point = (seg1['end_latlng_lat'], seg1['end_latlng_lon'])
        start_point = (seg2['start_latlng_lat'], seg2['start_latlng_lon'])

        try:
            end_node = ox.distance.nearest_nodes(G, end_point[1], end_point[0])
            start_node = ox.distance.nearest_nodes(G, start_point[1], start_point[0])

            route_nodes = nx.shortest_path(G, end_node, start_node, weight='length')
            path_coords = [(G.nodes[n]['x'], G.nodes[n]['y']) for n in route_nodes]
            full_route.extend(path_coords)
        except Exception as e:
            print(f"Napaka pri iskanju poti med segmentoma {i} in {i+1}: {e}")
            continue

    first_seg = segment_list[0]
    full_route.insert(0, (first_seg['start_latlng_lon'], first_seg['start_latlng_lat']))

    # Odstrani podvojene točke
    unique_route = [pt for i, pt in enumerate(full_route) if i == 0 or pt != full_route[i-1]]

    return pd.DataFrame(unique_route, columns=["lon", "lat"])
