"""

A fun program to automate the web game QWOP.
It will utilize scikit-learn for the neural net
automation and selenium for web browser automation.
"""
import time
import random

from autoqwop.auto_qwop import AUTOQWOP
from autoqwop.genetic import (
    Chromosome,
    crossover,
    mutate,
    get_random_sequence,
    roulette,)


def main():
    """

    Run many iterations and evolve the best combination of keys and time 
    """
    auto_qwop = AUTOQWOP()
    auto_qwop.load_website()
    auto_qwop.get_game()
    pop_size = 100
    population = []
    max_play_time =  300
    crossover_rate = 0.7
    mutation_rate = 0.01
    generations = 0
    fittest = 0.0
    total_fitness = 0.0
    max_chromo_length = 300
    fittest_ind = 0
    goal = 1.1
    try:
        for _ in range(pop_size):
            #Create initial population
            population.append(Chromosome(
                sequence=get_random_sequence(
                    random.randrange(max_chromo_length)),
                fitness=0.0))
        while fittest < goal:
            for i, chromo in enumerate(population):
                #Loop over each member of the population
                game_over = False
                game_won = False
                timed_out = False
                start_time = time.time()
                total_fitness = 0.0
                fittest = 0.0
                while not game_over and not game_won and not timed_out:
                    #Keep looping until game has ended
                    for state in chromo.sequence:
                        #Loop over the steps in the sequence
                        auto_qwop.update_outputs(state)
                        current_frame = auto_qwop.get_frame()
                        game_over = auto_qwop.test_for_game_over(current_frame)
                        game_won = auto_qwop.test_for_game_won(current_frame)
                        if time.time() - start_time >= max_play_time:
                            timed_out = True
                        time.sleep(.033)
                        if game_over or game_won or timed_out:
                            break
                run_time = time.time() - start_time
                if game_won:
                    population[i].fitness = 86/run_time
                if game_over or timed_out:
                    population[i].fitness = run_time/max_play_time
                if population[i].fitness > fittest:
                    fittest = population[i].fitness
                    fittest_ind = i
                print('Played for {} seconds. Chromo length: {}'\
                    .format(run_time, len(population[i].sequence)))
                total_fitness += population[i].fitness
                auto_qwop.restart()
            temp_pop = []
            while len(temp_pop) < pop_size:
                """

                Select offspring from the population via roulette wheel
                selection and create a new population after mating
                and mutating them.
                """
                parent1 = roulette(total_fitness, population)
                parent2 = roulette(total_fitness, population)
                offspring1, offspring2 = crossover(parent1, 
                    parent2, crossover_rate)
                offspring1 = mutate(offspring1, mutation_rate)
                offspring2 = mutate(offspring2, mutation_rate)
                offspring1.fitness = 0.0
                offspring2.fitness = 0.0

                temp_pop.append(offspring1)
                temp_pop.append(offspring2)
            #copy temp_pop to population before starting all over again
            population = temp_pop
            generations += 1
            print("Generation {}".format(generations))
            print("Total fitness = {}".format(total_fitness))
        print("You did it!")
        with open('sequence.txt', 'w') as f:
            print(population[fittest_ind].sequence, file=f)
    except Exception as e:
        print(e)
    finally:
        #clean up
        auto_qwop.driver.quit()

if __name__ == "__main__":
    main()
