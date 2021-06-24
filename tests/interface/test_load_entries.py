from typing import Dict

import pytest

from source.data_parsing.load_soft_constraints import load_time_requests, load_same_start_requests
from source.data_parsing.oris_constraints import add_oris_constraints
from source.resources import Category
from source.data_parsing.load_route_constraints import add_constraints
from source.data_parsing.load_oris import load_entries, load_controls


@pytest.fixture(scope="module")
def categories_example():
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

    return categories


def test_load_constraints(categories_example):
    add_constraints(categories_example, "/home/drajnoha/PycharmProjects/pa026/resources/JML2020TBM.Courses.Edited.txt")
    assert categories_example['D20'] in categories_example['H21D'].same_first_constraint


def test_load_entries(categories_example):
    categories = load_entries(oris_race_id=5662, ignore_categories=["HDR", "P", "T"])
    assert len(categories) == 26
    for category in categories:
        assert category in categories_example
        assert categories[category].num_entries == categories_example[category].num_entries


def test_load_times(categories_example):
    load_time_requests(categories_example,
                       filename="/home/drajnoha/PycharmProjects/pa026/resources/JML2020TBM_time_requests")
    assert 45 in categories_example['H10'].specific_time_request
    assert 55 in categories_example['H10'].specific_time_request


def test_load_same_start_req(categories_example):
    load_same_start_requests(categories_example,
                             filename="/home/drajnoha/PycharmProjects/pa026/resources/JML2020TBM_same_start_requests")
    assert categories_example['H21C'] in categories_example['H10'].same_time_request
    assert categories_example['H10'] in categories_example['H21C'].same_time_request


def test_load():
    categories = load_entries(oris_race_id=5662, ignore_categories=["HDR", "P", "T"])
    add_constraints(categories, "/home/drajnoha/PycharmProjects/pa026/resources/JML2020TBM.Courses.Edited.txt")
    load_time_requests(categories,
                       filename="/home/drajnoha/PycharmProjects/pa026/resources/JML2020TBM_time_requests")
    load_same_start_requests(categories,
                             filename="/home/drajnoha/PycharmProjects/pa026/resources/JML2020TBM_same_start_requests")
    assert categories['D20'] in categories['H21D'].same_first_constraint
    assert 44 in categories['D20'].specific_time_request
    assert categories['H21C'] in categories['H10'].same_time_request


def test_load_controls():
    categories = load_entries(oris_race_id=5662, ignore_categories=["HDR", "P", "T"])
    add_oris_constraints(categories)

    assert categories['D20'] in categories['H21D'].same_first_constraint






