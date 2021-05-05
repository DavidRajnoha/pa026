from source.ga.pipeline import ga_pipeline
from source.ga.population import create_population
import random


def test_pipeline(race_basic):
    random.seed(42)
    population = create_population(race_basic, 20)
    ga_pipeline(population)

    assert population


def test_pipeline_example(race_example):
    random.seed(38)
    population = create_population(race_example, 40)
    ga_pipeline(population, 200)

    assert population
