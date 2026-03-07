#!/bin/bash

# Drainage Failure Simulation Initialization Script

echo "Initializing Drainage Failure Simulation..."

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python -m venv .venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Run a quick test simulation
echo "Running quick test simulation..."
python main.py --steps 10 --mode simulate

echo "Initialization complete!"
echo "You can now run:"
echo "  source .venv/bin/activate  # Activate virtual environment"
echo "  python main.py --mode simulate  # Run simulation"
echo "  python main.py --mode analyze   # Run analysis"
echo "  python main.py --mode visualize # Generate visualizations"