import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os
import sys

# Add project root to path
sys.path.append(os.getcwd())

from src.visualization.plot_style import set_professional_style
set_professional_style()

def generate_rule_interaction(output_path="results/figures/rule_logic_flow.png"):
    fig, ax = plt.subplots(figsize=(8, 10))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 120)
    ax.axis('off')

    # Styles
    BOX_STYLE = dict(boxstyle='round,pad=0.5', fc='#e9d8a6', ec='#94d2bd', lw=2)
    RULE_STYLE = dict(boxstyle='round,pad=0.3', fc='#ae2012', ec='black', lw=1.5)
    ARROW_PROPS = dict(arrowstyle='->', color='#005f73', lw=2.5)

    def add_box(x, y, text, style=BOX_STYLE, fontsize=10):
        ax.text(x, y, text, ha='center', va='center', bbox=style, fontsize=fontsize, fontweight='bold')

    # Title
    ax.text(50, 115, "Graph Grammar Execution Logic", ha='center', fontsize=14, fontweight='black')

    # Flow
    add_box(50, 105, "Hydraulic Simulation (Manning's Flux)")
    
    ax.annotate('', xy=(50, 95), xytext=(50, 100), arrowprops=ARROW_PROPS)
    add_box(50, 90, "Condition Check: $\int (q - C) dt > \Theta$")

    ax.annotate('', xy=(50, 80), xytext=(50, 85), arrowprops=ARROW_PROPS)
    add_box(50, 75, "Rule R4 Triggered (Structural Rewrite)", style=RULE_STYLE)
    ax.text(50, 70, "$\Psi(e).status \leftarrow 'blocked'$ ", ha='center', fontsize=9, color='#ae2012', fontweight='bold')

    ax.annotate('', xy=(50, 60), xytext=(50, 65), arrowprops=ARROW_PROPS)
    add_box(50, 55, "Hydraulic Gradient Reversal ($R_5$)")

    ax.annotate('', xy=(50, 45), xytext=(50, 50), arrowprops=ARROW_PROPS)
    add_box(50, 40, "Rule R7 Triggered (Upstream Cascade)", style=RULE_STYLE)
    ax.text(50, 35, "$P_{upstream} \leftarrow P_{upstream} + \alpha$", ha='center', fontsize=9, color='#ae2012', fontweight='bold')

    ax.annotate('', xy=(50, 25), xytext=(50, 30), arrowprops=ARROW_PROPS)
    add_box(50, 20, "State Transition $G_t \to G_{t+1}$ complete")

    # Loop back
    ax.annotate('', xy=(85, 105), xytext=(85, 20), arrowprops=dict(arrowstyle='-', color='gray', lw=1, ls='--'))
    ax.annotate('', xy=(55, 105), xytext=(85, 105), arrowprops=dict(arrowstyle='->', color='gray', lw=1, ls='--'))
    ax.annotate('', xy=(85, 20), xytext=(55, 20), arrowprops=dict(arrowstyle='-', color='gray', lw=1, ls='--'))
    ax.text(90, 62.5, "Next Time Step", rotation=270, va='center', fontsize=8, color='gray')

    plt.tight_layout()
    plt.savefig(output_path, dpi=600, bbox_inches='tight')
    plt.close()
    print(f"Rule interaction diagram saved to {output_path}")

if __name__ == "__main__":
    os.makedirs("results/figures", exist_ok=True)
    generate_rule_interaction()
