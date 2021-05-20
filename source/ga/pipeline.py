from typing import List, Tuple

import toolz
from leap_ec import ops

from leap_ec.individual import Individual
from source.ga import mutation, crossover


def ga_pipeline(population: List[Individual], max_generation: int = 200) -> List:
    """
    Ground logic of the genetic algorithm.
    Randomly initiates the population and then iteratively creates a new generation
    of offsprings using mutations and crossovers and selects the best of offsprings and parents.
    :param population:
    :param max_generation:
    :return:
    """
    population = Individual.evaluate_population(population)
    best_individual: Individual = population[0]

    gen = 0
    while gen < max_generation:

        best_individual, average_fitness = get_metrics(population, best_individual)
        # print("best: " + str(best_fitness) + ", average: " + str(average_fitness))
        # more mutations does not necessarily means better convergence, more then 2 mutations seem to be disruptive
        # to the information available in the solutions, 1 seems to be optimal for the initial converging with
        # an increase to 2 when the average fitness approaches the nest fitness
        # maybe try disruptive mutations on just part of the population, so part will have the good characteristics and
        # part will include change

        mutations_probability = 1 if best_individual.fitness < average_fitness else 2

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

    return best_individual.genome


def get_metrics(population: List[Individual], best_individual: Individual) -> Tuple[Individual, float]:
    sum_fitness = 0
    for individual in population:
        best_individual = min(best_individual, individual, key=lambda x: x.fitness)
        sum_fitness += individual.fitness
    average_fitness = sum_fitness / len(population)
    return best_individual, average_fitness
