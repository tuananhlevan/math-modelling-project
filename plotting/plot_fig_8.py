import numpy as np
import matplotlib.pyplot as plt
from plotting.utils import pad_or_truncate

def plot_fig_8():
    data_hub = np.load('saved_run/results_sup0.2_pop637_mod2.npz')
    data_normal = np.load('saved_run/results_sup0_pop637_mod2.npz')
    data_strong = np.load('saved_run/results_sup0.2_pop637_mod1.npz')
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
    plt.savefig('plots/fig_8_epidemic_curve.png', dpi=300)

if __name__ == '__main__':
    plot_fig_8()
