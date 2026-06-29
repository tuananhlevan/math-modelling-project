from plotting.utils import generate_network_plot

def plot_fig_9_10_11():
    N_density_15 = 477
    generate_network_plot(sup_prob=0.2, env_pop=N_density_15, model_type=1, title='Figure 9: Route of Infection (Strong Model)', filename='fig_9_network_strong')
    generate_network_plot(sup_prob=0.2, env_pop=N_density_15, model_type=2, title='Figure 10: Route of Infection (Hub Model)', filename='fig_10_network_hub')
    generate_network_plot(sup_prob=0.0, env_pop=N_density_15, model_type=1, title='Figure 11: Route of Infection (Normal Model)', filename='fig_11_network_normal')

if __name__ == '__main__':
    plot_fig_9_10_11()
