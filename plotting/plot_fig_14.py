import numpy as np
import matplotlib.pyplot as plt

def plot_fig_14():
    k_vals = np.arange(41)
    counts = np.zeros(41)
    counts[0] = 162
    counts[1] = 20
    counts[2] = 7
    counts[3] = 6
    counts[7] = 1
    counts[12] = 1
    counts[21] = 1
    counts[23] = 1
    counts[40] = 1
    
    fig, ax = plt.subplots(figsize=(8, 4))
    
    ax.bar(k_vals, counts, color='magenta', width=0.6)
    
    ax.set_xlabel('number of direct secondary cases')
    ax.set_ylabel('number')
    ax.set_xlim(-1, 41)
    ax.set_ylim(0, 180)
    ax.tick_params(axis='both', direction='in', top=True, right=True)
    ax.plot([], [], color='magenta', label=' ')
    ax.legend(loc='upper right', frameon=False, handlelength=2)
    plt.tight_layout()
    plt.savefig('plots/fig_14_sars_data.png', dpi=300)

if __name__ == '__main__':
    plot_fig_14()
