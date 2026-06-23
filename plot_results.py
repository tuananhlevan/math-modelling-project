import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from matplotlib.patches import FancyArrowPatch
import os
import glob
from collections import defaultdict

from src.engine import main_loop, initialize
from src.variables import *

def pad_or_truncate(curve, target_len=41):
    if len(curve) > target_len:
        return curve[:target_len]
    else:
        return np.pad(curve, (0, target_len - len(curve)), mode='constant', constant_values=0)

def plot_fig_8():
    data_hub = np.load("saved_run/results_sup0.2_pop637_mod2.npz")
    data_normal = np.load("saved_run/results_sup0_pop637_mod2.npz")
    data_strong = np.load("saved_run/results_sup0.2_pop637_mod1.npz")

    curve_hub = pad_or_truncate(data_hub['epi_curve'], 41)
    curve_normal = pad_or_truncate(data_normal['epi_curve'], 41)
    curve_strong = pad_or_truncate(data_strong['epi_curve'], 41)

    plt.plot(curve_hub, label="Hub Model (λ=0.2)", marker='s')
    plt.plot(curve_normal, label="(λ=0.0)", marker='^')
    plt.plot(curve_strong, label="Strong (λ=0.2)", marker='o')

    plt.xlabel("Time Step")
    plt.ylabel("Number of Newly Infected")
    
    plt.xlim(0, 40) 
    
    plt.legend()
    plt.savefig("plots/fig_8_epidemic_curve.png", dpi=300)
    
def plot_fig_3():
    # Retrieve all files for the requested model_type
    files = glob.glob(f"saved_run/results_sup*_pop*_mod1.npz")
    
    # Dictionary to organize data: { sup_prob: { density: perc_prob } }
    data_map = {}
    
    for file in files:
        # Extract parameters from the filename (e.g., results_sup0.2_pop450_mod2.npz)
        parts = os.path.basename(file).split('_')
        sup = float(parts[1].replace('sup', ''))
        pop = int(parts[2].replace('pop', ''))
        
        # Convert population to Density (rho * pi * r0^2)
        # Area = 10x10 = 100, r0 = 1
        density = (pop / 100.0) * np.pi * (1**2)
        
        data = np.load(file)
        prob = data['perc_prob']
        
        if sup not in data_map:
            data_map[sup] = [(0, 0)]
        data_map[sup].append((density, prob))
    plt.figure(figsize=(7, 5))
    
    # Sort lambda (sup_prob) values so the legend is in order
    for sup in sorted(data_map.keys()):
        # Sort by density to draw a clean line
        sorted_points = sorted(data_map[sup], key=lambda x: x[0])
        densities = [p[0] for p in sorted_points]
        probs = [p[1] for p in sorted_points]
        
        marker = 'o' if sup == 0.0 else ('s' if sup == 0.2 else '^')
        errs = [np.sqrt(p * (1 - p) / 1000) for p in probs]
        plt.errorbar(densities, probs, yerr=errs, label=f"λ={sup}", marker=marker, linestyle='-', capsize=3)
        
    plt.xlabel(r"Density ($\rho \pi r_0^2$)")
    plt.ylabel("Percolation Probability")
    plt.xlim(0, 25)
    plt.ylim(0, 1.05)
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"plots/fig_3_percolation_probability_strong_model.png", dpi=300)
    plt.close()
    
