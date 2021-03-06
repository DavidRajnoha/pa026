"""
Logic related to mutations.
"""

import math
from collections import Iterator
from random import randint
from typing import List

from leap_ec.individual import Individual


def mutate_permutation(mutation_prob: float):
    """
    Mutates the genome of an individual.
    The floor of the mutation_prob determines the number of mutation that will be conducted,
    the decimal part is the probability of an additional mutation.
    """
    def _mutate_permutation(next_individual: Iterator) -> Iterator:
        while True:
            individual: Individual = next(next_individual)
            mutation_count = math.floor(mutation_prob)
            last_mutation_prob = mutation_prob - mutation_count

            for _ in range(mutation_count):
                mutate_genome_switch(individual.genome)
            if randint(1, 100) / 100 < last_mutation_prob:
                mutate_genome_switch(individual.genome)

            yield individual

    return _mutate_permutation


def mutate_genome_switch(genome: List) -> None:
    """
    Basic mutation for permutations
    Takes two random chromosomes and switches them
    """
    fst, snd = randint(0, len(genome) - 1), randint(0, len(genome) - 1)
    chromosome_fst = genome[fst]
    genome[fst] = genome[snd]
    genome[snd] = chromosome_fst
