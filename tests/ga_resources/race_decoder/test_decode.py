"""
Tests the decode function of the RaceDecoder
"""
from typing import List

import pytest

from source.ga.resources import RaceDecoder


@pytest.fixture(scope="module")
def race_basic_genome_empty_slot(race_basic):
    categories = race_basic.categories
    genome: List = list()
    genome.append(categories["HDR"])
    genome.append(categories["D10"])
    genome.append(0)
    genome.append(1)
    genome.append(categories["H10"])
    genome.append(categories["D12"])
    genome.append(categories["H12"])
    genome.append(categories["D16"])
    genome.append(categories["H16"])
    genome.append(2)
    genome.append(categories["D21"])
    genome.append(categories["H21"])

    return genome


def test_decode_basic_genome(race_basic, race_basic_genome):
    decoder = RaceDecoder(race_basic)
    phenom = decoder.decode(genome=race_basic_genome)
    assert phenom

    assert len(phenom.slots[0].categories) == 2
    assert len(phenom.slots[1].categories) == 3
    assert len(phenom.slots[2].categories) == 2
    assert len(phenom.slots[3].categories) == 2

    assert race_basic.categories['HDR'] in phenom.slots[0].categories
    assert race_basic.categories['H10'] in phenom.slots[1].categories
    assert race_basic.categories['H16'] in phenom.slots[2].categories
    assert race_basic.categories['D21'] in phenom.slots[3].categories


def test_decode_empty_slots(race_basic, race_basic_genome_empty_slot):
    decoder = RaceDecoder(race_basic)
    phenom = decoder.decode(genome=race_basic_genome_empty_slot)
    assert phenom

    assert len(phenom.slots[0].categories) == 2
    assert len(phenom.slots[1].categories) == 0
    assert len(phenom.slots[2].categories) == 5
    assert len(phenom.slots[3].categories) == 2

    assert race_basic.categories['HDR'] in phenom.slots[0].categories
    assert phenom.slots[1].categories == []
    assert race_basic.categories['H16'] in phenom.slots[2].categories
    assert race_basic.categories['D21'] in phenom.slots[3].categories
