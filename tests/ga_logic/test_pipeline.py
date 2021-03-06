from source.ga.pipeline import ga_pipeline
from source.ga.population import create_population
from source.ga.resources import RaceDecoder
import random


def test_pipeline(race_basic):
    random.seed(42)
    population = create_population(race_basic, 20)
    ga_pipeline(population)

    assert population


def test_pipeline_example(race_example):
    random.seed(39)
    population = create_population(race_example, 40)
    best_indv = ga_pipeline(population, 200)

    phenom = RaceDecoder(race_example).decode(best_indv)
    print(phenom)
    print(phenom.json())

    assert best_indv


