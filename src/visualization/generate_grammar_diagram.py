import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os
import sys

# Add project root to path
sys.path.append(os.getcwd())

from src.visualization.plot_style import set_professional_style
set_professional_style()

def generate_grammar_transformation(output_path="results/figures/grammar_transformation.png"):
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 40)
    ax.axis('off')

    # Styles
    C_ACTIVE = '#94d2bd'
    C_BLOCK = '#ae2012'
    C_SURCH = '#e9d8a6'
    C_EDGE = '#005f73'

    # Helper for circles
    def add_node(x, y, label, color):
        ax.add_patch(plt.Circle((x, y), 3, color=color, ec='black', lw=1.5, zorder=5))
        ax.text(x, y-1, label, ha='center', va='top', fontsize=9, fontweight='bold')

    # Helper for pipes
    def add_pipe(x1, y1, x2, y2, label, status='active'):
        color = C_BLOCK if status == 'blocked' else C_EDGE
        ls = '--' if status == 'blocked' else '-'
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='->', color=color, linestyle=ls, linewidth=3, shrinkA=5, shrinkB=5))
        ax.text((x1+x2)/2, (y1+y2)/2 + 2, label, ha='center', fontsize=8, fontweight='bold', color=color)

    # STATE 1: Normal Flow
    add_node(10, 20, "Node A", C_ACTIVE)
    add_node(30, 20, "Node B", C_ACTIVE)
    add_pipe(10, 20, 30, 20, "Q = 0.8C", 'active')
    ax.text(20, 10, "1. Hydraulic Equilibrium", ha='center', fontweight='black', color=C_EDGE)

    # Transition Arrow
    ax.annotate('', xy=(42, 20), xytext=(36, 20), arrowprops=dict(arrowstyle='->', color='gray', lw=2))

    # STATE 2: Blockage (Rule 4)
    add_node(50, 20, "Node A", C_ACTIVE)
    add_node(70, 20, "Node B", C_ACTIVE)
    add_pipe(50, 20, 70, 20, "BLOCKED!", 'blocked')
    ax.add_patch(plt.Rectangle((58, 18), 4, 4, color=C_BLOCK, alpha=0.8, zorder=6))
    ax.text(60, 10, "2. Structural Transformation", ha='center', fontweight='black', color=C_BLOCK)

    # Transition Arrow
    ax.annotate('', xy=(82, 20), xytext=(76, 20), arrowprops=dict(arrowstyle='->', color='gray', lw=2))

    # STATE 3: Upstream Cascade (Rule 7)
    add_node(90, 20, "Node A", C_BLOCK) # Node A now surcharging
    ax.text(90, 25, "Surcharging!", color=C_BLOCK, fontsize=8, ha='center', fontweight='black')
    ax.text(90, 10, "3. Upstream Cascade", ha='center', fontweight='black', color=C_BLOCK)

    plt.title("Graph Grammar State Transition: $G_t \\to G_{t+1}$", pad=10, fontsize=14, fontweight='black')
    plt.tight_layout()
    plt.savefig(output_path, dpi=600, bbox_inches='tight')
    plt.close()
    print(f"Grammar transformation diagram saved to {output_path}")

if __name__ == "__main__":
    os.makedirs("results/figures", exist_ok=True)
    generate_grammar_transformation()
