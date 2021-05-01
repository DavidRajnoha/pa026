from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Iterator, Optional


class Category:
    def __init__(self, name: str, num_entries: int):
        self.name: str = name
        self.start_time: int  # will be determined by the result of the ga, can be possibly omitted
        self.num_entries: int = num_entries
        self._same_first_constraint: List[Category] = list()
        self._same_route_constraint: List[Category] = list()
        self._same_time_request: List[Tuple[Category, int]] = list()
        self._distant_time_request: List[Tuple[Category, int]] = list()
        self._specific_time_request: List[int] = list()

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.name == other.name

    @property
    def same_first_constraint(self) -> List:
        return self._same_first_constraint
    
    def add_same_first_constraint(self, category):
        self._same_first_constraint.append(category)

    @property
    def same_route_constraint(self) -> List:
        return self._same_route_constraint

    def add_same_route_constraint(self, category):
        self._same_route_constraint.append(category)
        
    @property
    def same_time_request(self) -> List:
        return self._same_time_request

    def add_same_time_request(self, category):
        self._same_time_request.append(category)

    @property
    def distant_time_request(self) -> List:
        return self._distant_time_request

    def add_distant_time_request(self, category):
        self._distant_time_request.append(category)

    @property
    def specific_time_request(self) -> List:
        return self._specific_time_request

    def add_specific_time_request(self, category):
        self._specific_time_request.append(category)


class Slot:
    def __init__(self, offset, interval, categories):
        self.offset: int = offset
        self.interval: int = interval
        self.categories: List[Category] = categories

        # for the construction of clashes can be iterated through, this iterator returns the next category
        self._category_iterator: Optional[Iterator] = None
        # the category that is right now under iteration
        self.category = None
        self.prev_category = None
        # the start time of self.category
        self.iter_time = None

    def iter_next_categories(self):
        self._category_iterator = self.categories.__iter__()
        self.iter_time = self.offset
        try:
            self.category = self._category_iterator.__next__()
        except StopIteration:
            self.category = None
        self.prev_category = None

    def next_category(self):
        self.iter_time += self.category.num_entries * self.interval
        self.prev_category = self.category
        try:
            self.category = self._category_iterator.__next__()
        except StopIteration:
            self.category = None

    def length(self):
        slot_length = self.offset
        for category in self.categories:
            slot_length += category.num_entries * self.interval
        return slot_length

    def append(self, category: Category):
        self.categories.append(category)


@dataclass(order=True)
class PrioritizedSlot:
    priority: int
    slot: Slot = field(compare=False)


class Race:
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
