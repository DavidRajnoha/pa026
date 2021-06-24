"""
The implementation of the Phenom, Problem and Decoder classes defined by the LEAP library
"""

import copy
import json
from typing import List, Set, Dict
from queue import PriorityQueue

from leap_ec.problem import Problem
from leap_ec.decoder import Decoder
from source.resources import Race, Slot, Category, PrioritizedSlot


class RacePhenom:
    """
    Representation of the particular solution.
    Contains a list of slots with appended categories.
    The slots with their offsets and categories are the solution to the problem)
    Also provides statistics about the time optimality of the solution.
    """
    def __init__(self, slots: List[Slot]):
        self.slots: List[Slot] = slots

    def append_category(self, category):
        """
        Adds category to the last slot
        TODO: is not faster to store the last slot somewhere?
        """
        self.slots.pop().append(category)

    def total_length(self) -> int:
        """
        :return: The length of the longest slot, therefor the duration of the race
        """
        return max(map(lambda slot: slot.length(), self.slots))

    def optimal_time(self) -> int:
        """
        :return: Sum of times when someone is starting
        """
        return sum(map(lambda slot: slot.length(), self.slots))

    def optimal_length(self) -> float:
        return self.optimal_time() / len(self.slots)

    def efficiency(self) -> float:
        return self.optimal_length() / self.total_length()

    def __str__(self):
        string = ""
        for slot in self.slots:
            string += str(slot)
            string += "\n"
        return string

    def json(self) -> dict:
        data = dict()
        for slot in self.slots:
            data |= slot.categories_json()
        return data

    def json_pretty_str(self) -> str:
        return json.dumps(self.json(), indent=4, sort_keys=True)


def categories_start_times_overlapping(slots: List[Slot]) -> Set[frozenset]:
    """
    Constructs a set of sets of size two of categories that have overlapping start times,
    by iterating of the categories based on their start time
    The function should have time complexity O(categories * slots) as it iterates
    through all of the categories, for each adding the forbidden categories and there is slot of them.

    When given slots with the same offset, generates same first constrain, when given all slots,
    generates same route constrained.

    :param slots:
    :return: set of categories contained in the phenom that start in the same time
    """
    same_constrained: Set[frozenset] = set()
    # slots sorted based on the time of the start of the next iterated category
    priority_slots = PriorityQueue()
    # set of all categories that start in current state of priority queue (same categories as in priority quee)
    current_categories = set()

    for slot in slots:
        slot.iter_next_categories()
        if slot.category is None:
            continue

        priority_slots.put(PrioritizedSlot(priority=slot.iter_time,
                                           slot=slot))
        current_categories.add(slot.category)

    while not priority_slots.empty():
        # goes through the categories one after other in the order in which the categories start
        # creates the set of categories that are starting in the same time
        next_slot: Slot = priority_slots.get().slot

        if next_slot.prev_category is not None and next_slot.prev_category in current_categories:
            current_categories.remove(next_slot.prev_category)

        if next_slot.category is None:
            continue

        current_categories.add(next_slot.category)

        for category in current_categories:
            if category == next_slot.category:
                continue
            same_constrained.add(frozenset({next_slot.category, category}))

        next_slot.next_category()
        priority_slots.put(PrioritizedSlot(priority=next_slot.iter_time,
                                           slot=next_slot))

    return same_constrained


def construct_same_first_constrained(phenom: RacePhenom) -> Set[frozenset]:
    """
    Separates the slots by their offset time and then returns a list of
    categories with start time overlapping for each offset.
    """
    slots: List[Slot] = phenom.slots
    slots_by_offset: Dict[int, List[Slot]] = dict()
    for slot in slots:
        if slot.offset not in slots_by_offset:
            slots_by_offset[slot.offset] = list()
        slots_by_offset[slot.offset].append(slot)

    first_constrained: Set[frozenset] = set()

    for offset in slots_by_offset:
        slots_same_offset = slots_by_offset[offset]
        constrained_offset: Set[frozenset] =\
            categories_start_times_overlapping(slots_same_offset)
        first_constrained = first_constrained.union(constrained_offset)

    return first_constrained


def construct_same_route_constrained(phenom: RacePhenom) -> Set[frozenset]:
    """
    Returns a list of categories that can not have the same route, 
    """
    return categories_start_times_overlapping(phenom.slots)


