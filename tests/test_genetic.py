import pytest

from autoQWOP.genetic import Chromosome, crossover, mutate

def test_chromo():
    sequence = "235562513"
    fitness = 1.2
    chromo = Chromosome(sequence=sequence, fitness=fitness)
    assert chromo.sequence == sequence
    assert chromo.fitness == fitness

def test_crossover():
    parent1 = Chromosome(sequence="12345")
    parent2 = Chromosome(sequence="54321")
    offspring1, offspring2 = crossover(parent1, parent2, 1.1)
    assert offspring1.sequence != parent1.sequence
    assert offspring1.sequence != parent2.sequence
    assert offspring2.sequence != parent1.sequence
    assert offspring2.sequence != parent2.sequence
    assert offspring1.sequence != offspring2.sequence

def test_no_crossover():
    parent1 = Chromosome(sequence="12345")
    parent2 = Chromosome(sequence="54321")
    offspring1, offspring2 = crossover(parent1, parent2, 0.0)
    assert offspring1.sequence == parent1.sequence
    assert offspring1.sequence != parent2.sequence
    assert offspring2.sequence != parent1.sequence
    assert offspring2.sequence == parent2.sequence
    assert offspring1.sequence != offspring2.sequence

def test_mutate():
    pass