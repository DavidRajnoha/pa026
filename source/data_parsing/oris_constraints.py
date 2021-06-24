from source.data_parsing.load_oris import load_controls
from source.data_parsing.load_route_constraints import same_first_constraints
from source.resources import Category


def add_oris_constraints(categories) -> None:
    categories_by_first = dict()
    categories_by_route = dict()
    for category in categories:
        controls = load_controls(categories[category])
        if len(controls) == 0:
            continue

        fc = controls[0]
        if fc not in categories_by_first:
            categories_by_first[fc] = list()
        categories_by_first[fc].append(categories[category].name)

        c_str = str(controls)
        if c_str not in categories_by_route:
            categories_by_route[c_str] = list()
        categories_by_route[c_str].append(categories[category].name)

    same_route_constraints(categories_by_route, categories)
    same_first_constraints(categories_by_first, categories)


def same_route_constraints(categories_by_route: dict[str, list[str]], race_categories: dict[str, Category]) -> None:
    for first in categories_by_route:
        category_keys = categories_by_route[first]
        for category_key in category_keys:
            if category_key not in race_categories:
                continue
            category = race_categories[category_key]
            for constr_category_key in category_keys:
                if constr_category_key not in race_categories:
                    continue
                if category_key == constr_category_key:
                    continue
                category_constr = race_categories[constr_category_key]
                category.add_same_route_constraint(category_constr)

