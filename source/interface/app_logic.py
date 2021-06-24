import json
from typing import List, Dict, Tuple, Optional, Set

from source.data_parsing.load_oris import load_entries
from source.data_parsing.load_route_constraints import add_constraints
from source.data_parsing.load_soft_constraints import load_time_requests, load_same_start_requests
from source.data_parsing.oris_constraints import add_oris_constraints
from source.ga.population import create_population
from source.resources import Race, Category
from source.ga.pipeline import ga_pipeline
from source.ga.resources import RaceDecoder, RacePhenom


def create_race(oris_id: int, course_definition_f: Optional[str], same_start_req_f: Optional[str],
                specific_time_req_f: Optional[str], ignore_categories: Set[str], interval: int,
                concurrent_slots: int) -> Race:
    """
    Creates the race and parses the necessary data
    """
    categories: Dict[str, Category] = load_entries(oris_id, ignore_categories)
    if course_definition_f is not None:
        add_constraints(categories, course_definition_f)
    else:
        add_oris_constraints(categories)

    if specific_time_req_f:
        load_time_requests(categories, specific_time_req_f)

    if same_start_req_f:
        load_same_start_requests(categories, same_start_req_f)

    return Race("race_name", "id", categories, interval, concurrent_slots)


def schedule_categories(oris_id: int, course_definition_f: Optional[str], same_start_req_f: Optional[str],
                        specific_time_req_f: Optional[str], ignore_categories: Set[str], interval: int,
                        concurrent_slots: int, generation: int, initial_population: int):
    """
    Entry function, creates the race and tries to find the best schedule for that race, then prints the results
    and saves them to files.
    """
    race = create_race(oris_id, course_definition_f, same_start_req_f, specific_time_req_f, ignore_categories,
                       interval, concurrent_slots)
    best_json, best_pretty, best_phenom = best_schedule(race, generation, initial_population)
    print(best_pretty)
    with open("solution_" + str(oris_id), "w") as file:
        json.dump(best_json, file)
    with open("solution_graphic_" + str(oris_id), "w") as file:
        file.write(best_pretty)
    return best_json, best_pretty, best_phenom


def best_schedule(race: Race, generation: int, initial_population: int) -> Tuple[dict, str, RacePhenom]:
    """
    Tries to find the best schedule for the given race
    """
    population = create_population(race, initial_population)
    best_genome = ga_pipeline(population, max_generation=generation)
    best_phenom = RaceDecoder(race).decode(best_genome)
    return best_phenom.json(), str(best_phenom), best_phenom
