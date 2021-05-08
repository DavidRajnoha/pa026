import json

import pytest

from source.ga.resources import RaceDecoder


@pytest.fixture(scope="module")
def race_basic_phenom(race_basic, race_basic_genome):
    return RaceDecoder(race_basic).decode(race_basic_genome)


def test_pretty_print(race_basic_phenom):
    print("\n")
    print(race_basic_phenom)


def test_json(race_basic_phenom):
    print("\n")
    print(race_basic_phenom.json_pretty_str())

