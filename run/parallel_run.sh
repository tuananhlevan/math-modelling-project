#!/bin/bash
sup_prob=(0 0.2 0.4 0.6 0.8 1)
env_pop=(150 300 450 600 750 900)
model_type=(1 2)

mkdir -p saved_run

# -j 8 runs 8 jobs at a time. Adjust this based on your CPU cores.
# ::: passes the arrays as arguments to the command.
parallel -j 8 python src/engine.py \
    --num_sim 1000 \
    --save_path saved_run \
    --sup_prob {1} \
    --env_pop {2} \
    --model_type {3} \
    ::: "${sup_prob[@]}" ::: "${env_pop[@]}" ::: "${model_type[@]}"