from typing import Dict

from source.data_parsing.oris_client import OrisClient
from source.resources import Category


def load_entries(oris_race_id: int, ignore_categories: list[str] = None) -> Dict[str, Category]:
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
        category = Category(name, entries_count)
        categories[name] = category

    return categories
