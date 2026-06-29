#!/bin/bash

mkdir -p saved_run

NUM_SIM=1000

generate_tasks() {
    for DENSITY in $(seq 0 25); do
        POP=$(python3 -c "import math; print(round($DENSITY * 100 / math.pi))")
        
        for SUP in 0.0 0.2 0.4 0.6 0.8 1.0; do
            for MOD in 1 2; do
                if [ "$POP" -eq 0 ]; then
                    continue
                fi
                echo "python -m src.engine --sup_prob $SUP --env_pop $POP --model_type $MOD --num_sim $NUM_SIM --save_path /kaggle/working"
            done
        done
    done
}

# Determine the number of available CPU cores (fallback to 4 if nproc isn't available)
NUM_CORES=$(nproc 2>/dev/null || echo 4)
echo "Starting Monte Carlo simulations in parallel on $NUM_CORES cores..."

# Generate the commands, pipe them to xargs, and execute them concurrently
generate_tasks | xargs -P "$NUM_CORES" -I {} sh -c 'echo "Running: {}" && {}'

echo "All simulations completed successfully."