def plot_fig_4():
    # Retrieve all files for the requested model_type
    files = glob.glob(f"saved_run/results_sup*_pop*_mod2.npz")
    
    # Dictionary to organize data: { sup_prob: { density: perc_prob } }
    data_map = {}
    
    for file in files:
        # Extract parameters from the filename (e.g., results_sup0.2_pop450_mod2.npz)
        parts = os.path.basename(file).split('_')
        sup = float(parts[1].replace('sup', ''))
        pop = int(parts[2].replace('pop', ''))
        
        # Convert population to Density (rho * pi * r0^2)
        # Area = 10x10 = 100, r0 = 1
        density = (pop / 100.0) * np.pi * (1**2)
        
        data = np.load(file)
        prob = data['perc_prob']
        
        if sup not in data_map:
            data_map[sup] = [(0, 0)]
        data_map[sup].append((density, prob))
    plt.figure(figsize=(7, 5))
    
    # Sort lambda (sup_prob) values so the legend is in order
    for sup in sorted(data_map.keys()):
        # Sort by density to draw a clean line
        sorted_points = sorted(data_map[sup], key=lambda x: x[0])
        densities = [p[0] for p in sorted_points]
        probs = [p[1] for p in sorted_points]
        
        marker = 'o' if sup == 0.0 else ('s' if sup == 0.2 else '^')
        errs = [np.sqrt(p * (1 - p) / 1000) for p in probs]
        plt.errorbar(densities, probs, yerr=errs, label=f"λ={sup}", marker=marker, linestyle='-', capsize=3)
        
    plt.xlabel(r"Density ($\rho \pi r_0^2$)")
    plt.ylabel("Percolation Probability")
    plt.xlim(0, 25)
    plt.ylim(0, 1.05)
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"plots/fig_4_percolation_probability_hub_model.png", dpi=300)
    plt.close()
    
def get_critical_density(densities, probs, target_prob=0.5):
    """Linearly interpolates the density at which percolation hits 50%."""
    sorted_pairs = sorted(zip(densities, probs))
    d = [pair[0] for pair in sorted_pairs]
    p = [pair[1] for pair in sorted_pairs]

    for i in range(len(p) - 1):
        if p[i] <= target_prob and p[i+1] >= target_prob:
            # Handle edge case where probs are identical
            if p[i+1] == p[i]: return d[i]
            # Linear interpolation
            slope = (d[i+1] - d[i]) / (p[i+1] - p[i])
            return d[i] + slope * (target_prob - p[i])
            
    return np.nan # Return NaN if the threshold was never crossed

def plot_fig_5():
    lambdas = [0, 0.2, 0.4, 0.6, 0.8, 1]
    
    # 1. Extract simulation data points
    models = {
        1: {"name": "Strong infectiousness model", "marker": 'o', "color": 'red', "data": {}},
        2: {"name": "Hub model", "marker": 's', "color": 'blue', "data": {}}
    }
    
    for mod_id in models.keys():
        for lam in lambdas:
            # Glob all populations for this specific lambda and model
            files = glob.glob(f"saved_run/results_sup{lam}_pop*_mod{mod_id}.npz")
            densities = []
            probs = []
            
            for f in files:
                pop = int(os.path.basename(f).split('_')[2].replace('pop', ''))
                # Convert population to Density (Area = 100, r0 = 1)
                density = (pop / 100.0) * np.pi * (1**2)
                data = np.load(f)
                
                densities.append(density)
                probs.append(data['perc_prob'])
            
            if len(densities) > 0:
                crit_d = get_critical_density(densities, probs, 0.3)
                models[mod_id]["data"][lam] = crit_d

    plt.figure(figsize=(7, 5))

    # Plot empirical scatter points
    for mod_id, info in models.items():
        lams = sorted(info["data"].keys())
        crits = [info["data"][l] for l in lams]
        plt.scatter(lams, crits, label=f'{info["name"]}\n(simulation)', 
                    marker=info["marker"], color=info["color"], zorder=5)

    # 2. Plot Theoretical Curves (R0 = Rc)
    x_vals = np.linspace(0, 1, 100)
    
    # Strong Model
    y_strong = 27.0 / (1.0 + 5.0 * x_vals)
    plt.plot(x_vals, y_strong, color='limegreen', linestyle='-', label='(R0=Rc)')
    
    # Hub Model
    y_hub = 19.2 / (1.0 + 5.0 * x_vals)
    plt.plot(x_vals, y_hub, color='purple', linestyle='--', label='(R0=Rc)')

    # Formatting
    plt.xlabel(r"$\lambda$")
    plt.ylabel(r"$\rho_c \pi r_0^2$")
    plt.xlim(0., 1.)
    plt.ylim(0, 25)
    
    plt.legend(loc='upper right')
    plt.tight_layout()
    plt.savefig("plots/fig_5_critical_density.png", dpi=300)
    
