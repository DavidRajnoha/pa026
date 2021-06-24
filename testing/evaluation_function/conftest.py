from typing import Dict

import pytest

from source.data_parsing.load_oris import load_entries
from source.data_parsing.oris_constraints import add_oris_constraints
from source.ga.resources import RaceDecoder, RaceProblem
from source.resources import Race, Category


@pytest.fixture(scope="function")
def categories_example():
    def _categories_example() -> Dict[str, Category]:
        categories = load_entries(oris_race_id=5662, ignore_categories=["HDR", "P", "T"])
        add_oris_constraints(categories)
        return categories
    return _categories_example


@pytest.fixture(scope="function")
def race_example(categories_example):
    categories = categories_example()
    return Race(name="example_tesla1", id="5662", categories=categories,
                interval=3, concurrent_slots_limit=4)


@pytest.fixture(scope="function")
def genome_basic(categories_example):
    categories_example = categories_example()

    genome = [categories_example["H35"], 0,
              categories_example["D55"], categories_example["H14"], 1,
              categories_example["H21C"], 2,
              categories_example["D16"], categories_example["D21C"], 3,
              categories_example["D14"], categories_example["H65"], 4,
              categories_example["H12"], categories_example["D65"],  5,
              categories_example["D10"], categories_example["H21D"], categories_example["D20"], categories_example["D18"], 6,
              categories_example["H55"], categories_example["D35"], 7,
              categories_example["H10"], categories_example["D45"], 8,
              categories_example["H10N"], categories_example["D10N"], categories_example["H16"], 9,
              categories_example["H45"], 10,
              categories_example["D21D"], categories_example["H18"], categories_example["D12"],
              ]
    return genome


@pytest.fixture(scope="function")
def genome_extra_time(categories_example):
    categories_example = categories_example()

    genome = [categories_example["H35"], 0,
              categories_example["D55"], categories_example["H14"], 1,
              categories_example["H21C"], categories_example["H16"], 2,
              categories_example["D16"], categories_example["D21C"], 3,
              categories_example["D14"], categories_example["H65"], 4,
              categories_example["H12"], categories_example["D65"],  5,
              categories_example["D10"], categories_example["H21D"], categories_example["D20"], categories_example["D18"], 6,
              categories_example["H55"], categories_example["D35"], 7,
              categories_example["H10"], categories_example["D45"], 8,
              categories_example["H10N"], categories_example["D10N"], 9,
              categories_example["H45"], 10,
              categories_example["D21D"], categories_example["H18"], categories_example["D12"],
              ]
    return genome


@pytest.fixture(scope="function")
def genome_shorter_hard_constraints(categories_example):
    categories_example = categories_example()

    genome = [categories_example["H35"], categories_example["H21D"], 0,
              categories_example["D55"], categories_example["H14"], 1,
              categories_example["H21C"], 2,
              categories_example["D16"], categories_example["D21C"], 3,
              categories_example["D14"], categories_example["H65"], 4,
              categories_example["H12"], categories_example["D65"], categories_example["D20"], 5,
              categories_example["D10"], categories_example["H55"],  6,
              categories_example["D35"], 7,
              categories_example["H10"], categories_example["D45"], categories_example["H18"], 8,
              categories_example["H10N"], categories_example["D10N"], categories_example["H16"], 9,
              categories_example["H45"], categories_example["D18"], 10,
              categories_example["D21D"],  categories_example["D12"],
              ]
    return genome


@pytest.fixture(scope="function")
def genome_soft_constraints_unfulfilled(categories_example):
    categories_example = categories_example()

    genome = [categories_example["H35"], 0,
              categories_example["D55"], categories_example["H14"], 1,
              categories_example["H21C"], 2,
              categories_example["D16"], categories_example["D21C"], 3,
              categories_example["D14"], categories_example["H65"], 4,
              categories_example["H12"], categories_example["D65"],  5,
              categories_example["D10"], categories_example["H21D"], categories_example["D20"], categories_example["D18"], 6,
              categories_example["H55"], categories_example["D35"], 7,
              categories_example["H10"], categories_example["D45"], 8,
              categories_example["H10N"], categories_example["D10N"], categories_example["H16"], 9,
              categories_example["H45"], 10,
              categories_example["D21D"], categories_example["H18"], categories_example["D12"],
              ]
    for _ in range(5):
        categories_example["H16"].add_specific_time_request(105)
    return genome
    

