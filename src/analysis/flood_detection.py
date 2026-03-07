import json
import os
import pandas as pd

def analyze_results(log_path="results/simulation_logs/run_log.json"):
    if not os.path.exists(log_path):
        print(f"Log file {log_path} not found.")
        return
    
    with open(log_path, 'r') as f:
        history = json.load(f)
    
    df = pd.DataFrame(history)
    
    # Calculate key metrics
    max_flooded = df['flooded_nodes'].max()
    max_blocked = df['blocked_pipes'].max()
    peak_flow = df['total_flow'].max()
    
    # Resilience Index (Simplified: higher value = more resilient)
    # R = 1 - (max_flooded / total_nodes) - (max_blocked / total_pipes)
    # We'll just use counts for now.
    
    summary = {
        "Peak Flooded Nodes": int(max_flooded),
        "Peak Blocked Pipes": int(max_blocked),
        "Peak System Flow": float(peak_flow),
        "Duration": len(df)
    }
    
    print("\n--- Simulation Summary ---")
    for k, v in summary.items():
        print(f"{k}: {v}")
    
    with open("results/analysis_summary.json", 'w') as f:
        json.dump(summary, f, indent=2)
    print("\nSummary saved to results/analysis_summary.json")

if __name__ == "__main__":
    analyze_results()
