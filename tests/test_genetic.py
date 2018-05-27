import pytest

from autoQWOP.genetic import (
    Chromosome,
    crossover,
    mutate,
    get_random_sequence)

def test_chromo():
    sequence = "2355625130"
    fitness = 1.2
    chromo = Chromosome(sequence=sequence, fitness=fitness)
    assert chromo.sequence == sequence
    assert chromo.fitness == fitness

def test_crossover():
    parent1 = Chromosome(sequence="0123456789ABCDEF")
    parent2 = Chromosome(sequence="FEDCBA98765543210")
    offspring1, offspring2 = crossover(parent1, parent2, 1.1)
    assert offspring1.sequence != parent1.sequence
    assert offspring1.sequence != parent2.sequence
    assert offspring2.sequence != parent1.sequence
    assert offspring2.sequence != parent2.sequence
    assert offspring1.sequence != offspring2.sequence

def test_no_crossover():
    parent1 = Chromosome(sequence="0123456789ABCDEF")
    parent2 = Chromosome(sequence="FEDCBA9876543210")
    offspring1, offspring2 = crossover(parent1, parent2, 0.0)
    assert offspring1.sequence == parent1.sequence
    assert offspring1.sequence != parent2.sequence
    assert offspring2.sequence != parent1.sequence
    assert offspring2.sequence == parent2.sequence
    assert offspring1.sequence != offspring2.sequence

def test_mutate():
    """

    Mutate 5 indiviuals with identical sequences and make sure 
    that they are mutated in a random way.
    """
    sequence = "0123456789ABCDEF"
    individual1 = Chromosome(sequence=sequence)
    individual2 = Chromosome(sequence=sequence)
    individual3 = Chromosome(sequence=sequence)
    individual4 = Chromosome(sequence=sequence)
    individual5 = Chromosome(sequence=sequence)
    mutated1 = mutate(individual1, 1.0)
    mutated2 = mutate(individual2, 1.0)
    mutated3 = mutate(individual3, 1.0)
    mutated4 = mutate(individual4, 1.0)
    mutated5 = mutate(individual5, 1.0)
    assert mutated1.sequence != individual1.sequence
    assert mutated2.sequence != individual2.sequence
    assert mutated3.sequence != individual3.sequence
    assert mutated4.sequence != individual4.sequence
    assert mutated5.sequence != individual5.sequence
    assert mutated1.sequence != individual2.sequence
    assert mutated1.sequence != individual3.sequence
    assert mutated1.sequence != individual4.sequence
    assert mutated1.sequence != individual5.sequence

def test_no_mutate():
    sequence = "123456789ABCDEF"
    individual = Chromosome(sequence=sequence)
    mutated = mutate(individual, 0.0)
    assert mutated.sequence == individual.sequence

def test_random_sequence():
    hex_chars = {'0',
        '1',
        '2',
        '3',
        '4',
        '5',
        '6',
        '7',
        '8',
        '9',
        'a',
        'b',
        'c',
        'd',
        'e',
        'f'}
    sequence_length = 10
    sequence = get_random_sequence(sequence_length)
    assert len(sequence) == sequence_length
    for letter in sequence:
        assert letter in hex_chars
