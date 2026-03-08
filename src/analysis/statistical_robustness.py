import matplotlib.pyplot as plt
import numpy as np
import os
import sys
import random

# Add project root to path
sys.path.append(os.getcwd())

from src.visualization.plot_style import set_professional_style, get_color_palette
set_professional_style()
colors = get_color_palette()

from src.simulation.simulator import DrainageSimulator

def run_statistical_intensity_experiment(intensities=[10, 30, 50, 75, 100], iterations=10):
    """
    Runs repeated simulations to calculate Mean and Std Dev of flood nodes and cascade depth.
    """
    print(f"Running Statistical Robustness Analysis ({iterations}x repeats)...")
    flood_results = {i: [] for i in intensities}
    cascade_results = {i: [] for i in intensities}
    vfail_results = {i: [] for i in intensities}
    
    for intensity in intensities:
        print(f"  Simulating Intensity: {intensity} mm/hr")
        for j in range(iterations):
            # Use random seeds for Monte Carlo variation
            sim = DrainageSimulator()
            for t in range(50):
                sim.run_step(t, intensity=intensity) 
            
            stats = sim.get_stats()
            flood_results[intensity].append(stats['flooded_nodes'])
            cascade_results[intensity].append(stats['cascade_depth'])
            # v_fail = blocked_pipes / total_time_steps
            # Assuming stats['blocked_pipes'] exists or calculating from sim.G
            blocked_count = len([e for e, data in sim.G.edges(data=True) if data.get('status') == 'blocked'])
            vfail_results[intensity].append(blocked_count / 50.0)

    # Calculate statistics for Inundation
    flood_means = [np.mean(flood_results[i]) for i in intensities]
    flood_std = [np.std(flood_results[i]) for i in intensities]

    # Calculate statistics for Cascade Depth
    cascade_means = [np.mean(cascade_results[i]) for i in intensities]
    cascade_std = [np.std(cascade_results[i]) for i in intensities]

    # Plot 8: Statistical Sensitivity (Flood Nodes)
    plt.figure(figsize=(7, 5))
    plt.errorbar(intensities, flood_means, yerr=flood_std, fmt='-o', color='#ae2012', 
                 ecolor='#e5989b', elinewidth=2, capsize=5, label=r'Inundation ($\mu \pm \sigma$)')
    plt.fill_between(intensities, np.array(flood_means)-np.array(flood_std), np.array(flood_means)+np.array(flood_std), 
                     color='#ae2012', alpha=0.1)
    
    plt.title("Stochastic Inundation Sensitivity")
    plt.xlabel("Rainfall Intensity (mm/hr)")
    plt.ylabel(r"Inundated Node Count ($N_{flood}$)")
    plt.legend(frameon=True)
    plt.tight_layout()
    plt.savefig("results/figures/plot8_statistical_sensitivity.png", dpi=600)
    plt.close()

    # Calculate statistics for Failure Velocity
    vfail_means = [np.mean(vfail_results[i]) for i in intensities]
    vfail_std = [np.std(vfail_results[i]) for i in intensities]

    # Plot 11: Failure Velocity vs Intensity
    plt.figure(figsize=(7, 5))
    plt.errorbar(intensities, vfail_means, yerr=vfail_std, fmt='-D', color='#9b2226', 
                 ecolor='#ca6702', elinewidth=2, capsize=5, label=r'Failure Velocity ($v_{fail}$)')
    plt.title("Failure Propagation Rate vs Storm Intensity")
    plt.xlabel("Rainfall Intensity (mm/hr)")
    plt.ylabel(r"Failure Velocity ($v_{fail}$)")
    plt.legend(frameon=True)
    plt.tight_layout()
    plt.savefig("results/figures/plot11_vfail_intensity.png", dpi=600)
    plt.close()

    # Plot 10: Cascade Depth vs Intensity
    plt.figure(figsize=(7, 5))
    plt.errorbar(intensities, cascade_means, yerr=cascade_std, fmt='-s', color='#005f73', 
                 ecolor='#94d2bd', elinewidth=2, capsize=5, label=r'Cascade Depth ($\Lambda_{mean}$)')
    plt.title("Failure Propagation Complexity vs Storm Intensity")
    plt.xlabel("Rainfall Intensity (mm/hr)")
    plt.ylabel(r"Mean Cascade Depth ($\Lambda$)")
    plt.legend(frameon=True)
    plt.tight_layout()
    plt.savefig("results/figures/plot10_cascade_intensity.png", dpi=600)
    plt.close()
    
    print("Statistical experiments and Plot 10 generated.")

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
    plt.figure(figsize=(7, 5))
    plt.plot(prop_history, color='#ae2012', linewidth=3, label="Proposed (Graph Grammar)")
    plt.plot(base_history, color='#005f73', linewidth=2, linestyle='--', label="Baseline (Uniform Flow)")
    
    plt.title("Model Convergence & Comparative Accuracy")
    plt.xlabel("Simulation Steps (Time)")
    plt.ylabel("Detected Inundated Nodes")
    plt.legend(frameon=True, loc='upper left')
    plt.tight_layout()
    plt.savefig("results/figures/plot9_baseline_comparison.png", dpi=600)
    plt.close()
    
    print("Baseline comparison plot generated.")

if __name__ == "__main__":
    os.makedirs("results/figures", exist_ok=True)
    run_statistical_intensity_experiment()
    run_baseline_comparison()
    print("Research-grade statistical & baseline experiments complete.")