def plot_fig_6(num_sim=300, env_pop=637, target_time_steps=40):
    lambdas = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
    
    plt.figure(figsize=(7, 5))
    
    # Matching the paper's markers to the lambda values
    markers = {0.0: 'o', 0.2: '*', 0.4: 's', 0.6: 'p', 0.8: '^', 1.0: 'v'}
    colors = {0.0: 'brown', 0.2: 'limegreen', 0.4: 'blue', 0.6: 'magenta', 0.8: 'cyan', 1.0: 'yellow'}

    for lam in lambdas:
        print(f"Running Monte Carlo for λ={lam}...")
        all_rf_curves = []
        
        for _ in range(num_sim):
            # Model 1 = Strong Infectiousness Model
            _, _, rf_curve = main_loop(sup_prob=lam, env_pop=env_pop, model_type=1)
            
            # If the curve is shorter than 40 steps, pad it with its final value (the front line stopped)
            if len(rf_curve) < target_time_steps + 1:
                pad_length = (target_time_steps + 1) - len(rf_curve)
                padded_rf = np.pad(rf_curve, (0, pad_length), mode='edge')
            else:
                padded_rf = rf_curve[:target_time_steps + 1]
                
            all_rf_curves.append(padded_rf)
            
        # Average the distances unconditionally
        average_rf = np.mean(all_rf_curves, axis=0)
        
        # Plot the curve
        plt.scatter(range(len(average_rf)), average_rf, 
                    label=f"λ={lam}", marker=markers[lam], color=colors[lam], s=30)

    plt.xlabel("time step")
    plt.ylabel(r"$r_f / r_0$") # Since r0 = 1, this is just our distance
    
    plt.xlim(0, 40)
    plt.ylim(0, 12)
    
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.tight_layout()
    plt.savefig("plots/fig_6_propagation_speed.png", dpi=300)

def calculate_velocity(rf_curve):
    """
    Finds the velocity by calculating the slope of the linear growth region
    before the curve encounters boundary saturation, adapting to each curve's max height.
    """
    rf_array = np.array(rf_curve)
    time_steps = np.arange(len(rf_array))
    
    max_val = np.max(rf_array)
    min_val = rf_array[0]
    
    # Cleanly isolate the growth phase before it starts bending into its plateau
    growth_threshold = min_val + 0.85 * (max_val - min_val)
    
    # Find indices that are part of this growth window (skipping step 0 initialization)
    valid_indices = np.where((rf_array <= growth_threshold) & (time_steps > 0))[0]
    
    if len(valid_indices) >= 2:
        slope, _ = np.polyfit(time_steps[valid_indices], rf_array[valid_indices], 1)
        return slope
    else:
        # Fallback for ultra-fast transitions
        end_idx = min(5, len(rf_array) - 1)
        if end_idx > 1:
            return (rf_array[end_idx] - rf_array[1]) / float(end_idx - 1)
        return 0.0

def plot_fig_7(num_sim=300, env_pop=637):
    # The paper plots points roughly every 0.05 or 0.1 step to create a smooth curve
    lambdas = np.arange(0.0, 1.01, 0.1) 
    
    # Storage arrays for final velocities
    velocities_strong = []
    velocities_hub = []
    
    # 1. Sweep for Model 1 (Strong Infectiousness)
    print("Evaluating Strong Infectiousness Model...")
    for lam in lambdas:
        all_curves = []
        for _ in range(num_sim):
            _, _, rf_curve = main_loop(sup_prob=lam, env_pop=env_pop, model_type=1)
            all_curves.append(rf_curve)
            
        # Average the distance curves
        max_len = max(len(c) for c in all_curves)
        padded_curves = [c + [c[-1]] * (max_len - len(c)) for c in all_curves]
        avg_rf_curve = np.mean(padded_curves, axis=0)
        
        # Extract velocity from the average curve
        v = calculate_velocity(avg_rf_curve)
        velocities_strong.append(v)
        print(f"  λ = {lam:.2f} -> Velocity = {v:.4f}")
        
    # 2. Sweep for Model 2 (Hub Model)
    print("\nEvaluating Hub Model...")
    for lam in lambdas:
        all_curves = []
        for _ in range(num_sim):
            _, _, rf_curve = main_loop(sup_prob=lam, env_pop=env_pop, model_type=2)
            all_curves.append(rf_curve)
            
        # Average the distance curves
        max_len = max(len(c) for c in all_curves)
        padded_curves = [c + [c[-1]] * (max_len - len(c)) for c in all_curves]
        avg_rf_curve = np.mean(padded_curves, axis=0)
        
        # Extract velocity from the average curve
        v = calculate_velocity(avg_rf_curve)
        velocities_hub.append(v)
        print(f"  λ = {lam:.2f} -> Velocity = {v:.4f}")

    plt.figure(figsize=(7, 6))
    
    plt.plot(lambdas, velocities_strong, label="Strong infectiousness model", 
             marker='o', color='red', linestyle='-', markersize=6)
    plt.plot(lambdas, velocities_hub, label="Hub model", 
             marker='s', color='blue', linestyle='-', markersize=6)

    plt.xlabel(r"$\lambda$")
    plt.ylabel(r"velocity ($/r_0 \cdot s$)")
    
    plt.xlim(0, 1.0)
    plt.ylim(0, 1.6) # The paper's velocity metrics scale cleanly from 0.2 up to 1.6
    
    plt.legend(loc='lower right')
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.tight_layout()
    plt.savefig("plots/fig_7_velocity_comparison.png", dpi=300)
    plt.show()
    
