"""

A fun program to automate the web game QWOP.
It will utilize scikit-learn for the neural net
automation and selenium for web browser automation.
"""
import time
import random
import argparse
import glob
import os

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

    parser = argparse.ArgumentParser(description='''
        Run a genetic algorithm to play the game qwop''')
    parser.add_argument('--save', '-s', action='store_true')
    parser.add_argument('--seed')
    args = parser.parse_args()

    pop_size = 100
    population = []
    max_play_time = 30
    crossover_rate = 0.7
    mutation_rate = 0.01
    generations = 0
    fittest = 0.0
    total_fitness = 0.0
    max_chromo_length = 100
    fittest_ind = 0
    goal = 20
    image_counter = 0
    step_execute_time = 0.1
    try:
        if args.seed:
            for _ in range(pop_size):
                #Create initial population
                population.append(Chromosome(
                    sequence=args.seed,
                    fitness=0.0))
        else:
            for _ in range(pop_size):
                #Create initial population
                population.append(Chromosome(
                    sequence=get_random_sequence(
                        random.randrange(max_chromo_length, max_chromo_length+1)),
                    fitness=0.0))
        while fittest < goal:
            auto_qwop = AUTOQWOP()
            auto_qwop.load_website()
            auto_qwop.get_game()
            total_fitness = 0.0
            fittest = 0.0
            for i, chromo in enumerate(population):
                #Loop over each member of the population
                game_over = False
                game_won = False
                timed_out = False
                start_time = time.time()
                iters = 0
                current_frame = None
                while not game_over and not game_won and not timed_out:
                    #Keep looping until game has ended
                    for state in chromo.sequence:
                        step_start_time = time.time()
                        #Loop over the steps in the sequence
                        auto_qwop.update_outputs(state)
                        if iters == 0 or iters % 30 == 0:
                            current_frame = auto_qwop.get_frame()
                            game_over = auto_qwop.test_for_game_over(
                                current_frame)
                            game_won = auto_qwop.test_for_game_won(
                                current_frame)
                            if args.save:
                                current_frame.save(
                                    './play_images/{}.png'.format(
                                        image_counter),
                                    'PNG')
                                image_counter += 1
                        if time.time() - start_time >= max_play_time:
                            timed_out = True
                        
                        if game_over or game_won or timed_out:
                            break
                        iters += 1
                        execution_time = time.time() - step_start_time
                        if execution_time < step_execute_time:
                            time.sleep(step_execute_time - execution_time)
                        #print(time.time() - step_start_time)
                run_time = time.time() - start_time
                distance = auto_qwop.get_distance(current_frame)
                speed = distance/run_time

                if game_won:
                    population[i].fitness = distance
                if game_over or timed_out:
                    population[i].fitness = distance

                if population[i].fitness > fittest:
                    fittest = population[i].fitness
                    fittest_ind = i

                print('Ran {} meters in {} seconds!'.format(distance,
                    run_time))
                total_fitness += population[i].fitness
                if timed_out:
                    auto_qwop.driver.refresh()
                    auto_qwop.get_game()
                else:
                    auto_qwop.restart()
            auto_qwop.driver.quit()
            temp_pop = []

            # with open('sequence.txt', 'a') as f:
            #     print('Generation {}'.format(generations), file=f)
            #     for i in population:
            #         print(i.sequence, file=f)
            #         print(i.fitness, file=f)

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
        with open('sequence.txt', 'a') as f:
            print(population[fittest_ind].sequence, file=f)
            print(population[fittest_ind].fitness, file=f)
    except Exception as e:
        print(e)
    finally:
        #clean up
        auto_qwop.driver.quit()

if __name__ == "__main__":
    main()