class RaceProblem(Problem):
    """
    Class representing the race problem, main feature being the evaluation function
    """

    def __init__(self, race: Race):
        super().__init__()
        self.race: Race = race

    def evaluate(self, phenom: RacePhenom, *args, **kwargs) -> int:
        """
        Returns the evaluation for the given phenom
        The evaluation is based by the count of route constraints and first constraints
        """
        time_score = (1 - phenom.efficiency()) * 100
        time_req_score = self.evaluate_specific_time(phenom)
        same_start_req_score = self.evaluate_same_start_request(phenom) / 2
        soft_constraints_score = (time_score * 1.5) + time_req_score + same_start_req_score

        hard_constraints_score = self.evaluate_hard_constraints(phenom) * 100

        return int(hard_constraints_score + soft_constraints_score)

    def evaluate_hard_constraints(self, phenom: RacePhenom) -> float:
        """
        Returns the evaluation for the given phenom
        The evaluation is based by the count of route constraints and first constraints
        """
        same_route_constrained = construct_same_route_constrained(phenom)
        same_first_constrained = construct_same_first_constrained(phenom)

        same_route_constrained_count = 0
        same_first_constrained_count = 0
        for category in self.race.categories:
            same_route_categories = self.race.categories[category].same_route_constraint
            for same_route_category in same_route_categories:
                if frozenset({self.race.categories[category],
                              same_route_category}) in same_route_constrained:
                    same_route_constrained_count += 1

            # same route is stricter than same first
            same_first_categories = set(self.race.categories[category].same_first_constraint)\
                .difference(same_route_categories)

            for same_first_category in same_first_categories:
                if frozenset({self.race.categories[category],
                              same_first_category}) in same_first_constrained:
                    same_first_constrained_count += 1

        return same_route_constrained_count + same_first_constrained_count

    def evaluate_same_start_request(self, phenom: RacePhenom) -> int:
        """
        Each category can have a list of categories that should start at the same time.
        This returns the number of such requests that are not fulfilled by the phenom
        :param phenom:
        :return:
        """
        start_times_overlapping = construct_same_route_constrained(phenom)
        unfulfilled_requests = 0

        for category in self.race.categories:
            same_time_requested_categories = self.race.categories[category].same_time_request
            for same_time_requested_category in same_time_requested_categories:
                if frozenset({self.race.categories[category],
                              same_time_requested_category}) not in start_times_overlapping:
                    unfulfilled_requests += 1

        return unfulfilled_requests

    def evaluate_specific_time(self, phenom: RacePhenom) -> int:
        """
        Each category can have a list of times that the starting interval should span.
        Returns a number of how many of these start times are not covered by the real category starting time
        :param phenom:
        :return:
        """
        unfulfilled_requests = 0

        for slot in phenom.slots:
            for category in slot.categories:
                for request in category.specific_time_request:
                    if not category.first_start_time <= request <= \
                           category.first_start_time + category.num_entries * slot.interval:
                        unfulfilled_requests += 1
        return unfulfilled_requests

    def worse_than(self, first_fitness: int, second_fitness: int) -> bool:
        """
        Defines the order on the fitness score
        """
        return first_fitness >= second_fitness

    def equivalent(self, first_fitness, second_fitness):
        """
        Defines the equivalence on the fitness score
        """
        return first_fitness == second_fitness


class RaceDecoder(Decoder):
    """
    Class decoding genome (List of categories and integers) to RacePhenom
    """

    def __init__(self, race: Race):
        self.race: Race = race

    def decode(self, genome: List, *args, **kwargs) -> RacePhenom:
        """
        Takes a genome (list of categories and integers and converts it into phenom)
        Iterates through a genome, adds each category to the active Slot and
        for each separator takes a new slot and sets it as active.
        """
        phenom = RacePhenom(copy.deepcopy(self.race.slots))
        slots_iter = iter(phenom.slots)
        slot = slots_iter.__next__()

        for chromosome in genome:
            if isinstance(chromosome, int):
                slot = slots_iter.__next__()
            elif isinstance(chromosome, Category):
                category: Category = chromosome
                category.first_start_time = slot.length_better()
                slot.append(category)

        return phenom
