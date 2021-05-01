from source.ga.resources import RaceProblem


def test_evaluate(race_basic, race_basic_genome, race_basic_phenom):
    race_problem = RaceProblem(race_basic)

    evaluation = race_problem.evaluate_hard_constraints(race_basic_phenom)
    assert evaluation
