sup_prob=(0 0.2 0.4 0.6 0.8 1)
env_pop=(150 300 450 600 750 900)
model_type=(1 2)

for i in "${sup_prob[@]}"; do
    for j in "${env_pop[@]}"; do
        for k in "${model_type[@]}"; do
            echo "Running Monte Carlo simulation on 
                    Superspreader probability: ${i}
                    Environment population: ${j}
                    Model type: ${k}"
                
            python src/engine.py \
                --num_sim 150 \
                --save_path log \
                --sup_prob $i \
                --env_pop $j \
                --model_type $k
        done
    done
done