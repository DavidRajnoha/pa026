from source.ga.mutation import mutate_permutation, mutate_genome_switch


def test_mutate_genome(race_basic_genome):
    race_basic_genome_copy = race_basic_genome[:]
    mutate_genome_switch(race_basic_genome_copy)
    assert race_basic_genome != race_basic_genome_copy
