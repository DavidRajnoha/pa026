from source.ga.population import create_population, random_genome


def test_create_population(race_example):
    population = create_population(race_example, 20)
    assert population


def test_random_genome(race_basic):
    genome = random_genome(race_basic)
    assert genome


def test_random_genome_example(race_example):
    genome = random_genome(race_example)
    assert genome
