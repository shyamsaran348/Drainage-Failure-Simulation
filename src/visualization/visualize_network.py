import networkx as nx
import matplotlib.pyplot as plt
import json
import os
import sys
import pandas as pd

# Add project root to path
sys.path.append(os.getcwd())

from src.visualization.plot_style import set_professional_style, get_color_palette

set_professional_style()
colors = get_color_palette()

def visualize_graph(graph_path="data/drainage_graph_final.json", output_image="results/figures/network_map.png"):
    if not os.path.exists(graph_path):
        print(f"Graph file {graph_path} not found.")
        return
    with open(graph_path, 'r') as f:
        data = json.load(f)
    
    # Ensure compatibility with both 'links' and 'edges' nomenclature for networkx
    if 'links' not in data and 'edges' in data:
        data['links'] = data.pop('edges')
        
    G = nx.node_link_graph(data)
    pos = {n: d['pos'] for n, d in G.nodes(data=True)}
    
    plt.figure(figsize=(8, 7))
    edge_colors = ['#ae2012' if d['status'] in ['blocked', 'overloaded'] else '#005f73' for u, v, d in G.edges(data=True)]
    nx.draw_networkx_edges(G, pos, edge_color=edge_colors, width=1.5, alpha=0.4, arrows=True, arrowsize=10)
    
    node_colors = []
    for n, d in G.nodes(data=True):
        if d['type'] == 'flood': node_colors.append('#9b2226')
        elif d['type'] == 'outlet': node_colors.append('#0a9396')
        else: node_colors.append('#94d2bd')
            
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=30, linewidths=0.5, edgecolors='black')
    
    plt.title("Urban Drainage Infrastructure: Failure State Analysis", pad=20)
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.tight_layout()
    os.makedirs(os.path.dirname(output_image), exist_ok=True)
    plt.savefig(output_image, dpi=600, bbox_inches='tight')
    print(f"Professional network map saved to {output_image}")
    plt.close()

def visualize_heatmap(graph_path="data/drainage_graph_final.json", output_image="results/figures/flow_heatmap.png"):
    if not os.path.exists(graph_path): return
    with open(graph_path, 'r') as f:
        data = json.load(f)
        
    if 'links' not in data and 'edges' in data:
        data['links'] = data.pop('edges')
        
    G = nx.node_link_graph(data)
    pos = {n: d['pos'] for n, d in G.nodes(data=True)}
    
    plt.figure(figsize=(8, 7))
    edge_stress = []
    for u, v, d in G.edges(data=True):
        ratio = d['flow'] / max(0.1, d['capacity'])
        edge_stress.append(min(1.0, ratio))
    
    ax = plt.gca()
    edges = nx.draw_networkx_edges(G, pos, ax=ax, edge_color=edge_stress, edge_cmap=plt.cm.magma, width=2, arrows=True, arrowsize=8)
    node_colors = ['#9b2226' if d['type'] == 'flood' else 'black' for n, d in G.nodes(data=True)]
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_colors, node_size=15, alpha=0.8)
    
    sm = plt.cm.ScalarMappable(cmap=plt.cm.magma, norm=plt.Normalize(vmin=0, vmax=1))
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax, shrink=0.8)
    cbar.set_label("Hydraulic Stress Ratio ($q/C$)", fontsize=10)
    
    plt.title("Network Stress Vulnerability Heatmap", pad=20)
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.tight_layout()
    plt.savefig(output_image, dpi=600)
    print(f"Professional heatmap saved to {output_image}")
    plt.close()

def plot_time_series(log_path="results/simulation_logs/run_log.json", output_image="results/figures/plot_time_series.png"):
    if not os.path.exists(log_path): return
    with open(log_path, 'r') as f:
        history = json.load(f)
    
    df = pd.DataFrame(history)
    plt.figure(figsize=(7, 5))
    if 'flooded_nodes' in df.columns:
        plt.plot(df['time'], df['flooded_nodes'], color='#ae2012', label='Critical Flooding (Nodes)', linewidth=2.5)
    if 'blocked_pipes' in df.columns:
        plt.plot(df['time'], df['blocked_pipes'], color='#005f73', label='Structural Blockage (Pipes)', linewidth=1.5, linestyle='--')
    
    plt.xlabel("Simulation Timestep (minutes)")
    plt.ylabel("Infrastructure Count")
    plt.title("Temporal Dynamics of Failure Propagation")
    plt.legend(frameon=True, facecolor='white', framealpha=0.9)
    plt.tight_layout()
    plt.savefig(output_image, dpi=600)
    print(f"Professional time series plot saved to {output_image}")
    plt.close()

if __name__ == "__main__":
    path = "data/drainage_graph_final.json"
    if not os.path.exists(path): path = "data/drainage_graph.json"
    visualize_graph(graph_path=path)
    visualize_heatmap(graph_path=path)
    plot_time_series()
