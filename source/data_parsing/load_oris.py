import math
from datetime import datetime
from typing import Dict, Tuple, Set, List

from source.data_parsing.oris_client import OrisClient
from source.resources import Category


def load_entries(oris_race_id: int, ignore_categories: Set[str] = None) -> Dict[str, Category]:
    oris = OrisClient()
    data = oris.get(method="getEvent", id=oris_race_id)

    if data["Status"] != 'OK':
        raise Exception()
    categories_data = data['Data']['Classes']

    categories = dict()

    for category_key in categories_data:
        name = categories_data[category_key]['Name']
        if name in ignore_categories:
            continue
        entries_count = int(categories_data[category_key]['CurrentEntriesCount'])
        category = Category(name, entries_count, categories_data[category_key]['ID'])
        categories[name] = category

    return categories


def load_controls(category: Category):
    oris = OrisClient()
    control_codes = list()

    data = oris.get(method="getSplits", classid=category.id)
    if 'Controls' not in data['Data']:
        return []
    
    controls = data['Data']['Controls']
    for control in controls:
        control_codes.append(controls[control]['ControlCode'])

    return control_codes


def load_interval(data) -> int:
    data_keys = list(data.keys())

    entry1 = data[data_keys.pop(0)]
    entry2 = data[data_keys.pop(0)]

    while entry1['ClassDesc'] != entry2['ClassDesc'] or \
        datetime.strptime(entry1['StartTime'], "%Y-%m-%d %H:%M:%S") == \
            datetime.strptime(entry2['StartTime'], "%Y-%m-%d %H:%M:%S"):
        entry1 = entry2
        entry2 = data[data_keys.pop(0)]

    start1 = datetime.strptime(entry1['StartTime'], "%Y-%m-%d %H:%M:%S")
    start2 = datetime.strptime(entry2['StartTime'], "%Y-%m-%d %H:%M:%S")

    return int((start2.timestamp() - start1.timestamp()) / 60)


def load_ignored_categories(oris_race_id) -> Set[str]:
    oris = OrisClient()
    data = oris.get(method="getEventStartLists", eventid=oris_race_id)['Data']
    if data == []:
        raise InvalidDataException()

    data_keys = list(data.keys())
    categories_start_times: Dict[Set[str]] = dict()
    ignored_categories = set()

    for key in data_keys:
        category = data[key]['ClassDesc']
        if category in ignored_categories:
            continue

        start_time = datetime.strptime(data[key]['StartTime'], "%Y-%m-%d %H:%M:%S").timestamp()

        if category not in categories_start_times:
            categories_start_times[category] = {start_time}
        elif start_time in categories_start_times[category]:
            ignored_categories.add(category)

        categories_start_times[category].add(start_time)
    return ignored_categories


def load_concurrent_categories(data, ignored_categories: Set[str], interval: int) -> list[int]:
    data_keys = list(data.keys())
    concurrent: Dict[int, Dict[int, int]] = dict()
    max_concurrent = list()

    for key in data_keys:
        if data[key]['ClassDesc'] in ignored_categories:
            continue
        start_time: int = int(datetime.strptime(data[key]['StartTime'], "%Y-%m-%d %H:%M:%S").timestamp())
        offset: int = int(datetime.strptime(data[key]['StartTime'], "%Y-%m-%d %H:%M:%S").timestamp() % (60 * interval))

        if offset not in concurrent:
            concurrent[offset] = {start_time: 1}
        elif start_time not in concurrent[offset]:
            concurrent[offset][start_time] = 1
        else:
            concurrent[offset][start_time] += 1

    for offset in concurrent:
        max_concurrent.append(max(concurrent[offset].values()))

    return max_concurrent


def load_last_start(data) -> int:
    times = math.inf, 0

    for key in data:
        start_time = datetime.strptime(data[key]['StartTime'], "%Y-%m-%d %H:%M:%S").timestamp()
        times = min(times[0], start_time), max(times[1], start_time)

    return int((times[1] - times[0]) / 60)


class InvalidDataException(Exception):
    pass


def load_metadata(oris_race_id, ignored_categories: Set[str]) -> tuple[int, list[int], float, int, int]:
    oris = OrisClient()
    data = oris.get(method="getEventStartLists", eventid=oris_race_id)['Data']
    if data == []:
        raise InvalidDataException()

    interval = load_interval(data)
    if interval == 0:
        raise InvalidDataException()

    concurrent = load_concurrent_categories(data, ignored_categories, interval)
    concurent_avg = sum(concurrent) / interval
    last_start = load_last_start(data)
    entries = sum(1 for key in data if data[key]['ClassDesc'] not in ignored_categories)
    efficiency = entries / (last_start * concurent_avg)

    return interval, concurrent, efficiency, last_start, entries


def load_ids(date_from, date_to, level="4", sport="1", ):
    oris = OrisClient()
    data = oris.get(method="getEventList", datefrom=date_from, dateto=date_to, level=level, sport=sport)['Data']
    ids = list()
    for key in data:
        ids.append(int(data[key]['ID']))

    return ids


