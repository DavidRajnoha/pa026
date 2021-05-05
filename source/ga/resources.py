import copy
from typing import List, Tuple, Set, Dict
from queue import PriorityQueue

from leap_ec.problem import Problem
from leap_ec.decoder import Decoder
from source.resources import Race, Slot, Category, PrioritizedSlot


class RacePhenom:
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


def slots_overlapping(slots: List[Slot]) -> Set[frozenset]:
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
            # TODO: investigate the problem with the second condition
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
            slots_overlapping(slots_same_offset)
        first_constrained = first_constrained.union(constrained_offset)

    return first_constrained


def construct_same_route_constrained(phenom: RacePhenom) -> Set[frozenset]:
    """
    """
    return slots_overlapping(phenom.slots)


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
        hard_constraints_score = self.evaluate_hard_constraints(phenom) * 100
        # time_score = 0
        time_score = (1 - phenom.efficiency()) * 100
        soft_constraints_score = 0
        return int(hard_constraints_score + time_score + soft_constraints_score)

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

            # same route is stricter than same first TODO: Maybe do this difference somewhere else
            same_first_categories = set(self.race.categories[category].same_first_constraint)\
                .difference(same_route_categories)

            for same_first_category in same_first_categories:
                if frozenset({self.race.categories[category],
                              same_first_category}) in same_first_constrained:
                    same_first_constrained_count += 1

        return same_route_constrained_count + same_first_constrained_count

    def worse_than(self, first_fitness: int, second_fitness: int) -> bool:
        return first_fitness >= second_fitness

    def equivalent(self, first_fitness, second_fitness):
        return first_fitness == second_fitness


class RaceDecoder(Decoder):

    def __init__(self, race: Race):
        self.race: Race = race

    def decode(self, genome: List, *args, **kwargs) -> RacePhenom:
        phenom = RacePhenom(copy.deepcopy(self.race.slots))
        slots_iter = iter(phenom.slots)
        slot = slots_iter.__next__()

        for chromosome in genome:
            if isinstance(chromosome, int):
                slot = slots_iter.__next__()
            elif isinstance(chromosome, Category):
                # TODO: Change to category name and lookup in dict, possible numpy usage
                slot.append(category=chromosome)

        return phenom
