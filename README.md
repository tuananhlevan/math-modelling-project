# Epidemic Spread Superspreader Model

This repository contains a computational reimplementation of the spatial SIR epidemic model proposed by Ryo Fujie and Takashi Odagaki (*"Effects of superspreaders in spread of epidemic"*). The project evaluates two competing hypotheses for how "superspreaders" behave:
1. **Strong Infectiousness Model**: Superspreaders have a biologically higher transmission probability within a normal social radius.
2. **Hub Model**: Superspreaders have the same transmission probability curve, but possess a much wider radius of social connections.

## Project Structure

- `src/`: The core Python simulation engine utilizing Monte Carlo methods.
- `plot_results.py`: Script to generate all statistical figures and route-of-infection diagrams.
- `plots/`: Output directory containing generated data visualizations.
- `report/`: The LaTeX source code and compiled PDF for the technical modeling report.
- `demo/`: An interactive web-based visual simulation.

## Interactive Visual Demo

We have included a highly interactive, step-by-step visual demonstration of the infection network spreading across the 2D plane. 

**To use the demo:**
You do not need to install any web frameworks or dependencies. Simply open the `demo/index.html` file in any modern web browser.

```bash
# On Linux (Ubuntu/Debian):
xdg-open demo/index.html

# On macOS:
open demo/index.html
```

**Features:**
- Toggle seamlessly between the *Strong Infectiousness* and *Hub* models.
- Dynamically adjust the Environment Population ($N$) and the Superspreader Probability ($\lambda$).
- Step through the infection timestep by timestep, or auto-play with adjustable speeds.
- Visualize the explicit infection routes wrapping across the cylindrical boundary.

## Python Simulation

### Requirements
The core statistical simulations require Python 3 and a few standard scientific libraries:
```bash
pip install numpy matplotlib
```

### Running the Engine
You can manually run the Monte Carlo simulation engine and save the output array:
```bash
python -m src.engine \
  --sup_prob 0.2 \
  --env_pop 300 \
  --model_type 1 \
  --num_sim 1000 \
  --save_path ./saved_run/
```
*Note: `model_type 1` is the Strong Infectiousness model. `model_type 2` is the Hub model.*

### Plotting
To regenerate all the plots used in the report (including percolation probability, critical density, and network plots), run:
```bash
python plot_results.py
```
This script will parse the `.npz` files in `saved_run/` and output `.png` figures to the `plots/` directory.
