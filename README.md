# Drainage Failure Simulation

This project simulates drainage system failures under various conditions.

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   ```

2. Activate the virtual environment:
   ```bash
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

The main entry point is `main.py` which supports three modes:

### Simulation Mode
Run a drainage failure simulation:
```bash
python main.py --mode simulate --steps 100
```

### Analysis Mode
Run sensitivity analysis experiments:
```bash
python main.py --mode analyze
```

### Visualization Mode
Generate visualizations of the network:
```bash
python main.py --mode visualize
```

## Command Line Options

- `--steps`: Number of simulation steps (default: 60)
- `--mode`: Operation mode: simulate, analyze, or visualize (default: simulate)
- `--graph-path`: Path to the drainage graph file (default: data/drainage_graph.json)
- `--output-dir`: Output directory (default: results)

## Project Structure

- `src/`: Source code
  - `simulation/`: Core simulation engine
  - `analysis/`: Analysis tools and experiments
  - `visualization/`: Visualization tools
  - `data_processing/`: Data preprocessing utilities
  - `graph_model/`: Graph construction and manipulation
  - `grammar_engine/`: Rule-based failure modeling
- `data/`: Input data files
- `results/`: Output files and visualizations
- `requirements.txt`: Python dependencies