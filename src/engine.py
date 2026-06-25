import numpy as np
import argparse
import logging

from src.individual import Individual
from src.variables import *

def initialize(super_spreader_prob, environment_population):
    population = []
    
    infected = Individual()
    infected.coord = [ENV_WIDTH / 2, 0]
    if np.random.uniform(0, 1) < super_spreader_prob:
        infected.super_spreader = True
    infected.health_state = "I"
    population.append(infected)
    
    for i in range(environment_population - 1):
        ind = Individual()
        if np.random.uniform(0, 1) < super_spreader_prob:
            ind.super_spreader = True
        population.append(ind)
    
    return population
    
            
def main_loop(sup_prob, env_pop, model_type):
    count_new_infected = [1] # size = number of time steps
    rf_curve = [0.0]
    
    population = initialize(sup_prob, env_pop) # size = ENV_POP
    patient_zero = population[0]
    
    percolates_threshold = ENV_WIDTH * (1 - 1 / np.sqrt(env_pop))
    percolates = False
    
    while any(ind.health_state == "I" for ind in population):
        current_infected = []
        current_susceptible = []
        current_new_infected = []
        
        for ind in population:
            if ind.health_state == "I":
                current_infected.append(ind)
            elif ind.health_state == "S":
                current_susceptible.append(ind)
        
        for ind_i in current_infected:
            for ind_s in current_susceptible:
                ind_i.infect(ind_s, model_type=model_type)
            
            ind_i.recover()
        
        for ind in current_susceptible:
            if ind.health_state == "I":
                current_new_infected.append(ind)
        count_new_infected.append(len(current_new_infected))
        
        max_dist = 0.0
        for ind in population:
            if ind.health_state in ["I", "R"]:
                # Shortest X distance (Wrapped cylinder)
                dx = abs(ind.coord[0] - patient_zero.coord[0])
                if dx > ENV_WIDTH / 2: 
                    dx = ENV_WIDTH - dx
                    
                # True Y distance (Unwrapped)
                dy = abs(ind.coord[1] - patient_zero.coord[1])
                
                dist = np.sqrt(dx**2 + dy**2)
                if dist > max_dist:
                    max_dist = dist
        
        rf_curve.append(max_dist)
    
        if any(ind.coord[1] >= percolates_threshold for ind in current_new_infected):
            percolates = True
            # break
    
    return count_new_infected, percolates, rf_curve

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    parser.add_argument("--sup_prob", type=float, help="Superspreader probability")
    parser.add_argument("--env_pop", type=int, help="Environment population")
    parser.add_argument("--model_type", type=int, help="1 for Super infectiousness model, 2 for Hub model")
    parser.add_argument("--num_sim", type=int, help="Number of MC simulation")
    parser.add_argument("--save_path", type=str, help="Path of final epidemic curve")
    
    args = parser.parse_args()
    
    logging.basicConfig(
        filename='output.log',
        filemode='a',
        encoding='utf-8', 
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    total_percolations = 0
    all_epidemic_curves = []
    
    for _ in range(args.num_sim):
        curve, percolated, _ = main_loop(sup_prob=args.sup_prob, env_pop=args.env_pop, model_type=args.model_type)
        
        if percolated:
            total_percolations += 1
        all_epidemic_curves.append(curve)
        
    # Calculate the percolation probability for this specific parameter set
    percolation_probability = total_percolations / args.num_sim
    
    # Pad curves with zeros if they ended early
    if len(all_epidemic_curves) > 0:
        max_length = max(len(c) for c in all_epidemic_curves)
        padded_curves = [c + [0] * (max_length - len(c)) for c in all_epidemic_curves]
        average_curve = np.mean(padded_curves, axis=0)
    else:
        average_curve = np.array([0]) # Default if no epidemics occurred
    
    filename = f"results_sup{args.sup_prob}_pop{args.env_pop}_mod{args.model_type}.npz"
    np.savez(f"{args.save_path}/{filename}", perc_prob=percolation_probability, epi_curve=average_curve)
    
    logging.info(f"Running Monte Carlo simulation on\n \
                    Superspreader probability:  {args.sup_prob}\n \
                    Environment population:     {args.env_pop}\n \
                    Model type:                 {args.model_type}\n \
                    Percolation Prob: {percolation_probability}\n")