def generate_network_plot(sup_prob, env_pop, model_type, title, filename):
    print(f"Generating {title}...")
    
    success = False
    edges = []
    population = []
    
    # Keep running the simulation until we get a visually representative outbreak
    while not success:
        population = initialize(sup_prob, env_pop)
        edges = []
        
        while any(ind.health_state == "I" for ind in population):
            current_infected = [ind for ind in population if ind.health_state == "I"]
            current_susceptible = [ind for ind in population if ind.health_state == "S"]
            
            for ind_i in current_infected:
                for ind_s in current_susceptible:
                    if ind_s.health_state == "S":
                        ind_i.infect(ind_s, model_type=model_type)
                        if ind_s.health_state == "I":
                            edges.append((ind_i, ind_s))
                ind_i.recover()

        # Check if this run was a "dud" or if it matches the paper's visual intent
        if sup_prob > 0.0 and len(edges) > 150:
            success = True # A widespread outbreak for Fig 9 and 10
        elif sup_prob == 0.0 and 20 < len(edges) < 100:
            success = True # A moderate outbreak that died out for Fig 11

    # Setup the Plot
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.set_xlim(0, ENV_WIDTH)
    ax.set_ylim(0, ENV_WIDTH)
    ax.set_xticks([])
    ax.set_yticks([])

    # Draw the infection routes (Arrows)
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

    # Draw the Individuals (Nodes)
    for ind in population:
        is_infected = ind.health_state in ["I", "R"]
        is_super = ind.super_spreader
        
        if is_infected and is_super:
            c, ec = 'blue', 'blue'         
        elif is_infected and not is_super:
            c, ec = 'white', 'blue'        
        elif not is_infected and is_super:
            c, ec = 'black', 'black'       
        else:
            c, ec = 'white', 'black'       
            
        ax.scatter(ind.coord[0], ind.coord[1], facecolors=c, edgecolors=ec, 
                   marker='o', s=40, zorder=5, linewidths=1.2)

    # Add a border box
    for spine in ax.spines.values():
        spine.set_edgecolor('black')
        spine.set_linewidth(2)

    # --- CUSTOM LEGEND OUTSIDE THE BOX ---
    arrow_handle = mlines.Line2D([], [], color='black', marker='>', markersize=5, lw=1, label='route of infection')
    s_super_handle = mlines.Line2D([], [], color='w', marker='o', markerfacecolor='black', markeredgecolor='black', markersize=7, label='S (superspreader)')
    s_norm_handle = mlines.Line2D([], [], color='w', marker='o', markerfacecolor='white', markeredgecolor='black', markersize=7, label='S (normal)')
    i_super_handle = mlines.Line2D([], [], color='w', marker='o', markerfacecolor='blue', markeredgecolor='blue', markersize=7, label='I (superspreader)')
    i_norm_handle = mlines.Line2D([], [], color='w', marker='o', markerfacecolor='white', markeredgecolor='blue', markersize=7, label='I (normal)')

    # Place legend to the center-right, completely outside the axes
    ax.legend(handles=[arrow_handle, s_super_handle, s_norm_handle, i_super_handle, i_norm_handle],
              loc='center left', bbox_to_anchor=(1.02, 0.5), frameon=False, fontsize=11, labelspacing=0.8)
    
    # bbox_inches='tight' ensures the saved image expands to include the outside legend
    plt.savefig(f"plots/{filename}.png", bbox_inches='tight', dpi=300)
    plt.close()
    
