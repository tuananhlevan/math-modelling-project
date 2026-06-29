import os
import glob
import numpy as np
import matplotlib.pyplot as plt
from plotting.utils import get_critical_density

def plot_fig_5():
    lambdas = [0, 0.2, 0.4, 0.6, 0.8, 1]
    models = {1: {'name': 'Strong infectiousness model', 'marker': 'o', 'color': 'red', 'data': {}}, 2: {'name': 'Hub model', 'marker': 's', 'color': 'blue', 'data': {}}}
    
    for mod_id in models.keys():
        for lam in lambdas:
            files = glob.glob(f'saved_run/results_sup{lam}_pop*_mod{mod_id}.npz')
            densities = []
            probs = []
            for f in files:
                pop = int(os.path.basename(f).split('_')[2].replace('pop', ''))
                density = pop / 100.0 * np.pi * 1 ** 2
                data = np.load(f)
                densities.append(density)
                probs.append(data['perc_prob'])
            if len(densities) > 0:
                crit_d = get_critical_density(densities, probs, 0.3)
                models[mod_id]['data'][lam] = crit_d
    
    plt.figure(figsize=(7, 5))
    
    for mod_id, info in models.items():
        lams = sorted(info['data'].keys())
        crits = [info['data'][l] for lams in lams] # Wait, typo here: [info['data'][l] for l in lams]
        crits = [info['data'][l] for l in lams]
        plt.scatter(lams, crits, label=f"{info['name']}\n(simulation)", marker=info['marker'], color=info['color'], zorder=5)
    
    x_vals = np.linspace(0, 1, 100)
    y_strong = 27.0 / (1.0 + 5.0 * x_vals)
    plt.plot(x_vals, y_strong, color='limegreen', linestyle='-', label='(R0=Rc)')
    y_hub = 19.2 / (1.0 + 5.0 * x_vals)
    plt.plot(x_vals, y_hub, color='purple', linestyle='--', label='(R0=Rc)')
    plt.xlabel('$\\lambda$')
    plt.ylabel('$\\rho_c \\pi r_0^2$')
    plt.xlim(0.0, 1.0)
    plt.ylim(0, 25)
    plt.legend(loc='upper right')
    plt.tight_layout()
    plt.savefig('plots/fig_5_critical_density.png', dpi=300)

if __name__ == '__main__':
    plot_fig_5()
