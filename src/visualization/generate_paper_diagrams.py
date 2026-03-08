import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os
import sys

# Add project root to path
sys.path.append(os.getcwd())

from src.visualization.plot_style import set_professional_style

set_professional_style()

def generate_system_architecture(output_path="results/figures/final_system_architecture.png"):
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Color Palette: Deep Academic
    C_PRIMARY = '#1D3557' # Deep Blue
    C_SECONDARY = '#457B9D' # Mid Blue
    C_ACCENT = '#E63946' # Red for stressors
    C_SILVER = '#F1FAEE' # Background light
    C_EDGE = '#A8DADC' # Edge blue

    # Helper for styled boxes
    def add_layer_box(x, y, w, h, title, sub_items, color_base):
        # Background shadow-like effect
        ax.add_patch(patches.FancyBboxPatch((x+0.5, y-0.5), w, h, boxstyle="round,pad=1.5", 
                                             facecolor='gray', alpha=0.1, zorder=1))
        # Main box
        ax.add_patch(patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=1.5", 
                                             facecolor=color_base, alpha=0.08, 
                                             edgecolor=color_base, linewidth=2, zorder=2))
        # Header bar
        ax.add_patch(patches.Rectangle((x, y+h-5), w, 5, facecolor=color_base, alpha=0.8, zorder=3))
        ax.text(x + w/2, y + h - 2.5, title.upper(), ha='center', va='center', 
                color='white', fontsize=11, fontweight='black', zorder=4)
        
        # Sub-components as mini-boxes
        for i, item in enumerate(sub_items):
            iy = y + h - 15 - (i * 12)
            ax.add_patch(patches.Rectangle((x+3, iy), w-6, 9, facecolor='white', 
                                         edgecolor=color_base, alpha=0.9, linewidth=0.8, zorder=3))
            ax.text(x + w/2, iy + 4.5, item, ha='center', va='center', 
                    color=C_PRIMARY, fontsize=9, fontweight='bold', zorder=4)

    # 1. DATA ACQUISITION LAYER (Left)
    add_layer_box(5, 25, 20, 50, "Data Ingestion", 
                  ["OSM Topology", "NASA SRTM (DEM)", "Manning Constants", "Synthetic Storms"], C_PRIMARY)

    # 2. BIMODAL ENGINE LAYER (Center)
    # Background for the core engine grouping
    ax.add_patch(patches.FancyBboxPatch((32, 15), 36, 70, boxstyle="round,pad=2", 
                                         facecolor='#f8f9fa', edgecolor=C_SECONDARY, 
                                         linestyle='--', linewidth=1, alpha=0.5, zorder=1))
    ax.text(50, 88, "BIMODAL SIMULATION KERNEL", ha='center', fontweight='black', color=C_SECONDARY, fontsize=12)

    # Physics Core
    add_layer_box(35, 45, 30, 25, "Physics Core", 
                  ["Manning Flux Solver", "Back-Pressure Matrix"], C_SECONDARY)
    
    # Logic Grammar
    add_layer_box(35, 20, 30, 20, "Graph Grammar", 
                  ["8-Rule RHS Library", "Structural Rewriter"], C_ACCENT)

    # 3. ANALYSIS & VIS LAYER (Right)
    add_layer_box(75, 25, 20, 50, "Analytics Suite", 
                  ["Resilience Index", "Cascade Analysis", "Stochastic Metrics", "Statistical Export"], C_PRIMARY)

    # CONNECTOR ARROWS (Professional Style)
    arrow_props = dict(arrowstyle='simple,head_width=1.2,head_length=1.5', facecolor=C_SECONDARY, edgecolor='none', alpha=0.6)
    
    # Data to Engine
    ax.annotate('', xy=(34, 50), xytext=(26, 50), arrowprops=arrow_props)
    
    # Engine Internal loop
    ax.annotate('', xy=(50, 44), xytext=(50, 41), arrowprops=dict(arrowstyle='<->', color=C_ACCENT, linewidth=1.5))
    
    # Engine to Analysis
    ax.annotate('', xy=(74, 50), xytext=(66, 50), arrowprops=arrow_props)

    # TITLE & LEGEND
    plt.title("Formal UDN Cascading Failure Simulation Framework", pad=35, fontsize=16, fontweight='black', color=C_PRIMARY)
    
    # High-res save
    plt.tight_layout()
    plt.savefig(output_path, dpi=600, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"Professional system architecture saved to {output_path}")

def generate_simulation_workflow(output_path="results/figures/simulation_workflow_formal.png"):
    fig, ax = plt.subplots(figsize=(8, 10))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    steps = [
        ("INITIALIZATION", "Topology Generation & DEM Alignment"),
        ("FLUX STEP", "Manning Equation Iteration"),
        ("MATCHING", "Grammar Rule Search (LHS Pattern)"),
        ("TRANSFORM", "Topological Production (RHS)"),
        ("CASCADE", "Recursive Failure Propagation"),
        ("VALIDATION", "Stochastic Metric Computation")
    ]
    
    for i, (title, desc) in enumerate(steps):
        y = 85 - (i * 15)
        # Box
        ax.add_patch(patches.FancyBboxPatch((20, y), 60, 10, boxstyle="round,pad=1.5", 
                                             facecolor='white', edgecolor='#1D3557', linewidth=1.5))
        # Title
        ax.text(50, y+7, title, ha='center', va='center', fontsize=10, fontweight='black', color='#E63946')
        # Description
        ax.text(50, y+3, desc, ha='center', va='center', fontsize=8, color='#457B9D')
        
        # Connection
        if i < len(steps) - 1:
            ax.annotate('', xy=(50, y-5), xytext=(50, y), 
                        arrowprops=dict(arrowstyle='->', color='#1D3557', linewidth=1.2))

    plt.title("Bimodal Execution Workflow", pad=20, fontsize=14, fontweight='black')
    plt.savefig(output_path, dpi=600, bbox_inches='tight')
    plt.close()
    print(f"Professional simulation workflow saved to {output_path}")

if __name__ == "__main__":
    os.makedirs("results/figures", exist_ok=True)
    generate_system_architecture()
    generate_simulation_workflow()