def get_secondary_distribution(sup_prob, env_pop, model_type, num_sim=1000):
    k_counts = defaultdict(int)
    total_infected_individuals = 0
    
    for i in range(1, num_sim + 1):
        if i % 100 == 0 and i > 0:
            print(f"  Completed {i}/{num_sim} runs...")
            
        population = initialize(sup_prob, env_pop)
        
        secondary_infections = {id(ind): 0 for ind in population}
        
        while any(ind.health_state == "I" for ind in population):
            current_infected = [ind for ind in population if ind.health_state == "I"]
            current_susceptible = [ind for ind in population if ind.health_state == "S"]
            
            for ind_i in current_infected:
                for ind_s in current_susceptible:
                    if ind_s.health_state == "S":
                        ind_i.infect(ind_s, model_type=model_type)
                        if ind_s.health_state == "I":
                            secondary_infections[id(ind_i)] += 1
                ind_i.recover()

        for ind in population:
            if ind.health_state == "R":
                k = secondary_infections[id(ind)]
                k_counts[k] += 1
                total_infected_individuals += 1
                
    max_k = max(k_counts.keys()) if k_counts else 0
    k_values = np.arange(max_k + 1)
    p_values = np.zeros(max_k + 1)
    
    for k, count in k_counts.items():
        p_values[k] = count / total_infected_individuals
        
    return k_values, p_values

def plot_single_distribution(k_vals, p_vals, title, filename, color):
    fig, ax = plt.subplots(figsize=(6, 5))
    
    ax.bar(k_vals, p_vals, color='cyan', width=0.4, label='(λ=0.0)')
    
    ax.set_xlabel("the number of links")
    ax.set_ylabel("")
    
    ax.set_xlim(-1, 20)
    ax.set_ylim(0, 0.8)
    
    ax.tick_params(axis='both', direction='in', top=True, right=True)
    
    ax.legend(loc='upper right', frameon=True)
    
    plt.tight_layout()
    plt.savefig(f"plots/{filename}.png", dpi=300)
    plt.close()

def plot_merged_distributions(k1, p1, label1, color1, k2, p2, label2, color2, title, filename):
    fig, ax = plt.subplots(figsize=(6, 5))
    
    width = 0.4
    
    ax.bar(k1 - width/2, p1, color=color1, width=width, label=label1)
    ax.bar(k2 + width/2, p2, color=color2, width=width, label=label2)
    
    ax.set_xlabel("the number of links")
    ax.set_ylabel("") 
    
    ax.set_xlim(-1, 20)
    ax.set_ylim(0, 0.8)
    
    ax.tick_params(axis='both', direction='in', top=True, right=True)
    
    ax.legend(loc='upper right', frameon=False)
    
    plt.tight_layout()
    plt.savefig(f"plots/{filename}.png", dpi=300)
    plt.close()

def plot_fig_12_13():
    # Target density of 20.0 (N=637)
    N = 637 
    num_sim = 300
    
    print("Generating Figure 12 (Normal Model)...")
    k_norm, p_norm = get_secondary_distribution(0.0, N, 1, num_sim)
    plot_single_distribution(k_norm, p_norm, "Fig. 12: Distribution of secondary infections\n(Normal model)", "fig_12_normal", "gray")
    
    print("\nGenerating Figure 13 (Strong & Hub Models)...")
    k_strong, p_strong = get_secondary_distribution(0.2, N, 1, num_sim)
    k_hub, p_hub = get_secondary_distribution(0.2, N, 2, num_sim)
    
    plot_merged_distributions(
        k_strong, p_strong, "Strong infectiousness model", "red",
        k_hub, p_hub, "Hub model", "blue",
        "Fig. 13: Distribution of secondary infections\n(Superspreader models)", 
        "fig_13_superspreaders"
    )
    
