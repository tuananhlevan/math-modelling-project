sup_prob=(0 0.2 0.4 0.6 0.8 1)
env_pop=(150 300 450 600 750 900)
model_type=(1 2)

mk_dir -p saved_run

for i in "${sup_prob[@]}"; do
    for j in "${env_pop[@]}"; do
        for k in "${model_type[@]}"; do
            python src/engine.py \
                --num_sim 150 \
                --save_path saved_run \
                --sup_prob $i \
                --env_pop $j \
                --model_type $k
        done
    done
done