import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from matplotlib.patches import FancyArrowPatch
from collections import defaultdict
from src.engine import main_loop, initialize
from src.variables import *

def pad_or_truncate(curve, target_len=41):
    if len(curve) > target_len:
        return curve[:target_len]
    else:
        return np.pad(curve, (0, target_len - len(curve)), mode='constant', constant_values=0)

def get_critical_density(densities, probs, target_prob=0.5):
    sorted_pairs = sorted(zip(densities, probs))
    d = [pair[0] for pair in sorted_pairs]
    p = [pair[1] for pair in sorted_pairs]
    for i in range(len(p) - 1):
        if p[i] <= target_prob and p[i + 1] >= target_prob:
            if p[i + 1] == p[i]:
                return d[i]
            slope = (d[i + 1] - d[i]) / (p[i + 1] - p[i])
            return d[i] + slope * (target_prob - p[i])
    return np.nan

def calculate_velocity(rf_curve):
    rf_array = np.array(rf_curve)
    time_steps = np.arange(len(rf_array))
    max_val = np.max(rf_array)
    min_val = rf_array[0]
    growth_threshold = min_val + 0.85 * (max_val - min_val)
    valid_indices = np.where((rf_array <= growth_threshold) & (time_steps > 0))[0]
    if len(valid_indices) >= 2:
        slope, _ = np.polyfit(time_steps[valid_indices], rf_array[valid_indices], 1)
        return slope
    else:
        end_idx = min(5, len(rf_array) - 1)
        if end_idx > 1:
            return (rf_array[end_idx] - rf_array[1]) / float(end_idx - 1)
        return 0.0

def generate_network_plot(sup_prob, env_pop, model_type, title, filename):
    print(f'Generating {title}...')
    success = False
    edges = []
    population = []
    while not success:
        population = initialize(sup_prob, env_pop)
        edges = []
        while any((ind.health_state == 'I' for ind in population)):
            current_infected = [ind for ind in population if ind.health_state == 'I']
            current_susceptible = [ind for ind in population if ind.health_state == 'S']
            for ind_i in current_infected:
                for ind_s in current_susceptible:
                    if ind_s.health_state == 'S':
                        ind_i.infect(ind_s, model_type=model_type)
                        if ind_s.health_state == 'I':
                            edges.append((ind_i, ind_s))
                ind_i.recover()
        if sup_prob > 0.0 and len(edges) > 150:
            success = True
        elif sup_prob == 0.0 and 20 < len(edges) < 100:
            success = True
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.set_xlim(0, ENV_WIDTH)
    ax.set_ylim(0, ENV_WIDTH)
    ax.set_xticks([])
    ax.set_yticks([])
    for ind_i, ind_s in edges:
        x1, y1 = ind_i.coord
        x2, y2 = ind_s.coord
        dx = x2 - x1
        if abs(dx) > ENV_WIDTH / 2:
            x2_phantom = x2 - ENV_WIDTH if x2 > x1 else x2 + ENV_WIDTH
            x1_phantom = x1 + ENV_WIDTH if x1 < x2 else x1 - ENV_WIDTH
            arrow1 = FancyArrowPatch((x1, y1), (x2_phantom, y2), arrowstyle='-|>', color='black', lw=0.6, mutation_scale=10)
            arrow2 = FancyArrowPatch((x1_phantom, y1), (x2, y2), arrowstyle='-|>', color='black', lw=0.6, mutation_scale=10)
            ax.add_patch(arrow1)
            ax.add_patch(arrow2)
        else:
            arrow = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle='-|>', color='black', lw=0.6, mutation_scale=10)
            ax.add_patch(arrow)
    for ind in population:
        is_infected = ind.health_state in ['I', 'R']
        is_super = ind.super_spreader
        if is_infected and is_super:
            c, ec = ('blue', 'blue')
        elif is_infected and (not is_super):
            c, ec = ('white', 'blue')
        elif not is_infected and is_super:
            c, ec = ('black', 'black')
        else:
            c, ec = ('white', 'black')
        ax.scatter(ind.coord[0], ind.coord[1], facecolors=c, edgecolors=ec, marker='o', s=40, zorder=5, linewidths=1.2)
    for spine in ax.spines.values():
        spine.set_edgecolor('black')
        spine.set_linewidth(2)
    arrow_handle = mlines.Line2D([], [], color='black', marker='>', markersize=5, lw=1, label='route of infection')
    s_super_handle = mlines.Line2D([], [], color='w', marker='o', markerfacecolor='black', markeredgecolor='black', markersize=7, label='S (superspreader)')
    s_norm_handle = mlines.Line2D([], [], color='w', marker='o', markerfacecolor='white', markeredgecolor='black', markersize=7, label='S (normal)')
    i_super_handle = mlines.Line2D([], [], color='w', marker='o', markerfacecolor='blue', markeredgecolor='blue', markersize=7, label='I (superspreader)')
    i_norm_handle = mlines.Line2D([], [], color='w', marker='o', markerfacecolor='white', markeredgecolor='blue', markersize=7, label='I (normal)')
    ax.legend(handles=[arrow_handle, s_super_handle, s_norm_handle, i_super_handle, i_norm_handle], loc='center left', bbox_to_anchor=(1.02, 0.5), frameon=False, fontsize=11, labelspacing=0.8)
    plt.savefig(f'plots/{filename}.png', bbox_inches='tight', dpi=300)
    plt.close()

