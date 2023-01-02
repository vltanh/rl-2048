import numpy as np


class RandomAgent:
    def move(self, _):
        return np.random.choice(['L', 'R', 'U', 'D'])
