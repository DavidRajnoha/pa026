from typing import Dict, List

import pytest
from source.resources import Category, Race


@pytest.fixture(scope="module")
def race_basic_genome(race_basic):
    categories = race_basic.categories
    genome: List = list()
    genome.append(categories["HDR"])
    genome.append(categories["D10"])
    genome.append("|")
    genome.append(categories["H10"])
    genome.append(categories["D12"])
    genome.append(categories["H12"])
    genome.append("|")
    genome.append(categories["D16"])
    genome.append(categories["H16"])
    genome.append("|")
    genome.append(categories["D21"])
    genome.append(categories["H21"])

    return genome


@pytest.fixture(scope="module")
def race_basic():
    categories: Dict[str, Category] = dict()
    for name, size in [("HDR", 10), ("D10", 4), ("H10", 5), ("D12", 2),
                       ("H12", 13), ("D16", 1), ("H16", 4), ("D21", 9), ("H21", 12)]:
        category = Category(name, size)
        categories[name] = category

    add_same_first_constraints(categories)
    add_same_route_constraints(categories)

    race: Race = Race(name="basic", id=1, categories=categories,
                      interval=2, concurrent_slots_limit=2)
    return race


def add_same_route_constraints(categories: Dict[str, Category]):
    categories["H10"].add_same_route_constraint(categories["HDR"])
    categories["HDR"].add_same_route_constraint(categories["H10"])

    categories["H21"].add_same_route_constraint(categories["H16"])
    categories["H16"].add_same_route_constraint(categories["H21"])


def add_same_first_constraints(categories):
    categories["HDR"].add_same_first_constraint(categories["D12"])
    categories["D12"].add_same_first_constraint(categories["HDR"])
    categories["H10"].add_same_first_constraint(categories["HDR"])
    categories["H10"].add_same_first_constraint(categories["D12"])
    categories["HDR"].add_same_first_constraint(categories["H10"])
    categories["D12"].add_same_first_constraint(categories["H10"])

    categories["H21"].add_same_first_constraint(categories["H16"])
    categories["H16"].add_same_first_constraint(categories["H21"])

    categories["D16"].add_same_first_constraint(categories["D21"])
    categories["D21"].add_same_first_constraint(categories["D16"])
    categories["D16"].add_same_first_constraint(categories["D10"])
    categories["D10"].add_same_first_constraint(categories["D16"])
    categories["D10"].add_same_first_constraint(categories["D21"])
    categories["D21"].add_same_first_constraint(categories["D10"])


@pytest.fixture(scope="module")
def race_example():
    categories: Dict[str, Category] = dict()
    for name, size in [("D10N", 11), ("D10", 16), ("D12", 23), ("D14", 20),
                       ("D16", 8), ("D18", 1), ("D20", 1), ("D21C", 17), ("D21D", 5),
                       ("D35", 24), ("D45", 12), ("D55", 6), ("D65", 4),
                       ("H10N", 6), ("H10", 15), ("H12", 22), ("H14", 20),
                       ("H16", 10), ("H18", 2), ("H20", 0), ("H21C", 29), ("H21D", 3),
                       ("H35", 28), ("H45", 24), ("H55", 9), ("H65", 5),
                       ]:
        category = Category(name, size)
        categories[name] = category

    add_same_first_example(categories)

    race: Race = Race(name="example_tesla1", id=2, categories=categories,
                      interval=3, concurrent_slots_limit=4)

    return race


def add_same_first_example(categories):
    # 231
    categories["H45"].add_same_first_constraint(categories["D55"])
    categories["D55"].add_same_first_constraint(categories["H45"])
    categories["H45"].add_same_first_constraint(categories["H65"])
    categories["H65"].add_same_first_constraint(categories["H45"])
    categories["D55"].add_same_first_constraint(categories["H65"])
    categories["H65"].add_same_first_constraint(categories["D55"])
    
    # 232
    categories["H35"].add_same_first_constraint(categories["D35"])
    categories["D35"].add_same_first_constraint(categories["H35"])
    categories["H35"].add_same_first_constraint(categories["H55"])
    categories["H55"].add_same_first_constraint(categories["H35"])
    categories["D35"].add_same_first_constraint(categories["H55"])
    categories["H55"].add_same_first_constraint(categories["D35"])
    
    # 34
    categories["H21C"].add_same_first_constraint(categories["H18"])
    categories["H18"].add_same_first_constraint(categories["H21C"])
    categories["H21C"].add_same_first_constraint(categories["H20"])
    categories["H20"].add_same_first_constraint(categories["H21C"])
    categories["H21C"].add_same_first_constraint(categories["D45"])
    categories["D45"].add_same_first_constraint(categories["H21C"])
    
    categories["H18"].add_same_first_constraint(categories["H20"])
    categories["H20"].add_same_first_constraint(categories["H18"])
    categories["H18"].add_same_first_constraint(categories["D45"])
    categories["D45"].add_same_first_constraint(categories["H18"])

    categories["H20"].add_same_first_constraint(categories["D45"])
    categories["D45"].add_same_first_constraint(categories["H20"])

    # 226
    categories["H16"].add_same_first_constraint(categories["D21D"])
    categories["D21D"].add_same_first_constraint(categories["H16"])
    categories["H16"].add_same_first_constraint(categories["D65"])
    categories["D65"].add_same_first_constraint(categories["H16"])
    categories["H16"].add_same_first_constraint(categories["D21C"])
    categories["D21C"].add_same_first_constraint(categories["H16"])

    categories["D21D"].add_same_first_constraint(categories["D65"])
    categories["D65"].add_same_first_constraint(categories["D21D"])
    categories["D21D"].add_same_first_constraint(categories["D21C"])
    categories["D21C"].add_same_first_constraint(categories["D21D"])

    categories["D65"].add_same_first_constraint(categories["D21C"])
    categories["D21C"].add_same_first_constraint(categories["D65"])
    
    # 32
    categories["H14"].add_same_first_constraint(categories["D14"])
    categories["D14"].add_same_first_constraint(categories["H14"])
    
    # 237
    categories["H12"].add_same_first_constraint(categories["D12"])
    categories["D12"].add_same_first_constraint(categories["H12"])

    # 210
    categories["H10"].add_same_first_constraint(categories["D10"])
    categories["D10"].add_same_first_constraint(categories["H10"])
    
    # 58
    categories["D20"].add_same_first_constraint(categories["H21D"])
    categories["H21D"].add_same_first_constraint(categories["D20"])
    categories["D20"].add_same_first_constraint(categories["D16"])
    categories["D16"].add_same_first_constraint(categories["D20"])
    categories["D20"].add_same_first_constraint(categories["D18"])
    categories["D18"].add_same_first_constraint(categories["D20"])

    categories["H21D"].add_same_first_constraint(categories["D16"])
    categories["D16"].add_same_first_constraint(categories["H21D"])
    categories["H21D"].add_same_first_constraint(categories["D18"])
    categories["D18"].add_same_first_constraint(categories["H21D"])

    categories["D16"].add_same_first_constraint(categories["D18"])
    categories["D18"].add_same_first_constraint(categories["D16"])
