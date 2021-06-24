
def test_phenom1(phenom_basic, phenom_extra_time, phenom_shorter_hard_constraints, race_problem):
    """
    TODO: tinker with soft constraints and time and test, that the evaluation function evaluates "correctly"
    """
    print(str(phenom_basic))
    print(str(phenom_extra_time))
    print(str(phenom_shorter_hard_constraints))

    score_basic = race_problem.evaluate(phenom_basic)
    score_extra = race_problem.evaluate(phenom_extra_time)
    score_hard = race_problem.evaluate(phenom_shorter_hard_constraints)

    print(score_basic)
    print(score_extra)
    print(score_hard)

    assert score_basic < score_extra < score_hard


def test_soft_vs_time(phenom_soft_constraints_fulfilled, phenom_soft_constraints_unfulfilled, phenom_basic,
                      race_problem):
    print(str(phenom_basic))
    print(str(phenom_soft_constraints_fulfilled))
    print(str(phenom_soft_constraints_unfulfilled))

    score_basic = race_problem.evaluate(phenom_basic)
    score_fulfilled = race_problem.evaluate(phenom_soft_constraints_fulfilled)
    score_unfulfilled = race_problem.evaluate(phenom_soft_constraints_unfulfilled)

    print(score_basic)
    print(score_fulfilled)
    print(score_unfulfilled)

    assert score_basic < score_unfulfilled < score_fulfilled


def test_soft_vs_time_many(phenom_many_soft_constraints_fulfilled, phenom_many_soft_constraints_unfulfilled, phenom_basic,
                      race_problem):
    print(str(phenom_basic))
    print(str(phenom_many_soft_constraints_fulfilled))
    print(str(phenom_many_soft_constraints_unfulfilled))

    score_basic = race_problem.evaluate(phenom_basic)
    score_fulfilled = race_problem.evaluate(phenom_many_soft_constraints_fulfilled)
    score_unfulfilled = race_problem.evaluate(phenom_many_soft_constraints_unfulfilled)

    print(score_basic)
    print(score_fulfilled)
    print(score_unfulfilled)

    assert score_basic < score_fulfilled < score_unfulfilled
