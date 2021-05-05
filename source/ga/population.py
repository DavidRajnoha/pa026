import random
from typing import List

from leap_ec.individual import Individual

from source.ga.resources import RaceProblem, RaceDecoder
from source.resources import Race


def random_genome(race: Race) -> List:
    """
    :param race:
    :return:
    """
    genome: List = list(race.categories.values())

    for separator in range(race.concurrent_slots_limit * race.interval - 1):
        genome.append(separator)

    random.shuffle(genome)
    return genome


def create_population(race: Race, size: int):
    """
    Creates a population of Individuals of the RaceProblem using the random_genome function to
    initialize the genome
    :param race: race specification, defining the problem
    :param size: size of the population
    :return: A list of initiated Individuals of RaceProblem
    """

    def initialize():
        return random_genome(race)

    problem = RaceProblem(race)
    decoder = RaceDecoder(race)

    return Individual.create_population(size, initialize=initialize, decoder=decoder, problem=problem)
