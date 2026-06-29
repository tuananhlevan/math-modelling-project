import numpy as np
import matplotlib.pyplot as plt
from src.engine import main_loop
from plotting.utils import calculate_velocity

def plot_fig_7(num_sim=300, env_pop=637):
    lambdas = np.arange(0.0, 1.01, 0.1)
    velocities_strong = []
    velocities_hub = []
    
    print('Evaluating Strong Infectiousness Model...')
    for lam in lambdas:
        all_curves = []
        for _ in range(num_sim):
            _, _, rf_curve = main_loop(sup_prob=lam, env_pop=env_pop, model_type=1)
            all_curves.append(rf_curve)
        max_len = max((len(c) for c in all_curves))
        padded_curves = [c + [c[-1]] * (max_len - len(c)) for c in all_curves]
        avg_rf_curve = np.mean(padded_curves, axis=0)
        v = calculate_velocity(avg_rf_curve)
        velocities_strong.append(v)
        print(f'  λ = {lam:.2f} -> Velocity = {v:.4f}')
    
    print('\nEvaluating Hub Model...')
    for lam in lambdas:
        all_curves = []
        for _ in range(num_sim):
            _, _, rf_curve = main_loop(sup_prob=lam, env_pop=env_pop, model_type=2)
            all_curves.append(rf_curve)
        max_len = max((len(c) for c in all_curves))
        padded_curves = [c + [c[-1]] * (max_len - len(c)) for c in all_curves]
        avg_rf_curve = np.mean(padded_curves, axis=0)
        v = calculate_velocity(avg_rf_curve)
        velocities_hub.append(v)
        print(f'  λ = {lam:.2f} -> Velocity = {v:.4f}')
    
    plt.figure(figsize=(7, 6))
    plt.plot(lambdas, velocities_strong, label='Strong infectiousness model', marker='o', color='red', linestyle='-', markersize=6)
    plt.plot(lambdas, velocities_hub, label='Hub model', marker='s', color='blue', linestyle='-', markersize=6)
    plt.xlabel('$\\lambda$')
    plt.ylabel('velocity ($/r_0 \\cdot s$)')
    plt.xlim(0, 1.0)
    plt.ylim(0, 1.6)
    plt.legend(loc='lower right')
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.tight_layout()
    plt.savefig('plots/fig_7_velocity_comparison.png', dpi=300)
    plt.show()

if __name__ == '__main__':
    plot_fig_7()
