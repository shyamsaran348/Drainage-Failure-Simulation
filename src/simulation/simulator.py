import networkx as nx
import numpy as np
import json
import os
import sys

# Add project root to path for imports
sys.path.append(os.getcwd())

from src.grammar_engine.rule_engine import RuleEngine
from src.simulation.rainfall_model import get_rainfall_intensity

class DrainageSimulator:
    def __init__(self, graph_path="data/drainage_graph.json", use_rerouting=True, use_rules=True):
        self.load_graph(graph_path)
        self.engine = RuleEngine(use_rerouting=use_rerouting, use_rules=use_rules)
        self.step = 0
        self.history = []

    def load_graph(self, path):
        if not os.path.exists(path):
            raise FileNotFoundError(f"Graph file {path} not found.")
        with open(path, 'r') as f:
            data = json.load(f)
        
        # Determine the correct key for links/edges
        link_key = 'links' if 'links' in data else 'edges'
        
        # Support for older/newer NX versions
        try:
            self.G = nx.node_link_graph(data, edges=link_key)
        except TypeError:
            # Fallback for versions that don't take 'edges' argument or use different ones
            if link_key == 'links' and 'edges' not in data:
                data['edges'] = data.pop('links')
            self.G = nx.node_link_graph(data)
            
        print(f"Loaded graph with {self.G.number_of_nodes()} nodes.")

    def calculate_pipe_capacity(self, diameter, slope, n=0.013):
        """
        Calculates pipe capacity (m^3/s) using Manning's Equation.
        """
        area = np.pi * (diameter / 2)**2
        wetted_perimeter = np.pi * diameter
        hydraulic_radius = area / wetted_perimeter if wetted_perimeter > 0 else 0
        S = max(0.0001, slope)
        velocity = (1.0 / n) * (hydraulic_radius**(2/3)) * (S**0.5)
        capacity = velocity * area
        return capacity

    def run_step(self, t, intensity=50.0):
        # 1. Update Rainfall (Rule 1)
        rainfall_intensity_mm_hr = get_rainfall_intensity(t, peak_intensity=intensity) 
        rainfall_m_s = (rainfall_intensity_mm_hr / 1000.0) / 3600.0
        for node in self.G.nodes():
            # Introduce stochasticity for research robustness: Mean=5000, StdDev=500
            catchment_area = np.random.normal(5000.0, 500.0) 
            inflow = rainfall_m_s * catchment_area
            self.G.nodes[node]['water_level'] += inflow
            
        # 2. Distribute Flow (Downstream propagation with Gravity)
        try:
            topo_order = list(nx.topological_sort(self.G))
        except nx.NetworkXUnfeasible:
            topo_order = list(self.G.nodes())

        for u in topo_order:
            node_water = self.G.nodes[u]['water_level']
            if node_water <= 0:
                continue
            
            edges = self.G.out_edges(u, data=True)
            active_out = [(u, v) for _, v, attr in edges if attr['status'] == 'active']
            if not active_out: continue
                
            total_manning_cap = sum(self.calculate_pipe_capacity(self.G.edges[e]['diameter'], self.G.edges[e]['slope']) for e in active_out)
            
            for e in active_out:
                u_n, v_n = e
                manning_cap = self.calculate_pipe_capacity(self.G.edges[e]['diameter'], self.G.edges[e]['slope'])
                share = (manning_cap / total_manning_cap) if total_manning_cap > 0 else (1.0 / len(active_out))
                requested_flow = node_water * share
                actual_flow = min(requested_flow, manning_cap)
                
                self.G.edges[e]['flow'] = actual_flow
                self.G.nodes[u_n]['water_level'] -= actual_flow
                self.G.nodes[v_n]['water_level'] += actual_flow

        # 3. Apply Grammar Rules
        logs = self.engine.apply_rules(self.G)
        
        # 4. Increment Overload Duration
        for u, v, attr in self.G.edges(data=True):
            if attr['status'] == 'overloaded':
                self.G.edges[u, v]['overload_duration'] = attr.get('overload_duration', 0) + 1
            else:
                self.G.edges[u, v]['overload_duration'] = 0
        
        stats = self.get_stats()
        stats['time'] = t
        stats['logs'] = logs
        self.history.append(stats)
        return stats

    def get_stats(self):
        blocked_pipes = sum(1 for _, _, a in self.G.edges(data=True) if a['status'] == 'blocked')
        flooded_nodes = sum(1 for _, a in self.G.nodes(data=True) if a['type'] == 'flood')
        total_flow = sum(a['flow'] for _, _, a in self.G.edges(data=True))
        
        # Calculate Cascade Depth (Formal Metric Lambda)
        cascade_depth = 0
        blocked_edges = [(u, v) for u, v, a in self.G.edges(data=True) if a.get('status') == 'blocked']
        if blocked_edges:
            fail_graph = nx.DiGraph()
            fail_graph.add_edges_from(blocked_edges)
            try:
                cascade_depth = nx.dag_longest_path_length(fail_graph)
            except nx.NetworkXUnfeasible:
                cascade_depth = len(blocked_edges)

        # Calculate Resilience (Ratio)
        total_nodes = self.G.number_of_nodes()
        resilience = 1.0 - (flooded_nodes / total_nodes) if total_nodes > 0 else 1.0

        return {
            'blocked_pipes': blocked_pipes, 
            'flooded_nodes': flooded_nodes, 
            'total_flow': total_flow,
            'cascade_depth': cascade_depth,
            'resilience': resilience
        }

    def run_simulation(self, steps=60):
        print(f"Starting simulation for {steps} steps...")
        for t in range(steps):
            stats = self.run_step(t)
            if t % 10 == 0:
                print(f"T={t}: Blocked={stats['blocked_pipes']}, Flooded={stats['flooded_nodes']}")
        self.save_results()
        self.save_final_graph()

    def save_final_graph(self, output_path="data/drainage_graph_final.json"):
        data = nx.node_link_data(self.G)
        with open(output_path, 'w') as f:
            json.dump(data, f)
        print(f"Final graph state saved to {output_path}")

    def save_results(self, output_path="results/simulation_logs/run_log.json"):
        os.makedirs(os.path.dirname(output_image) if 'output_image' in locals() else "results/simulation_logs", exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(self.history, f, indent=2)

if __name__ == "__main__":
    sim = DrainageSimulator()
    sim.run_simulation()
