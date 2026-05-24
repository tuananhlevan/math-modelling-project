import numpy as np
import matplotlib.pyplot as plt

def plot_epi_curve():
    data_hub = np.load("saved_run/results_sup0.2_pop600_mod2.npz")
    data_normal = np.load("saved_run/results_sup0.0_pop600_mod2.npz")
    data_strong = np.load("saved_run/results_sup0.2_pop600_mod1.npz")

    plt.plot(data_hub['epi_curve'], label="Hub Model (λ=0.2)", marker='s')
    plt.plot(data_normal['epi_curve'], label="(λ=0.0)", marker='^')
    plt.plot(data_strong['epi_curve'], label="Strong (λ=0.2)", marker='o')

    plt.title("Epidemic Curve")
    plt.xlabel("Time Step")
    plt.ylabel("Number of Newly Infected")
    plt.legend()
    plt.savefig("plots/epidemic_curve.png")
    
def plot_perc_prob():
    pass

if __name__ == "__main__":
    plot_epi_curve()
    # plot_perc_prob()