import os
import glob
import numpy as np
import matplotlib.pyplot as plt

def plot_fig_4():
    files = glob.glob(f'saved_run/results_sup*_pop*_mod2.npz')
    data_map = {}

    for file in files:
        parts = os.path.basename(file).split('_')
        sup = float(parts[1].replace('sup', ''))
        pop = int(parts[2].replace('pop', ''))
        density = pop / 100.0 * np.pi * 1 ** 2
        data = np.load(file)
        prob = data['perc_prob']
        if sup not in data_map:
            data_map[sup] = [(0, 0)]
        data_map[sup].append((density, prob))
    
    plt.figure(figsize=(7, 5))
    
    for sup in sorted(data_map.keys()):
        sorted_points = sorted(data_map[sup], key=lambda x: x[0])
        densities = [p[0] for p in sorted_points]
        probs = [p[1] for p in sorted_points]
        marker = 'o' if sup == 0.0 else 's' if sup == 0.2 else '^'
        errs = [np.sqrt(p * (1 - p) / 1000) for p in probs]
        plt.errorbar(densities, probs, yerr=errs, label=f'λ={sup}', marker=marker, linestyle='-', capsize=3)
    
    plt.xlabel('Density ($\\rho \\pi r_0^2$)')
    plt.ylabel('Percolation Probability')
    plt.xlim(0, 25)
    plt.ylim(0, 1.05)
    plt.legend()
    plt.tight_layout()
    plt.savefig(f'plots/fig_4_percolation_probability_hub_model.png', dpi=300)
    plt.close()

if __name__ == '__main__':
    plot_fig_4()
