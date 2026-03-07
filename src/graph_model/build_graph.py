import asyncio
import geopandas as gpd
import networkx as nx
import os
import json
from shapely.geometry import Point

from src.graph_model.elevation_provider import ElevationProvider

def build_drainage_graph(input_path="data/drainage_clean.gpkg"):
    """
    Constructs a NetworkX DiGraph from the GeoPackage.
    """
    if not os.path.exists(input_path):
        print(f"Input file {input_path} not found.")
        return None
    
    print(f"Loading {input_path}...")
    gdf = gpd.read_file(input_path)
    
    elev_provider = ElevationProvider()
    G = nx.DiGraph()
    
    # Counter for edges to ensure unique IDs if needed
    edge_counter = 0
    
    for idx, row in gdf.iterrows():
        # Get start and end points of the line
        geom = row.geometry
        if geom is None:
            continue
            
        coords = list(geom.coords)
        if len(coords) < 2:
            continue
            
        start_pt = coords[0] # (lon, lat)
        end_pt = coords[-1]
        
        u = f"{start_pt[0]:.6f},{start_pt[1]:.6f}"
        v = f"{end_pt[0]:.6f},{end_pt[1]:.6f}"
        
        # Add nodes with coordinates and elevation
        if not G.has_node(u):
            elev = elev_provider.get_elevation(start_pt[0], start_pt[1])
            G.add_node(u, pos=start_pt, elev=elev, type='junction', water_level=0.0, capacity=2.0, status='active')
        if not G.has_node(v):
            elev = elev_provider.get_elevation(end_pt[0], end_pt[1])
            G.add_node(v, pos=end_pt, elev=elev, type='junction', water_level=0.0, capacity=2.0, status='active')
        
        # Calculate Slope S = (elev_u - elev_v) / length
        elev_u = G.nodes[u]['elev']
        elev_v = G.nodes[v]['elev']
        length = geom.length * 111000 # Rough deg to meters
        slope = (elev_u - elev_v) / length if length > 0 else 0
        
        # Add edge with attributes
        edge_data = {
            'edge_id': edge_counter,
            'length': length,
            'slope': max(0.0001, slope), # Min slope for gravity flow
            'diameter': row.get('diameter', 0.5),
            'capacity': row.get('capacity', 2.0),
            'status': row.get('status', 'active'),
            'flow': 0.0,
            'original_index': idx
        }
        G.add_edge(u, v, **edge_data)
        edge_counter += 1

    # Identify Outlets (nodes with zero out-degree)
    for node, out_degree in G.out_degree():
        if out_degree == 0:
            G.nodes[node]['type'] = 'outlet'
            
    print(f"Graph built with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges.")
    return G

def save_graph(G, output_path="data/drainage_graph.json"):
    """
    Saves the graph as JSON.
    """
    data = nx.node_link_data(G)
    with open(output_path, 'w') as f:
        json.dump(data, f)
    print(f"Graph saved to {output_path}")

if __name__ == "__main__":
    G = build_drainage_graph()
    if G:
        save_graph(G)
