from typing import List

import pytest

from source.ga.resources import RaceDecoder


@pytest.fixture(scope="module")
def race_basic_phenom(race_basic, race_basic_genome):
    return RaceDecoder(race_basic).decode(race_basic_genome)


@pytest.fixture(scope="module")
def race_basic_genome_2(race_basic):
    categories = race_basic.categories
    genome: List = list()
    genome.append(categories["HDR"])
    genome.append(categories["D10"])
    genome.append(0)
    genome.append(categories["H12"])
    genome.append(categories["H10"])
    genome.append(1)
    genome.append(categories["D16"])
    genome.append(categories["H16"])
    genome.append(2)
    genome.append(categories["D21"])
    genome.append(categories["H21"])
    genome.append(categories["D12"])

    return genome


@pytest.fixture(scope="module")
def race_basic_phenom_2(race_basic, race_basic_genome_2):
    return RaceDecoder(race_basic).decode(race_basic_genome_2)
