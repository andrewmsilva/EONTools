import numpy.random as random
from itertools import combinations

class Demand():
    def __init__(self, source, target, data_rate):
        self.source = source
        self.target = target
        self.data_rate = data_rate
        self.links_path = None
        self.path_length = None
        self.modulation_level = None
        self.frequency_slots = None
        self.spectrum_begin = None
        self.status = None

    def __repr__(self):
        return '<%s to %s: %d GBps>'%(self.source, self.target, self.data_rate)

    def __str__(self):
        return '<%s to %s: %d GBps>'%(self.source, self.target, self.data_rate)

    def reset(self):
        self.links_path = None
        self.path_length = None
        self.modulation_level = None
        self.frequency_slots = None
        self.spectrum_begin = None
        self.status = None

def createRandomDemands(eon, possible_data_rate=[40, 100, 200, 400, 1000], random_state=None):
    # Shuffle nodes
    if random_state is not None:
        random.seed(random_state)
    # Setting data rate probabilities
    length = len(possible_data_rate)
    total = (length**2 + length)/2
    p = [x/total for x in range(length, 0, -1)]
    # Creating demands
    demands = []
    for source, target in combinations(eon.nodes(), 2):
        demands.append(Demand(source, target, random.choice(possible_data_rate, p=p)))
    random.shuffle(demands)
    return demands