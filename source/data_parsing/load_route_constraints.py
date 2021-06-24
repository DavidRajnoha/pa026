from source.resources import Category


def add_constraints(race_categories: dict[str, Category], filename: str):
    """
    Adds the constraints specified in the passed file to the passed categories
    """
    categories_by_first: dict[str, list[str]] = dict()
    with open(filename) as file:
        lines = file.readlines()
        for line in lines:
            line.replace("\t", " ")
            categories = line.split(", ")
            last = categories.pop()
            category, controls = last.split(maxsplit=2)
            controls = controls.split("-")
            categories.append(category)

            same_route_constraints(categories, race_categories)

            controls.pop(0)

            for category_key in categories:
                if controls[0] not in categories_by_first:
                    categories_by_first[controls[0]] = list()
                categories_by_first[controls[0]].append(category_key)

    same_first_constraints(categories_by_first, race_categories)


def same_first_constraints(categories_by_first: dict[str, list[str]], race_categories: dict[str, Category]):
    """
    Identifies the categories starting with the same first control
    """
    for first in categories_by_first:
        category_keys = categories_by_first[first]
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
                category.add_same_first_constraint(category_constr)


def same_route_constraints(category_keys: list[str], race_categories: dict[str, Category]) -> None:
    """
    Identifies the categories with the same route
    """
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
