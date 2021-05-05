from typing import List

import toolz
from leap_ec import ops

from leap_ec.individual import Individual
from source.ga import mutation, crossover


def ga_pipeline(population: List[Individual], max_generation: int = 200) -> None:
    """
    TODO: Optimization always converges to the best individual, but then it can get stuck on
    TODO: the case when best == average it is waiting on suitable mutation to move it forward
    :param population:
    :param max_generation:
    :return:
    """
    population = Individual.evaluate_population(population)

    gen = 0
    while gen < max_generation:
        best_fitness = 10000
        sum_fitness = 0
        for individual in population:
            best_fitness = min(best_fitness, individual.fitness)
            sum_fitness += individual.fitness
        average_fitness = sum_fitness / len(population)
        print("best: " + str(best_fitness) + ", average: " + str(average_fitness))

        # more mutations does not necessarily means better convergence, more then 2 mutations seem to be disruptive
        # to the information available in the solutions, 1 seems to be optimal for the initial converging with
        # an increase to 2 when the average fitness approaches the nest fitness
        # maybe try disruptive mutations on just part of the population, so part will have the good characteristics and
        # part will include change

        mutations_probability = 1 if best_fitness < average_fitness else 2
        # mutations_count = 1

        offspring = toolz.pipe(population,
                               ops.naive_cyclic_selection,
                               ops.clone,
                               mutation.mutate_permutation(mutations_probability),
                               crossover.crossover_permutation,
                               ops.evaluate,
                               ops.pool(size=len(population)))

        # takes the best from the parents and offsprings
        population = ops.truncation_selection(offspring, len(population), population)

        gen += 1
    pass
