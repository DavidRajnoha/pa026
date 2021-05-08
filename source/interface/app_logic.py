import json
from typing import List, Dict, Tuple

from source.data_parsing.load_entries import load_entries
from source.data_parsing.load_route_constraints import add_constraints
from source.data_parsing.load_soft_constraints import load_time_requests, load_same_start_requests
from source.ga.population import create_population
from source.resources import Race, Category
from source.ga.pipeline import ga_pipeline
from source.ga.resources import RaceDecoder


def create_race(oris_id: int, course_definition_f: str, same_start_req_f: str,
                specific_time_req_f, ignore_categories: List[str], interval: int,
                concurrent_slots: int) -> Race:
    categories: Dict[str, Category] = load_entries(oris_id, ignore_categories)
    add_constraints(categories, course_definition_f)
    load_time_requests(categories, specific_time_req_f)
    load_same_start_requests(categories, same_start_req_f)

    return Race("race_name", "id", categories, interval, concurrent_slots)


def schedule_categories(oris_id: int, course_definition_f: str, same_start_req_f: str,
                        specific_time_req_f, ignore_categories: List[str], interval: int,
                        concurrent_slots: int, generation: int, initial_population: int):
    race = create_race(oris_id, course_definition_f, same_start_req_f, specific_time_req_f, ignore_categories,
                       interval, concurrent_slots)
    best_json, best_pretty = best_schedule(race, generation, initial_population)
    print(best_pretty)
    with open("solution", "w") as file:
        json.dump(best_json, file)
    with open("solution_graphic", "w") as file:
        file.write(best_pretty)


def best_schedule(race: Race, generation: int, initial_population: int) -> Tuple[dict, str]:
    population = create_population(race, initial_population)
    best_genome = ga_pipeline(population, max_generation=generation)
    best_phenom = RaceDecoder(race).decode(best_genome)
    return best_phenom.json(), str(best_phenom)
