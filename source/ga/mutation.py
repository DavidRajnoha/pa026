from collections import Iterator
from random import randint
from typing import List

from leap_ec.individual import Individual


def mutate_permutation(next_individual: Iterator) -> Iterator:
    while True:
        individual: Individual = next(next_individual)
        mutate_genome_switch(individual.genome)
        yield individual


def mutate_genome_switch(genome: List) -> None:
    fst, snd = randint(0, len(genome) - 1), randint(0, len(genome) - 1)
    chromosome_fst = genome[fst]
    genome[fst] = genome[snd]
    genome[snd] = chromosome_fst
