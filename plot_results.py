import numpy as np
import matplotlib.pyplot as plt
import os
import glob

def pad_or_truncate(curve, target_len=41):
    if len(curve) > target_len:
        return curve[:target_len]
    else:
        return np.pad(curve, (0, target_len - len(curve)), mode='constant', constant_values=0)

def plot_epi_curve():
    data_hub = np.load("saved_run/results_sup0.2_pop636_mod2.npz")
    data_normal = np.load("saved_run/results_sup0.0_pop636_mod2.npz")
    data_strong = np.load("saved_run/results_sup0.2_pop636_mod1.npz")

    # Target length of 41 corresponds to time steps 0 through 40
    curve_hub = pad_or_truncate(data_hub['epi_curve'], 41)
    curve_normal = pad_or_truncate(data_normal['epi_curve'], 41)
    curve_strong = pad_or_truncate(data_strong['epi_curve'], 41)

    plt.plot(curve_hub, label="Hub Model (λ=0.2)", marker='s')
    plt.plot(curve_normal, label="(λ=0.0)", marker='^')
    plt.plot(curve_strong, label="Strong (λ=0.2)", marker='o')

    plt.title("Epidemic Curve")
    plt.xlabel("Time Step")
    plt.ylabel("Number of Newly Infected")
    
    # Explicitly lock the x-axis view to 0-40 just to be safe
    plt.xlim(0, 40) 
    
    plt.legend()
    plt.savefig("plots/epidemic_curve.png")
    
def plot_perc_prob(model_type, filename):
    # Retrieve all files for the requested model_type
    files = glob.glob(f"saved_run/results_sup*_pop*_mod{model_type}.npz")
    
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
            data_map[sup] = []
        data_map[sup].append((density, prob))
    plt.figure(figsize=(7, 5))
    
    # Sort lambda (sup_prob) values so the legend is in order
    for sup in sorted(data_map.keys()):
        # Sort by density to draw a clean line
        sorted_points = sorted(data_map[sup], key=lambda x: x[0])
        densities = [p[0] for p in sorted_points]
        probs = [p[1] for p in sorted_points]
        
        # Use different markers for different lambda values
        marker = 'o' if sup == 0.0 else ('s' if sup == 0.2 else '^')
        plt.plot(densities, probs, label=f"λ={sup}", marker=marker, linestyle='-')
        
    plt.xlabel(r"Density ($\rho \pi r_0^2$)")
    plt.ylabel("Percolation Probability")
    plt.xlim(0, 25)
    plt.ylim(0, 1.05)
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"plots/{filename}.png")
    plt.close()

if __name__ == "__main__":
    # plot_epi_curve()
    plot_perc_prob(1, "percolation_probability_strong_model")