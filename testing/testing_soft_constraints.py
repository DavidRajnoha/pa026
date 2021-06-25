import json
import math
from random import randint
from datetime import datetime
from multiprocessing import Pool

from source.data_parsing.load_oris import load_metadata, load_ids, InvalidDataException, load_ignored_categories
from source.ga.resources import RaceProblem
from source.interface.app_logic import schedule_categories

NUMBER_OF_RUNS = 5
IDs = [5662, 4930, 4931, 4932, 4933]

# IDs = [4930, 4931, 4932, 4933, 4935, 4937, 4938, 4939, 4940]


def test_soft_constraints():
    results = dict()
    filename = "soft_constraints" + str(datetime.now())
    ids = IDs

    for size, iteration in [(40, 800)]:
        average_eff = 0
        for i in range(NUMBER_OF_RUNS):
            average_eff += test_set_of_races(iteration, size, ids, filename)
        average_eff /= NUMBER_OF_RUNS
        results[str(iteration) + "_" + str(size)] = average_eff

    print(average_eff)


def test_set_of_races(iterations, size, ids, filename=None, ):
    average_efficiency_difference = 0
    filename = filename or "results_2018_run_1" + str(datetime.now())
    data = list()

    for id in ids:
        data.append((id, iterations, size))

    with Pool(processes=10) as pool:
        results = pool.map_async(process_race, data).get()

        for result in results:
            if result is None:
                continue
            oris_id, real_eff, computed_eff, efficiency_diff, real_time, computed_time, fitness,\
                spec_time_score, same_time_score = result
            with open(filename, "a") as file:
                file.write(str(oris_id) + ',' +
                           str(real_eff) + ',' +
                           str(computed_eff) + ',' +
                           str(efficiency_diff) + ',' +
                           str(fitness) + ',' +
                           str(spec_time_score) + ',' +
                           str(same_time_score) + ',' +
                           '\n')
                average_efficiency_difference += efficiency_diff

    average_efficiency_difference /= len(IDs)
    # with open(filename, "a") as file:
    #     file.write(str(average_efficiency_difference) + "\n")

    return average_efficiency_difference


def process_race(id_iterations_population):
    oris_id, iterations, population_size = id_iterations_population
    time_req_f = "/home/drajnoha/PycharmProjects/pa026/resources/" + str(oris_id) + "_time_requests"
    same_start_req_f = "/home/drajnoha/PycharmProjects/pa026/resources/" + str(oris_id) + "_same_start_requests"

    try:
        ignored_categories = load_ignored_categories(oris_id)

        interval, concurrent, efficiency, last_start, entries = load_metadata(oris_id, ignored_categories)
        if efficiency < 0.1:
            return None

        best_pretty, best_json, best_phenom, race = schedule_categories(oris_id, None, same_start_req_f, time_req_f,
                                                                        ignored_categories,
                                                                  interval, math.ceil(sum(concurrent) / interval),
                                                                  iterations, population_size)
    except Exception as e:
        print(e)
        return None

    race_problem = RaceProblem(race)

    efficiency_diff = efficiency - best_phenom.efficiency()
    return oris_id, efficiency, best_phenom.efficiency(), efficiency_diff, last_start, best_phenom.total_length(),\
        race_problem.evaluate(best_phenom), race_problem.evaluate_specific_time(best_phenom),\
           race_problem.evaluate_same_start_request(best_phenom)
