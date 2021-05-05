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
        offspring = toolz.pipe(population,
                               ops.naive_cyclic_selection,
                               ops.clone,
                               mutation.mutate_permutation,
                               crossover.crossover_permutation,
                               ops.evaluate,
                               ops.pool(size=len(population)))

        population = ops.truncation_selection(offspring, len(population), population)
        best_fitness = 10000
        sum_fitness = 0
        for individual in population:
            best_fitness = min(best_fitness, individual.fitness)
            sum_fitness += individual.fitness
        print("best: " + str(best_fitness) + ", average: " + str(sum_fitness/len(population)))

        gen += 1
    pass
