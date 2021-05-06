from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Iterator, Optional


class Category:
    """
    Representation of the category.
    Contains the number of entries and the information related to the
    constraints on this category.
    """
    def __init__(self, name: str, num_entries: int):
        self.name: str = name
        self.first_start_time: int = 0
        self.num_entries: int = num_entries
        self._same_first_constraint: List[Category] = list()
        self._same_route_constraint: List[Category] = list()
        self._same_time_request: List[Tuple[Category]] = list()
        self._distant_time_request: List[Tuple[Category, int]] = list()
        self._specific_time_request: List[int] = list()

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.name == other.name

    @property
    def same_first_constraint(self) -> List:
        """
        List of categories with the same first control - can not start concurrently in the same offset
        """
        return self._same_first_constraint
    
    def add_same_first_constraint(self, category):
        self._same_first_constraint.append(category)

    @property
    def same_route_constraint(self) -> List:
        """
        List of categories with the same route - the starts can not overlap (even with different offsets)
        """
        return self._same_route_constraint

    def add_same_route_constraint(self, category):
        self._same_route_constraint.append(category)
        
    @property
    def same_time_request(self) -> List:
        """
        List of categories that would like to start concurrently with this category
        """
        return self._same_time_request

    def add_same_time_request(self, category):
        self._same_time_request.append(category)

    @property
    def distant_time_request(self) -> List:
        """
        List of categories that would like to start separately from this category - currently not used in evaluation
        """
        return self._distant_time_request

    def add_distant_time_request(self, category):
        self._distant_time_request.append(category)

    @property
    def specific_time_request(self) -> List:
        """
        List of starting times that this category would like to cover
        """
        return self._specific_time_request

    def add_specific_time_request(self, time: int):
        self._specific_time_request.append(time)


class Slot:
    """
    Representation of a starting slot that contains multiple categories.
    Works as iterator, can provide the next category in the slot in the correct order.
    """
    def __init__(self, offset: int, interval: int, categories: List[Category]):
        self.offset: int = offset
        self.interval: int = interval
        self.categories: List[Category] = categories
        # if this failed, the initiation of entries count will have to be different
        assert len(self.categories) == 0
        self.entries_count: int = 0

        # for the construction of clashes can be iterated through, this iterator returns the next category
        self._category_iterator: Optional[Iterator] = None
        # the category that is right now under iteration
        self.category = None
        self.prev_category = None
        # the start time of self.category
        self.iter_time = None

    def iter_next_categories(self):
        """
        Initiates the iteration
        """
        self._category_iterator = self.categories.__iter__()
        self.iter_time = self.offset
        try:
            self.category = self._category_iterator.__next__()
        except StopIteration:
            self.category = None
        self.prev_category = None

    def next_category(self):
        """
        Provides the next category in the correct order
        """
        self.iter_time += self.category.num_entries * self.interval
        self.prev_category = self.category
        try:
            self.category = self._category_iterator.__next__()
        except StopIteration:
            self.category = None

    def length(self):
        """
        Returns the total length of the slot
        """
        slot_length = self.offset
        for category in self.categories:
            slot_length += category.num_entries * self.interval
        return slot_length

    def length_better(self):
        """
        Returns the total length of the slot
        """
        return self.offset + self.entries_count * self.interval

    def append(self, category: Category):
        """
        Adds next category to the slot.
        """
        self.categories.append(category)
        self.entries_count += category.num_entries


@dataclass(order=True)
class PrioritizedSlot:
    """
    Wrapper over Slot with a priority
    """
    priority: int
    slot: Slot = field(compare=False)


class Race:
    """
    Representation of the race
    Contains categories and empty slots, which define the conditions of the problem.
    """
    def __init__(self, name, id, categories, interval, concurrent_slots_limit):
        self.name: str = name
        self.id: str = id
        self.categories: Dict[str, Category] = categories
        self.interval: int = interval
        self.concurrent_slots_limit: int = concurrent_slots_limit

        self.slots: List[Slot] = self._create_slots(concurrent_slots_limit, interval)

    @staticmethod
    def _create_slots(concurrent_slots_limit, interval) -> List[Slot]:
        slots: List[Slot] = list()
        for minute in range(interval):
            for index in range(concurrent_slots_limit):
                slots.append(Slot(offset=minute, interval=interval, categories=list()))
        return slots
