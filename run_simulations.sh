#!/bin/bash
# run_simulations.sh
# Runs the simulations with the numbers specified in the reference paper
# "Effects of superspreaders in spread of epidemic"

# Create the output directory if it doesn't exist
mkdir -p saved_run

# The reference paper states:
# "Monte Carlo simulation was performed from N = 150 to 900 on L x L continuous space..."
# "...averaging over 1000 Monte Carlo runs"
NUM_SIM=1000

echo "Starting Monte Carlo simulations..."

# 1. Sweep over Density from 0 to 25
#    Density = (POP / 100) * pi  =>  POP = round(Density * 100 / pi)
for DENSITY in $(seq 0 25); do
    # Calculate corresponding population integer using Python
    POP=$(python3 -c "import math; print(round($DENSITY * 100 / math.pi))")
    
    # Sweep over lambda (Superspreader Probability) from 0.0 to 1.0
    for SUP in 0.0 0.2 0.4 0.6 0.8 1.0; do
        for MOD in 1 2; do
            # Skip if density is 0 and population is 0 (simulation might break or be trivial)
            if [ "$POP" -eq 0 ]; then
                continue
            fi
            echo "Running Density=$DENSITY (N=$POP), lambda=$SUP, model=$MOD..."
            python -m src.engine --sup_prob $SUP --env_pop $POP --model_type $MOD --num_sim $NUM_SIM --save_path ./saved_run/
        done
    done
done

echo "All simulations completed successfully."
