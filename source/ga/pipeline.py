from typing import List

import toolz
from leap_ec import ops

from leap_ec.individual import Individual
from source.ga import mutation, crossover


def ga_pipeline(population: List[Individual], max_generation: int = 200) -> None:
    """
    TODO: optimization based on the time does not work. The crossover probably doesn't transmit the characteristics
    TODO: of the short phenotype, also the initial population is not well defined
    :param population:
    :param max_generation:
    :return:
    """
    population = Individual.evaluate_population(population)

    gen = 0
    while gen < max_generation:
        offspring = toolz.pipe(population,
                               ops.tournament_selection,
                               ops.clone,
                               mutation.mutate_permutation,
                               crossover.crossover_permutation,
                               ops.evaluate,
                               ops.pool(size=len(population)))

        population = offspring
        best_fitness = 10000
        sum_fitness = 0
        for individual in population:
            best_fitness = min(best_fitness, individual.fitness)
            sum_fitness += individual.fitness
        print("best: " + str(best_fitness) + ", average: " + str(sum_fitness/len(population)))

        gen += 1
