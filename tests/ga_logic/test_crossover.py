from typing import List

import pytest

from source.ga.crossover import get_cycles, order_crossover, separate_genome, merge_genome, crossover_genome_permutation


@pytest.fixture(scope="module")
def race_basic_genome_snd(race_basic):
    categories = race_basic.categories
    genome: List = list()
    genome.append(categories["D10"])
    genome.append("|")
    genome.append(categories["H16"])
    genome.append(categories["D21"])
    genome.append(categories["H10"])
    genome.append("|")
    genome.append(categories["HDR"])
    genome.append(categories["D12"])
    genome.append(categories["H12"])
    genome.append("|")
    genome.append(categories["D16"])
    genome.append(categories["H21"])

    return genome


def test_get_cycles():
    g_fst = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    g_snd = [9, 3, 7, 8, 2, 6, 5, 1, 4]

    cycles = get_cycles(g_fst, g_snd)
    assert len(cycles) == 3
    assert sorted(cycles[0]) == [0, 3, 7, 8]
    assert sorted(cycles[1]) == [1, 2, 4, 6]
    assert sorted(cycles[2]) == [5]


def test_order_crossover():
    g_fst = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    g_snd = [9, 3, 7, 8, 2, 6, 5, 1, 4]

    offspring_fst, offspring_snd = order_crossover(g_fst, g_snd)

    assert offspring_fst == [1, 3, 7, 4, 2, 6, 5, 8, 9]
    assert offspring_snd == [9, 2, 3, 8, 5, 6, 7, 1, 4]


def test_separate_genome(race_basic_genome, race_basic):
    g_cat, g_slots = separate_genome(race_basic_genome)
    assert g_cat == [race_basic.categories["HDR"],
                     race_basic.categories["D10"],
                     race_basic.categories["H10"],
                     race_basic.categories["D12"],
                     race_basic.categories["H12"],
                     race_basic.categories["D16"],
                     race_basic.categories["H16"],
                     race_basic.categories["D21"],
                     race_basic.categories["H21"],
                     ]
    assert g_slots == [2, 6, 9]


def test_merge_genome(race_basic_genome):
    g_cat, g_slots = separate_genome(race_basic_genome)
    assert merge_genome(g_cat, g_slots) == race_basic_genome


def test_crossover_genome_permuttion(race_basic_genome, race_basic_genome_snd):
    offspring_fst, offspring_snd = crossover_genome_permutation(race_basic_genome, race_basic_genome_snd)
    assert offspring_fst != offspring_snd != race_basic_genome_snd != race_basic_genome
