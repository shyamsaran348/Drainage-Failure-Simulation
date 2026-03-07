import networkx as nx
import matplotlib.pyplot as plt
import json
import os
import pandas as pd

def visualize_graph(graph_path="data/drainage_graph_final.json", output_image="results/figures/network_map.png"):
    if not os.path.exists(graph_path):
        print(f"Graph file {graph_path} not found.")
        return
    with open(graph_path, 'r') as f:
        data = json.load(f)
    # Handle case where graph uses "links" instead of "edges"
    if 'links' in data and 'edges' not in data:
        data['edges'] = data.pop('links')
    G = nx.node_link_graph(data)
    pos = {n: d['pos'] for n, d in G.nodes(data=True)}
    
    plt.figure(figsize=(12, 10))
    edge_colors = ['red' if d['status'] in ['blocked', 'overloaded'] else 'blue' for u, v, d in G.edges(data=True)]
    nx.draw_networkx_edges(G, pos, edge_color=edge_colors, width=2, alpha=0.6, arrows=True)
    
    node_colors = []
    for n, d in G.nodes(data=True):
        if d['type'] == 'flood': node_colors.append('red')
        elif d['type'] == 'outlet': node_colors.append('blue')
        else: node_colors.append('green')
            
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=50)
    plt.title("Drainage Network - Final State\n(Red Nodes = Flooded, Red Edges = Overloaded/Blocked)")
    plt.grid(True, linestyle='--', alpha=0.5)
    os.makedirs(os.path.dirname(output_image), exist_ok=True)
    plt.savefig(output_image)
    print(f"Network map saved to {output_image}")
    plt.close()

def visualize_heatmap(graph_path="data/drainage_graph_final.json", output_image="results/figures/flow_heatmap.png"):
    if not os.path.exists(graph_path): return
    with open(graph_path, 'r') as f:
        data = json.load(f)
    # Handle case where graph uses "links" instead of "edges"
    if 'links' in data and 'edges' not in data:
        data['edges'] = data.pop('links')
    G = nx.node_link_graph(data)
    pos = {n: d['pos'] for n, d in G.nodes(data=True)}
    
    plt.figure(figsize=(12, 10))
    edge_stress = []
    for u, v, d in G.edges(data=True):
        ratio = d['flow'] / max(0.1, d['capacity'])
        edge_stress.append(min(1.0, ratio))
    
    ax = plt.gca()
    nx.draw_networkx_edges(G, pos, ax=ax, edge_color=edge_stress, edge_cmap=plt.cm.YlOrRd, width=3, arrows=True)
    node_colors = ['red' if d['type'] == 'flood' else 'black' for n, d in G.nodes(data=True)]
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_colors, node_size=30)
    
    # Create a ScalarMappable for the colorbar
    sm = plt.cm.ScalarMappable(cmap=plt.cm.YlOrRd, norm=plt.Normalize(vmin=0, vmax=1))
    sm.set_array([])
    plt.colorbar(sm, ax=ax, label="Flow/Capacity Stress Ratio")
    plt.title("Drainage Network Stress Heatmap\n(Red Nodes = Flooded, Color Scale = Pipe Utilization)")
    plt.savefig(output_image)
    print(f"Heatmap saved to {output_image}")
    plt.close()

def plot_time_series(log_path="results/simulation_logs/run_log.json", output_image="results/figures/plot_time_series.png"):
    if not os.path.exists(log_path): return
    with open(log_path, 'r') as f:
        history = json.load(f)
    
    df = pd.DataFrame(history)
    plt.figure(figsize=(10, 6))
    if 'flooded_nodes' in df.columns:
        plt.plot(df['time'], df['flooded_nodes'], color='red', label='Flooded Nodes')
    if 'blocked_pipes' in df.columns:
        plt.plot(df['time'], df['blocked_pipes'], color='blue', label='Blocked Pipes')
    plt.xlabel("Timestep (min)")
    plt.ylabel("Count")
    plt.title("Failure Propagation Over Time")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig(output_image)
    print(f"Time series plot saved to {output_image}")
    plt.close()

if __name__ == "__main__":
    path = "data/drainage_graph_final.json"
    if not os.path.exists(path): path = "data/drainage_graph.json"
    visualize_graph(graph_path=path)
    visualize_heatmap(graph_path=path)
    plot_time_series()
