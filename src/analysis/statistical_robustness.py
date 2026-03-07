import matplotlib.pyplot as plt
import numpy as np
import os
import sys
import random

# Add project root to path
sys.path.append(os.getcwd())

from src.simulation.simulator import DrainageSimulator

def run_statistical_intensity_experiment(intensities=[10, 30, 50, 75, 100], iterations=10):
    """
    Runs repeated simulations to calculate Mean and Std Dev of flood nodes.
    """
    print(f"Running Statistical Robustness Analysis ({iterations}x repeats)...")
    results = {i: [] for i in intensities}
    
    for intensity in intensities:
        print(f"  Simulating Intensity: {intensity} mm/hr")
        for _ in range(iterations):
            sim = DrainageSimulator()
            # Overwrite inflow logic or just run steps (stochasticity is now in simulator.py)
            for t in range(50):
                sim.run_step(t, intensity=intensity) 
                               # but we should ideally pass it. 
                               # For this experiment, we'll assume the simulator uses the target intensity.
            
            stats = sim.get_stats()
            results[intensity].append(stats['flooded_nodes'])

    # Calculate statistics
    means = [np.mean(results[i]) for i in intensities]
    std_devs = [np.std(results[i]) for i in intensities]

    # Plot Plot 8: Statistical Sensitivity with Error Bars
    plt.figure(figsize=(10, 6))
    plt.errorbar(intensities, means, yerr=std_devs, fmt='bo-', capsize=5, linewidth=2, label="Mean Inundation")
    plt.fill_between(intensities, np.array(means)-np.array(std_devs), np.array(means)+np.array(std_devs), alpha=0.2)
    plt.title("Statistical Sensitivity: Inundation vs. Rainfall Intensity", fontsize=14, fontweight='bold')
    plt.xlabel("Rainfall Intensity (mm/hr)", fontsize=12)
    plt.ylabel("Inundated Nodes (Mean \u00b1 SD)", fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.savefig("results/figures/plot8_statistical_sensitivity.png", dpi=300)
    plt.close()

def run_baseline_comparison(intensity=50.0):
    """
    Compares Graph Grammar (Proposed) vs. Uniform Flow (Baseline).
    """
    print(f"Running Baseline Comparison at {intensity} mm/hr...")
    
    # 1. Run Proposed Model (with rules)
    sim_prop = DrainageSimulator(use_rules=True)
    prop_history = []
    for t in range(100):
        stats = sim_prop.run_step(t, intensity=intensity)
        prop_history.append(stats['flooded_nodes'])
        
    # 2. Run Baseline Model (No rules enabled)
    sim_base = DrainageSimulator(use_rules=False)
    base_history = []
    for t in range(100):
        stats = sim_base.run_step(t, intensity=intensity)
        base_history.append(stats['flooded_nodes'])
        
    # Plot Plot 9: Baseline Comparison
    plt.figure(figsize=(10, 6))
    plt.plot(prop_history, 'r-', linewidth=3, label="Proposed (Graph Grammar)")
    plt.plot(base_history, 'b--', linewidth=2, label="Baseline (Uniform Flow)")
    plt.title("Methodology Comparison: Flood Capture Efficiency", fontsize=14, fontweight='bold')
    plt.xlabel("Simulation Time (Steps)", fontsize=12)
    plt.ylabel("Inundated Nodes", fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig("results/figures/plot9_baseline_comparison.png", dpi=300)
    plt.close()
    
    print("Baseline comparison plot generated.")

if __name__ == "__main__":
    os.makedirs("results/figures", exist_ok=True)
    run_statistical_intensity_experiment()
    run_baseline_comparison()
    print("Research-grade statistical & baseline experiments complete.")
