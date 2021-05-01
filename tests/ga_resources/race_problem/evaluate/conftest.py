import pytest

from source.ga.resources import RaceDecoder


@pytest.fixture(scope="module")
def race_basic_phenom(race_basic, race_basic_genome):
    return RaceDecoder(race_basic).decode(race_basic_genome)
