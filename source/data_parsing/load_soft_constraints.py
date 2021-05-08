from source.resources import Category


def load_time_requests(race_categories: dict[str, Category], filename: str):
    with open(filename) as file:
        lines = file.readlines()
        for line in lines:
            tokens = line.split()
            category_key = tokens[0]
            if category_key not in race_categories:
                continue

            requested_times = tokens[1:]
            requested_times = map(int, requested_times)

            for time in requested_times:
                race_categories[category_key].add_specific_time_request(time)


def load_same_start_requests(race_categories: dict[str, Category], filename: str):
    with open(filename) as file:
        lines = file.readlines()
        for line in lines:
            tokens = line.split()
            category_fst = tokens[0]
            category_snd = tokens[1]
            if category_fst not in race_categories or category_snd not in race_categories:
                continue

            race_categories[category_fst].add_same_time_request(race_categories[category_snd])
            race_categories[category_snd].add_same_time_request(race_categories[category_fst])
