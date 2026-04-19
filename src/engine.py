import numpy as np

from variables import *

def initialize():
    pass

def main_loop(model_type = 1):
    count_new_infected = [] # size = number of time steps
    population = [] # size = ENV_POP
    
    while True:
        current_infected = []
        current_susceptible = []
        current_new_infected = []
        
        