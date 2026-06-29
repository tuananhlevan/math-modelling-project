import numpy as np
import matplotlib.pyplot as plt
from src.engine import main_loop

def plot_fig_6(num_sim=300, env_pop=637, target_time_steps=40):
    lambdas = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
    plt.figure(figsize=(7, 5))
    markers = {0.0: 'o', 0.2: '*', 0.4: 's', 0.6: 'p', 0.8: '^', 1.0: 'v'}
    colors = {0.0: 'brown', 0.2: 'limegreen', 0.4: 'blue', 0.6: 'magenta', 0.8: 'cyan', 1.0: 'yellow'}
    
    for lam in lambdas:
        print(f'Running Monte Carlo for λ={lam}...')
        all_rf_curves = []
        for _ in range(num_sim):
            _, _, rf_curve = main_loop(sup_prob=lam, env_pop=env_pop, model_type=1)
            if len(rf_curve) < target_time_steps + 1:
                pad_length = target_time_steps + 1 - len(rf_curve)
                padded_rf = np.pad(rf_curve, (0, pad_length), mode='edge')
            else:
                padded_rf = rf_curve[:target_time_steps + 1]
            all_rf_curves.append(padded_rf)
        average_rf = np.mean(all_rf_curves, axis=0)
        plt.scatter(range(len(average_rf)), average_rf, label=f'λ={lam}', marker=markers[lam], color=colors[lam], s=30)
    
    plt.xlabel('time step')
    plt.ylabel('$r_f / r_0$')
    plt.xlim(0, 40)
    plt.ylim(0, 12)
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.tight_layout()
    plt.savefig('plots/fig_6_propagation_speed.png', dpi=300)

if __name__ == '__main__':
    plot_fig_6()
