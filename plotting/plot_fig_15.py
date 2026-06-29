import numpy as np
import matplotlib.pyplot as plt
from plotting.utils import pad_or_truncate

def plot_fig_15():
    sars_time_steps = np.arange(13)
    sars_counts = np.zeros(13)
    sars_counts[3] = 3
    sars_counts[4] = 20
    sars_counts[5] = 51
    sars_counts[6] = 17
    sars_counts[7] = 16
    sars_counts[8] = 40
    sars_counts[9] = 27
    sars_counts[10] = 12
    sars_counts[11] = 8
    
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.bar(sars_time_steps, sars_counts, color='orange', width=1.0, edgecolor='white', linewidth=0.5, label='data of SARS in Singapore', alpha=0.9)
    
    data_hub = np.load('saved_run/results_sup0.4_pop477_mod2.npz')
    data_normal = np.load('saved_run/results_sup0_pop477_mod2.npz')
    data_strong = np.load('saved_run/results_sup0.4_pop477_mod1.npz')
    
    curve_hub = pad_or_truncate(data_hub['epi_curve'], 41)
    curve_normal = pad_or_truncate(data_normal['epi_curve'], 41)
    curve_strong = pad_or_truncate(data_strong['epi_curve'], 41)
    plt.plot(curve_hub, label='Hub Model (λ=0.2)', marker='s')
    plt.plot(curve_normal, label='(λ=0.0)', marker='^')
    plt.plot(curve_strong, label='Strong (λ=0.2)', marker='o')
    plt.xlabel('Time Step')
    plt.ylabel('Number of Newly Infected')
    plt.xlim(0, 40)
    plt.legend()
    plt.savefig('plots/fig_15_epidemic_curve.png', dpi=300)

if __name__ == '__main__':
    plot_fig_15()
