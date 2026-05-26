import numpy as np
import matplotlib.pyplot as plt

def pad_or_truncate(curve, target_len=41):
    """
    Cuts the array if it's longer than target_len, 
    or zero-pads it if it's shorter.
    """
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
    
def plot_perc_prob():
    pass

if __name__ == "__main__":
    plot_epi_curve()
    # plot_perc_prob()