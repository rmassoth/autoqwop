"""

A simple genetic algorithm for finding the optimal
button presses for playing the game QWOP.
"""

import random

class Chromosome():
    """

    Represents a single chromosome.
    """

    def __init__(self, sequence="", fitness=0.0):
        self.sequence = sequence
        self.fitness = fitness


def crossover(parent1, parent2, rate):
    """

    Performs genetic crossover of two chromosomes to create an offspring.
    """
    if random.random() < rate:
        crossover = int(random.random() * len(parent1.sequence))
        chromo1 = "{}{}".format(
            parent1.sequence[:crossover],
            parent2.sequence[crossover:])
        chromo2 = "{}{}".format(
            parent2.sequence[:crossover],
            parent1.sequence[crossover:])
        return Chromosome(sequence=chromo1), Chromosome(sequence=chromo2)
    else:
        return parent1, parent2


def mutate():
    """

    Performs a genetic mutation on a chromosome.
    """
    pass