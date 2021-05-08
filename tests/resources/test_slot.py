import pytest

from source.resources import Slot, Category


@pytest.fixture(scope="module")
def slot():
    slot = Slot(offset=1, interval=2, categories=[])
    category1 = Category("category1", 5)
    category2 = Category("category2", 5)

    slot.append(category1)
    slot.append(category2)

    return slot


def test_slot():
    slot = Slot(offset=1, interval=2, categories=[])
    category1 = Category("category1", 5)
    category2 = Category("category2", 5)

    slot.append(category1)
    slot.append(category2)

    assert category1 in slot.categories
    assert category2 in slot.categories

    slot.iter_next_categories()
    assert slot.category == category1
    assert slot.iter_time == 1

    slot.next_category()
    assert slot.category == category2
    assert slot.iter_time == 1 + 2 * 5


def test_slot_empty():
    slot = Slot(offset=1, interval=2, categories=[])
    slot.iter_next_categories()
    assert slot.category is None


def test_slot_print(slot):
    print("\n")
    print(slot)


def test_slot_json(slot):
    print("\n")
    print(slot.categories_json())
