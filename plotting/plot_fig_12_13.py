from plotting.utils import get_secondary_distribution, plot_single_distribution, plot_merged_distributions

def plot_fig_12_13():
    N = 637
    num_sim = 300
    
    print('Generating Figure 12 (Normal Model)...')
    k_norm, p_norm = get_secondary_distribution(0.0, N, 1, num_sim)
    plot_single_distribution(k_norm, p_norm, 'Fig. 12: Distribution of secondary infections\n(Normal model)', 'fig_12_normal', 'gray')
    
    print('\nGenerating Figure 13 (Strong & Hub Models)...')
    k_strong, p_strong = get_secondary_distribution(0.2, N, 1, num_sim)
    k_hub, p_hub = get_secondary_distribution(0.2, N, 2, num_sim)
    plot_merged_distributions(k_strong, p_strong, 'Strong infectiousness model', 'red', k_hub, p_hub, 'Hub model', 'blue', 'Fig. 13: Distribution of secondary infections\n(Superspreader models)', 'fig_13_superspreaders')

if __name__ == '__main__':
    plot_fig_12_13()
