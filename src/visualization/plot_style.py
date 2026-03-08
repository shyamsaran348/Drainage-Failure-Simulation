import matplotlib.pyplot as plt
import matplotlib as mpl

def set_professional_style():
    """
    Sets a professional, journal-ready style for matplotlib plots.
    """
    # Use a clean, professional aesthetic
    plt.style.use('seaborn-v0_8-muted')
    
    # Configure global RC parameters
    mpl.rcParams.update({
        'font.family': 'sans-serif',
        'font.sans-serif': ['Inter', 'Roboto', 'Helvetica', 'Arial', 'DejaVu Sans'],
        'font.size': 10,
        'axes.labelsize': 11,
        'axes.titlesize': 12,
        'xtick.labelsize': 9,
        'ytick.labelsize': 9,
        'legend.fontsize': 9,
        'figure.titlesize': 14,
        'figure.dpi': 300,
        'savefig.dpi': 600,
        'axes.spines.top': False,
        'axes.spines.right': False,
        'axes.grid': True,
        'grid.alpha': 0.3,
        'grid.linestyle': '--',
        'lines.linewidth': 2.0,
        'lines.markersize': 6,
        'axes.prop_cycle': mpl.cycler(color=['#005f73', '#0a9396', '#94d2bd', '#e9d8a6', '#ee9b00', '#ca6702', '#bb3e03', '#ae2012', '#9b2226'])
    })

def get_color_palette():
    """Returns a scholarly color palette."""
    return ['#005f73', '#ae2012', '#0a9396', '#ee9b00', '#9b2226']