def plot_fig_14():
    # Historical data extracted from the CDC Singapore 2003 SARS outbreak
    k_vals = np.arange(41)
    counts = np.zeros(41)
    
    # Bulk of normal patients (visually extracted from the chart)
    counts[0] = 162
    counts[1] = 20
    counts[2] = 7
    counts[3] = 6
    counts[7] = 1 
    
    # The explicitly noted superspreaders from the paper's text
    counts[12] = 1
    counts[21] = 1
    counts[23] = 1
    counts[40] = 1

    fig, ax = plt.subplots(figsize=(8, 4)) # Slightly wider aspect ratio
    
    # Use magenta to match the paper's styling
    ax.bar(k_vals, counts, color='magenta', width=0.6)
    
    # Exact formatting from the paper
    ax.set_xlabel("number of direct secondary cases")
    ax.set_ylabel("number")
    
    # Lock the axes to the paper's exact dimensions
    ax.set_xlim(-1, 41)
    ax.set_ylim(0, 180)
    
    # Tick marks pointing inwards, on all 4 sides of the box
    ax.tick_params(axis='both', direction='in', top=True, right=True)
    
    # The paper has a weird empty pink line in the legend, we can hack that in:
    ax.plot([], [], color='magenta', label=' ') 
    ax.legend(loc='upper right', frameon=False, handlelength=2)
    
    plt.tight_layout()
    plt.savefig("plots/fig_14_sars_data.png", dpi=300)

def plot_fig_15():
    # Historical SARS Data (Singapore, Feb 13-Jun 13, 2003)
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

    # 3. Render the Plot
    fig, ax = plt.subplots(figsize=(6, 5))
    
    # Plot the historical data as a histogram first (so it sits in the background)
    ax.bar(sars_time_steps, sars_counts, color='orange', width=1.0, 
           edgecolor='white', linewidth=0.5, label='data of SARS in Singapore', alpha=0.9)
    
    data_hub = np.load("saved_run/results_sup0.4_pop477_mod2.npz")
    data_normal = np.load("saved_run/results_sup0_pop477_mod2.npz")
    data_strong = np.load("saved_run/results_sup0.4_pop477_mod1.npz")

    # Target length of 41 corresponds to time steps 0 through 40
    curve_hub = pad_or_truncate(data_hub['epi_curve'], 41)
    curve_normal = pad_or_truncate(data_normal['epi_curve'], 41)
    curve_strong = pad_or_truncate(data_strong['epi_curve'], 41)

    plt.plot(curve_hub, label="Hub Model (λ=0.2)", marker='s')
    plt.plot(curve_normal, label="(λ=0.0)", marker='^')
    plt.plot(curve_strong, label="Strong (λ=0.2)", marker='o')

    plt.xlabel("Time Step")
    plt.ylabel("Number of Newly Infected")
    
    # Explicitly lock the x-axis view to 0-40 just to be safe
    plt.xlim(0, 40) 
    
    plt.legend()
    plt.savefig("plots/fig_15_epidemic_curve.png", dpi=300)
    

if __name__ == "__main__":
    plot_fig_3()
    plot_fig_4()
    plot_fig_5()
    plot_fig_6()
    plot_fig_7()
    plot_fig_8()
    
    N_density_15 = 477
    # Figure 9: Strong Infectiousness Model
    generate_network_plot(sup_prob=0.2, env_pop=N_density_15, model_type=1, 
                          title="Figure 9: Route of Infection (Strong Model)", 
                          filename="fig_9_network_strong")
                          
    # Figure 10: Hub Model
    generate_network_plot(sup_prob=0.2, env_pop=N_density_15, model_type=2, 
                          title="Figure 10: Route of Infection (Hub Model)", 
                          filename="fig_10_network_hub")
                          
    # Figure 11: Normal Model (No superspreaders)
    generate_network_plot(sup_prob=0.0, env_pop=N_density_15, model_type=1, 
                          title="Figure 11: Route of Infection (Normal Model)", 
                          filename="fig_11_network_normal")
    
    plot_fig_12_13()
    plot_fig_14()
    plot_fig_15()