def get_secondary_distribution(sup_prob, env_pop, model_type, num_sim=1000):
    k_counts = defaultdict(int)
    total_infected_individuals = 0
    for i in range(1, num_sim + 1):
        if i % 100 == 0 and i > 0:
            print(f'  Completed {i}/{num_sim} runs...')
        population = initialize(sup_prob, env_pop)
        secondary_infections = {id(ind): 0 for ind in population}
        while any((ind.health_state == 'I' for ind in population)):
            current_infected = [ind for ind in population if ind.health_state == 'I']
            current_susceptible = [ind for ind in population if ind.health_state == 'S']
            for ind_i in current_infected:
                for ind_s in current_susceptible:
                    if ind_s.health_state == 'S':
                        ind_i.infect(ind_s, model_type=model_type)
                        if ind_s.health_state == 'I':
                            secondary_infections[id(ind_i)] += 1
                ind_i.recover()
        for ind in population:
            if ind.health_state == 'R':
                k = secondary_infections[id(ind)]
                k_counts[k] += 1
                total_infected_individuals += 1
    max_k = max(k_counts.keys()) if k_counts else 0
    k_values = np.arange(max_k + 1)
    p_values = np.zeros(max_k + 1)
    for k, count in k_counts.items():
        p_values[k] = count / total_infected_individuals
    return (k_values, p_values)

def plot_single_distribution(k_vals, p_vals, title, filename, color):
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.bar(k_vals, p_vals, color='cyan', width=0.4, label='(λ=0.0)')
    ax.set_xlabel('the number of links')
    ax.set_ylabel('')
    ax.set_xlim(-1, 20)
    ax.set_ylim(0, 0.8)
    ax.tick_params(axis='both', direction='in', top=True, right=True)
    ax.legend(loc='upper right', frameon=True)
    plt.tight_layout()
    plt.savefig(f'plots/{filename}.png', dpi=300)
    plt.close()

def plot_merged_distributions(k1, p1, label1, color1, k2, p2, label2, color2, title, filename):
    fig, ax = plt.subplots(figsize=(6, 5))
    width = 0.4
    ax.bar(k1 - width / 2, p1, color=color1, width=width, label=label1)
    ax.bar(k2 + width / 2, p2, color=color2, width=width, label=label2)
    ax.set_xlabel('the number of links')
    ax.set_ylabel('')
    ax.set_xlim(-1, 20)
    ax.set_ylim(0, 0.8)
    ax.tick_params(axis='both', direction='in', top=True, right=True)
    ax.legend(loc='upper right', frameon=False)
    plt.tight_layout()
    plt.savefig(f'plots/{filename}.png', dpi=300)
    plt.close()
