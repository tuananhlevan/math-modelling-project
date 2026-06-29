#!/bin/bash

mkdir -p saved_run

NUM_SIM=1000

echo "Starting Monte Carlo simulations..."
for DENSITY in $(seq 0 25); do
    POP=$(python3 -c "import math; print(round($DENSITY * 100 / math.pi))")
    
    for SUP in 0.0 0.2 0.4 0.6 0.8 1.0; do
        for MOD in 1 2; do
            if [ "$POP" -eq 0 ]; then
                continue
            fi
            echo "Running Density=$DENSITY (N=$POP), lambda=$SUP, model=$MOD..."
            python -m src.engine --sup_prob $SUP --env_pop $POP --model_type $MOD --num_sim $NUM_SIM --save_path ./saved_run/
        done
    done
done

echo "All simulations completed successfully."
