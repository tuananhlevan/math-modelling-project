import numpy as np
from src.variables import *

class Individual:

    def __init__(self):
        self.health_state = 'S'
        self.coord = [np.random.uniform(0, 1) * ENV_WIDTH, np.random.uniform(0, 1) * ENV_WIDTH]
        self.super_spreader = False
        self.infected_by = None
        self.links_count = 0

    def euclidean_distance(self, other):
        x_delta = abs(self.coord[0] - other.coord[0])
        if x_delta > 1 / 2 * ENV_WIDTH:
            x_delta = ENV_WIDTH - x_delta
        y_delta = abs(self.coord[1] - other.coord[1])
        return np.sqrt(pow(x_delta, 2) + pow(y_delta, 2))

    def infect(self, other, model_type):
        r = self.euclidean_distance(other)
        if model_type == 1:
            if r <= INFECT_CUTOFF:
                if self.super_spreader:
                    prob = SUPER_INFECT
                else:
                    prob = SUPER_INFECT * pow(1 - r / INFECT_CUTOFF, INFECT_ALPHA)
            else:
                prob = 0
        elif model_type == 2:
            if self.super_spreader:
                if r <= INFECT_CUTOFF * np.sqrt(6):
                    prob = SUPER_INFECT * pow(1 - r / (INFECT_CUTOFF * np.sqrt(6)), INFECT_ALPHA)
                else:
                    prob = 0
            elif r <= INFECT_CUTOFF:
                prob = SUPER_INFECT * pow(1 - r / INFECT_CUTOFF, INFECT_ALPHA)
            else:
                prob = 0
        if np.random.uniform(0, 1) < prob:
            other.health_state = 'I'

    def recover(self):
        if np.random.uniform(0, 1) < RECOVER_PROB:
            self.health_state = 'R'