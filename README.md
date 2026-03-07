# Graph Grammar–Based Drainage Failure Simulation Framework

## 1. Project Overview
This repository contains a research-grade framework for simulating cascading failures in urban drainage networks using a **Bimodal Simulation Engine**. The system integrates traditional **Manning's Hydraulics** with a novel **Graph Grammar Rule Engine** to model how localized pipe blockages propagate structural and hydraulic stress across an infrastructure network.

### Key Innovations:
- **Graph Grammar Modeling**: Treats network failures as topological "rewrites" rather than just hydraulic anomalies.
- **Physics-Aware**: Grounded in Manning's equation for realistic gravity-driven flow.
- **Advanced Analytics**: Built-in metrics for Network Resilience ($R$), Cascade Depth ($D$), and Impact Scoring ($I$).
- **DrainFlex PRO Dashboard**: A professional React/Vite/Force-Graph interface for real-time simulation playback.

---

## 2. Mathematical Foundation & Logic

### A. Graph Representation
The drainage network is modeled as an attributed directed graph $G = (V, E)$.
- **Nodes ($V$)**: Represent junctions, manholes, or outlets. Attributes include elevation ($z$), water level ($L$), and catchment area ($A_c$).
- **Edges ($E$)**: Represent circular pipelines. Attributes include diameter ($d$), roughness ($n$), slope ($S$), and logical status (active, overloaded, blocked).

### B. Hydraulic Simulation (The Physics)
The core flow logic uses **Manning's Equation** to determine the maximum discharge capacity ($Q_{cap}$) of each pipe:
$$V = \frac{1}{n} R_h^{2/3} S^{1/2}$$
$$Q_{cap} = V \cdot A$$
Where:
- $n$: Roughness coefficient (default: 0.013 for concrete).
- $R_h$: Hydraulic Radius ($d/4$ for full pipe flow).
- $S$: Hydraulic Gradient (Pipe Slope), calculated as $\frac{Elev_{source} - Elev_{target}}{Length}$.

### C. The Graph Grammar Engine (The Logic)
The simulation proceeds in discrete time steps ($\Delta t$). At each step, 8 production rules are evaluated:

1. **Rule 1 - Rainfall Inflow ($R_{inflow}$)**:
   - **Logic**: Water enters nodes based on current rainfall intensity.
   - **Formula**: $L_v(t+1) = L_v(t) + (Intensity(t) \cdot A_c \cdot \Delta t)$.
   - **Stochasticity**: $A_c$ is randomized per node ($\mu=5000, \sigma=500$) for research robustness.

2. **Rule 2 - Gravity Flow ($R_{gravity}$)**:
   - **Logic**: Water moves from high-elevation nodes to low-elevation nodes through active pipes.
   - **Constraint**: Flow is limited by the $Q_{cap}$ calculated in the Physics layer.

3. **Rule 3 - Pipe Overload ($R_{overload}$)**:
   - **LHS Condition**: Flow $Q_{actual} > Q_{cap}$.
   - **Transformation**: Edge status is set to `overloaded`.

4. **Rule 4 - Blockage Formation ($R_{block}$)**:
   - **Logic**: Physical blockage occurs if a pipe remains overloaded for $T > \tau$ steps (simulating debris accumulation).
   - **Transformation**: Edge status is set to `blocked`. Capacity becomes 0.

5. **Rule 6 - Node Overflow ($R_{flood}$)**:
   - **LHS Condition**: $L_v > Capacity_v$.
   - **Transformation**: Node is marked as `flooded`.

6. **Rule 7 - Cascading Failure ($R_{cascade}$)**:
   - **Logic**: A blocked downstream pipe creates "back-pressure" upstream.
   - **Transformation**: Upstream pipes connected to the blocked node suffer a 20% reduction in effective capacity.

7. **Rule 5 - Flow Rerouting ($R_{reroute}$)**:
   - **Logic**: If the primary path is blocked, the engine seeks alternate outgoing edges from the junction manhole.

8. **Rule 8 - System Recovery ($R_{recess}$)**:
   - **Logic**: Downward intensity leads to water depletion through network outlets.

---

## 3. Evaluation Metrics

### Network Resilience ($R$)
Measures the system's ability to maintain function:
$$R = 1 - \frac{N_{flooded}}{N_{total}}$$
A value of 1.0 represents perfect performance; 0.0 represents total system collapse.

### Cascade Depth ($D$)
The maximum length of a failure chain. If Blockage A leads to Overload B which leads to Blockage C, the depth is the topological distance of this propagation.

### Impact Score ($I$)
Calculated via a "Leave-One-Out" stochastic experiment. For each node $v$:
$$I(v) = \frac{\text{Projected Inundation After Failure of } v}{\text{Total Network Scale}}$$
Helps identify **Critical Infrastructure Nodes**.

---

## 4. Software Architecture

### Backend (Python)
- `src/simulation/simulator.py`: The heart of the engine; implements the time-stepping loop and hydraulics.
- `src/grammar_engine/rule_engine.py`: Manages the application of the 8 Graph Grammar rules.
- `src/analysis/advanced_metrics.py`: Computes research metrics (Resilience, Cascade Depth).

### Frontend (React/Vite)
- `dashboard/src/App.jsx`: State-of-the-art geo-topology visualization.
- **Features**:
  - Live simulation playback (step through history).
  - Node hover details with geospatial data.
  - Animated flow particles representing hydraulic load.

---

## 5. Usage & Reproduction

### Prerequisites
- Python 3.9+
- Node.js 18+

### Installation
1. Clone the repository: `git clone <repo_url>`
2. Initialize environment: `./init.sh`
3. Install Dashboard dependencies: `cd dashboard && npm install`

### Run Simulation
```bash
# Generate a new simulation run
python3 main.py --mode simulate

# Run analytical experiments (generates figures)
python3 main.py --mode analyze
```

### Start Dashboard
```bash
cd dashboard
npm run dev
```

---

## 6. Research Documentation
- **Methodology**: Detailed in `paper.tex` (IEEE LaTeX Format).
- **System Architecture**: Professional diagram available in `results/figures/`.
- **Case Study**: Focused on **Velachery, Chennai**, using real-world OSM topology and DEM elevation profiling.

---
*Created as part of an advanced study into Urban Infrastructure Resilience.*