@pytest.fixture(scope="function")
def genome_soft_constraints_fulfilled(categories_example):
    categories_example = categories_example()

    genome = [categories_example["H35"], 0,
              categories_example["D55"], categories_example["H14"], 1,
              categories_example["H21C"], categories_example["H16"], 2,
              categories_example["D16"], categories_example["D21C"], 3,
              categories_example["D14"], categories_example["H65"], 4,
              categories_example["H12"], categories_example["D65"],  5,
              categories_example["D10"], categories_example["H21D"], categories_example["D20"], categories_example["D18"], 6,
              categories_example["H55"], categories_example["D35"], 7,
              categories_example["H10"], categories_example["D45"], 8,
              categories_example["H10N"], categories_example["D10N"], 9,
              categories_example["H45"], 10,
              categories_example["D21D"], categories_example["H18"], categories_example["D12"],
              ]
    for _ in range(5):
        categories_example["H16"].add_specific_time_request(105)
    return genome


@pytest.fixture(scope="function")
def genome_many_soft_constraints_fulfilled(categories_example):
    categories_example = categories_example()

    genome = [categories_example["H35"], 0,
              categories_example["D55"], categories_example["H14"], 1,
              categories_example["H21C"], categories_example["H16"], 2,
              categories_example["D16"], categories_example["D21C"], 3,
              categories_example["D14"], categories_example["H65"], 4,
              categories_example["H12"], categories_example["D65"],  5,
              categories_example["D10"], categories_example["H21D"], categories_example["D20"], categories_example["D18"], 6,
              categories_example["H55"], categories_example["D35"], 7,
              categories_example["H10"], categories_example["D45"], 8,
              categories_example["H10N"], categories_example["D10N"], 9,
              categories_example["H45"], 10,
              categories_example["D21D"], categories_example["H18"], categories_example["D12"],
              ]
    for _ in range(20):
        categories_example["H16"].add_specific_time_request(105)
    return genome


@pytest.fixture(scope="function")
def genome_many_soft_constraints_unfulfilled(categories_example):
    categories_example = categories_example()

    genome = [categories_example["H35"], 0,
              categories_example["D55"], categories_example["H14"], 1,
              categories_example["H21C"], 2,
              categories_example["D16"], categories_example["D21C"], 3,
              categories_example["D14"], categories_example["H65"], 4,
              categories_example["H12"], categories_example["D65"], 5,
              categories_example["D10"], categories_example["H21D"], categories_example["D20"],
              categories_example["D18"], 6,
              categories_example["H55"], categories_example["D35"], 7,
              categories_example["H10"], categories_example["D45"], 8,
              categories_example["H10N"], categories_example["D10N"], categories_example["H16"], 9,
              categories_example["H45"], 10,
              categories_example["D21D"], categories_example["H18"], categories_example["D12"],
              ]
    for _ in range(20):
        categories_example["H16"].add_specific_time_request(105)
    return genome


@pytest.fixture(scope="function")
def phenom_basic(genome_basic, race_example):
    decoder = RaceDecoder(race_example)
    return decoder.decode(genome_basic)


@pytest.fixture(scope="function")
def phenom_extra_time(genome_extra_time, race_example):
    decoder = RaceDecoder(race_example)
    return decoder.decode(genome_extra_time)


@pytest.fixture(scope="function")
def phenom_shorter_hard_constraints(genome_shorter_hard_constraints, race_example):
    decoder = RaceDecoder(race_example)
    return decoder.decode(genome_shorter_hard_constraints)


@pytest.fixture(scope="function")
def phenom_soft_constraints_fulfilled(genome_soft_constraints_fulfilled, race_example):
    decoder = RaceDecoder(race_example)
    return decoder.decode(genome_soft_constraints_fulfilled)


@pytest.fixture(scope="function")
def phenom_many_soft_constraints_fulfilled(genome_many_soft_constraints_fulfilled, race_example):
    decoder = RaceDecoder(race_example)
    return decoder.decode(genome_many_soft_constraints_fulfilled)


@pytest.fixture(scope="function")
def phenom_soft_constraints_unfulfilled(genome_soft_constraints_unfulfilled, race_example):
    decoder = RaceDecoder(race_example)
    return decoder.decode(genome_soft_constraints_unfulfilled)


@pytest.fixture(scope="function")
def phenom_many_soft_constraints_unfulfilled(genome_many_soft_constraints_unfulfilled, race_example):
    decoder = RaceDecoder(race_example)
    return decoder.decode(genome_many_soft_constraints_unfulfilled)


@pytest.fixture(scope="function")
def race_problem(race_example):
    return RaceProblem(race_example)
