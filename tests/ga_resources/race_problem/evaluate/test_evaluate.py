import pytest

from source.ga.resources import RaceProblem


def test_evaluate(race_basic, race_basic_genome, race_basic_phenom):
    race_problem = RaceProblem(race_basic)

    evaluation = race_problem.evaluate_hard_constraints(race_basic_phenom)
    assert evaluation


def test_evaluate_same_time_req(race_basic, race_basic_phenom):
    race_problem = RaceProblem(race_basic)
    evaluation = race_problem.evaluate_same_start_request(race_basic_phenom)

    assert evaluation == 0


def test_evaluate_same_time_req_unfulfilled(race_basic, race_basic_phenom_2):
    race_problem = RaceProblem(race_basic)
    evaluation = race_problem.evaluate_same_start_request(race_basic_phenom_2)

    assert evaluation == 2


def test_evaluate_time_request(race_basic, race_basic_phenom):
    race_problem = RaceProblem(race_basic)
    race_problem.race.categories["H10"].add_specific_time_request(1)
    evaluation = race_problem.evaluate_specific_time(race_basic_phenom)

    assert evaluation == 0


def test_evaluate_time_request_unfulfilled(race_basic, race_basic_phenom_2):
    race_problem = RaceProblem(race_basic)
    race_problem.race.categories["H10"].add_specific_time_request(1)
    evaluation = race_problem.evaluate_specific_time(race_basic_phenom_2)

    assert evaluation > 0
