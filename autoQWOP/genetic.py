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


def crossover(parent1, parent2, crossover_rate):
    """

    Performs genetic crossover of two chromosomes to create an offspring.
    """
    if random.random() < crossover_rate:
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


def mutate(individual, mutation_rate):
    """

    Performs a genetic mutation on a chromosome at the specified rate.
    """
    new_chromo = Chromosome(sequence=individual.sequence)
    if random.random() < mutation_rate:
        position = random.randrange(len(individual.sequence))
        mutation = format(random.randrange(16), 'x')
        sequence_list = list(individual.sequence)
        sequence_list[position] = mutation
        new_sequence_string = ''.join(sequence_list)
        new_chromo.sequence = new_sequence_string
    return new_chromo

def get_random_sequence(length):
    """

    Returns a random string of hexadecimal numbers
    """
    sequence = ''
    for i in range(length):
        random_letter = format(random.randrange(16), 'x')
        sequence = '{}{}'.format(sequence, random_letter)
    return sequence