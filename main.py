#!/usr/bin/env python3
"""
Main entry point for the Drainage Failure Simulation
"""

import sys
import os
import argparse
import json

# Add project root to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.simulation.simulator import DrainageSimulator
from src.analysis.run_experiments import run_intensity_experiment
from src.visualization.visualize_network import visualize_graph

def main():
    parser = argparse.ArgumentParser(description='Drainage Failure Simulation')
    parser.add_argument('--steps', type=int, default=60, help='Number of simulation steps')
    parser.add_argument('--mode', choices=['simulate', 'analyze', 'visualize'],
                       default='simulate', help='Operation mode')
    parser.add_argument('--graph-path', default='data/drainage_graph.json',
                       help='Path to the drainage graph file')
    parser.add_argument('--output-dir', default='results', help='Output directory')

    args = parser.parse_args()

    if args.mode == 'simulate':
        print("Initializing Drainage Failure Simulation...")
        sim = DrainageSimulator(graph_path=args.graph_path)
        sim.run_simulation(steps=args.steps)
        print("Simulation completed successfully!")

    elif args.mode == 'analyze':
        print("Running intensity experiment...")
        run_intensity_experiment()
        print("Analysis completed!")

    elif args.mode == 'visualize':
        print("Generating network visualization...")
        visualize_graph(graph_path=args.graph_path)
        print("Visualization saved!")

if __name__ == "__main__":
    main()