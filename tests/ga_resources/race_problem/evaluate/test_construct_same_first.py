import pytest

from source.ga.resources import RaceProblem, RaceDecoder, construct_same_route_constrained, construct_same_first_constrained


def test_construct_same_route_constrained(race_basic_phenom):
    same_route = construct_same_route_constrained(race_basic_phenom)
    assert same_route

    labels = list()
    for constrained_set in same_route:
        string = ""
        for category in constrained_set:
            string += category.name
            string += ", "
        labels.append(string)

    labels = sorted(labels)

    assert len(same_route) == 18


def test_construct_same_first_constrained(race_basic_phenom):
    same_first = construct_same_first_constrained(race_basic_phenom)

    assert len(same_first) == 6
