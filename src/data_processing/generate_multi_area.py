import os
import json
import sys

# Add project root to path
sys.path.append(os.getcwd())

from src.data_processing.download_osm import download_drainage_data
from src.data_processing.preprocess_data import preprocess_drainage
from src.graph_model.build_graph import build_drainage_graph, save_graph
from src.simulation.simulator import DrainageSimulator

AREAS = {
    "velachery": "Velachery, Chennai",
    "adyar": "Adyar, Chennai",
    "mylapore": "Mylapore, Chennai",
    "tnagar": "T. Nagar, Chennai"
}

def generate_area_data(area_id, place_name, intensity=50.0):
    print(f"\n{'='*40}")
    print(f"PROCESSING AREA: {area_id.upper()} (Intensity: {intensity} mm/hr)")
    print(f"{'='*40}")
    
    # Paths
    base_data = f"data/areas/{area_id}"
    base_results = f"results/areas/{area_id}"
    os.makedirs(base_data, exist_ok=True)
    os.makedirs(base_results, exist_ok=True)
    
    raw_path = f"{base_data}/raw.gpkg"
    clean_path = f"{base_data}/clean.gpkg"
    graph_path = f"{base_data}/graph.json"
    log_path = f"{base_results}/run_log.json"
    
    # 1. Download (Skip if exists to save time)
    if not os.path.exists(raw_path):
        download_drainage_data(place_name, output_path=raw_path)
    
    # 2. Preprocess
    preprocess_drainage(input_path=raw_path, output_path=clean_path)
    
    # 3. Build Graph
    G = build_drainage_graph(input_path=clean_path)
    if G:
        save_graph(G, output_path=graph_path)
        
        # 4. Run Simulation with custom intensity
        print(f"Running simulation for {area_id} at {intensity} mm/hr...")
        sim = DrainageSimulator(graph_path=graph_path)
        sim.run_step(0, intensity=intensity) # Prime it
        sim.run_simulation(steps=100) # Longer simulation
        
        # Move the default log to the area results
        # Fixed path after simulator.py output
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        if os.path.exists("results/simulation_logs/run_log.json"):
            os.replace("results/simulation_logs/run_log.json", log_path)
            print(f"Log saved to {log_path}")

if __name__ == "__main__":
    for area_id, place_name in AREAS.items():
        try:
            generate_area_data(area_id, place_name)
        except Exception as e:
            print(f"Failed to process {area_id}: {e}")
    
    # Create a manifest for the dashboard
    manifest = {
        "areas": [
            {"id": "velachery", "label": "Velachery (South Chennai)", "base_path": "areas/velachery"},
            {"id": "adyar", "label": "Adyar (Riverfront)", "base_path": "areas/adyar"},
            {"id": "mylapore", "label": "Mylapore (Heritage District)", "base_path": "areas/mylapore"},
            {"id": "tnagar", "label": "T. Nagar (Commercial Hub)", "base_path": "areas/tnagar"}
        ]
    }
    with open("data/manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)
    print("\nManifest generated at data/manifest.json")
