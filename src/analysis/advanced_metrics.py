import networkx as nx
import numpy as np
import json
import os
import sys

# Add project root to path
sys.path.append(os.getcwd())

from src.simulation.simulator import DrainageSimulator

def calculate_critical_nodes(graph_path="data/drainage_graph.json", top_n=10):
    """
    Identifies nodes that cause the most flooding when their outflows are blocked.
    Impact Score = (Total Flooded Nodes) / (Total Nodes)
    """
    print("Starting Critical Node Analysis (Impact Scoring)...")
    with open(graph_path, 'r') as f:
        graph_data = json.load(f)
    
    node_ids = [n['id'] for n in graph_data['nodes'] if n['type'] != 'outlet']
    impact_scores = {}
    
    total_nodes = len(graph_data['nodes'])

    for node_id in node_ids:
        # Create a temp simulator with a modified graph
        sim = DrainageSimulator(graph_path)
        
        # Manually block all out-edges of this node
        out_edges = list(sim.G.out_edges(node_id))
        for u, v in out_edges:
            sim.G.edges[u, v]['status'] = 'blocked'
            
        # Run simulation for a fixed high-stress duration (e.g., 50 steps at 50mm/hr)
        # Note: simulator.run_step uses get_rainfall_intensity(t)
        for t in range(50):
            sim.run_step(t)
            
        final_stats = sim.get_stats()
        score = final_stats['flooded_nodes'] / total_nodes
        impact_scores[node_id] = score
        # print(f"Node {node_id}: Impact Score = {score:.4f}")

    # Sort and return top N
    sorted_nodes = sorted(impact_scores.items(), key=lambda x: x[1], reverse=True)
    return sorted_nodes[:top_n]

def calculate_cascade_depth(graph):
    """
    Measures the maximum length of a failure chain.
    """
    # Find all blocked edges
    blocked_edges = [(u, v) for u, v, a in graph.edges(data=True) if a.get('status') == 'blocked']
    if not blocked_edges:
        return 0
    
    # Create a failure subgraph
    fail_graph = nx.DiGraph()
    for u, v in blocked_edges:
        fail_graph.add_edge(u, v)
        
    try:
        # Longest path in the failure subgraph represents the deepest cascade
        depth = nx.dag_longest_path_length(fail_graph)
    except nx.NetworkXUnfeasible:
        # If there are cycles, it's not a DAG, but drainage is usually a DAG
        depth = len(blocked_edges) # fallback
        
    return depth

def calculate_resilience(flooded_nodes, total_nodes):
    """
    Formal Resilience Definition: R = 1 - (N_flood / N_total)
    """
    if total_nodes == 0: return 1.0
    return 1.0 - (flooded_nodes / total_nodes)

if __name__ == "__main__":
    # Test the metrics
    top_nodes = calculate_critical_nodes()
    print("\nTop 10 Critical Nodes (Highest Flood Impact):")
    for node, score in top_nodes:
        print(f"Node {node}: {score:.2%}")
    
    # Save top nodes for analysis summary
    os.makedirs("results", exist_ok=True)
    with open("results/critical_nodes.json", "w") as f:
        json.dump(dict(top_nodes), f, indent=2)
