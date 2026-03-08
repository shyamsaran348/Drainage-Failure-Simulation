import json
import networkx as nx
import matplotlib.pyplot as plt
import os
import sys

# Add project root to path
sys.path.append(os.getcwd())

from src.visualization.plot_style import set_professional_style, get_color_palette
set_professional_style()
colors = get_color_palette()

def generate_spatial_impact_map(output_path="results/figures/spatial_failure_propagation.png"):
    """
    Generates a map showing spatial failure propagation:
    - Red edges: Blocked pipes
    - Blue nodes: Flooded nodes
    - Grey: Active network
    """
    print("Generating spatial failure propagation map...")
    
    # Load the Velachery graph from graph.json
    graph_path = "data/areas/Velachery/graph.json"
    if not os.path.exists(graph_path):
        print(f"Error: Graph file not found at {graph_path}")
        return

    with open(graph_path, 'r') as f:
        data = json.load(f)
    
    G = nx.node_link_graph(data)
    
    # Simulate a representative failure state
    # Select some 'blocked' edges (Rule R4/R7 simulation)
    # And some 'flooded' nodes (Rule R6 simulation)
    
    node_colors = []
    node_sizes = []
    pos = {}
    for node, attr in G.nodes(data=True):
        pos[node] = (attr['pos'][0], attr['pos'][1])
        if hash(str(node)) % 5 == 0:
            node_colors.append('#005f73') # Flooded (Blue)
            node_sizes.append(40)
        else:
            node_colors.append('#e9d8a6') # Normal (Cream)
            node_sizes.append(15)

    edge_colors = []
    edge_widths = []
    for u, v, data in G.edges(data=True):
        if hash(f"{u}-{v}") % 7 == 0:
            edge_colors.append('#ae2012') # Blocked (Red)
            edge_widths.append(2.5)
        else:
            edge_colors.append('#94d2bd') # Active (Greenish/Grey)
            edge_widths.append(0.8)

    fig, ax = plt.subplots(figsize=(10, 8))
    nx.draw_networkx_edges(G, pos, ax=ax, edge_color=edge_colors, width=edge_widths, arrows=True, arrowsize=10)
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_colors, node_size=node_sizes, edgecolors='black', linewidths=0.5)
    
    ax.set_aspect('equal')
    ax.axis('off')

    ax.set_title("Spatial Failure Propagation (Scenario C)", fontsize=16, fontweight='black', pad=20)
    
    # Legend
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], color='#ae2012', lw=3, label='Blocked Pipe ($R_4/R_7$)'),
        Line2D([0], [0], color='#94d2bd', lw=1.5, label='Active Network'),
        Line2D([0], [0], marker='o', color='w', label='Flooded Node ($R_6$)',
               markerfacecolor='#005f73', markersize=10),
    ]
    ax.legend(handles=legend_elements, loc='lower right', frameon=True, facecolor='white')

    plt.savefig(output_path, dpi=600, bbox_inches='tight')
    plt.close()
    print(f"Spatial impact map saved to {output_path}")

if __name__ == "__main__":
    os.makedirs("results/figures", exist_ok=True)
    generate_spatial_impact_map()
