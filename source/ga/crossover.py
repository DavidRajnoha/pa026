from typing import List, Any, Set, Tuple, Iterator

from leap_ec.individual import Individual


def crossover_permutation(next_individual: Iterator) -> Iterator:
    while True:
        parent1: Individual = next(next_individual)
        parent2: Individual = next(next_individual)

        genome_offspring1, genome_offspring2 = crossover_genome_permutation(parent1.genome, parent2.genome)
        yield Individual(genome_offspring1, decoder=parent1.decoder, problem=parent1.problem)
        yield Individual(genome_offspring2, decoder=parent1.decoder, problem=parent1.problem)


def crossover_genome_permutation(genome_fst: List, genome_snd: List):
    g_categories_fst, g_slots_fst = separate_genome(genome_fst)
    g_categories_snd, g_slots_snd = separate_genome(genome_snd)

    g_cat_offspring_fst, g_cat_offspring_snd = order_crossover(g_categories_fst, g_categories_snd)

    return merge_genome(g_cat_offspring_fst, g_slots_fst), \
        merge_genome(g_cat_offspring_snd, g_slots_snd)


def order_crossover(g_fst: List[Any], g_snd: List[Any]) -> Tuple[List[Any], List[Any]]:
    g_offspring_fst = [0 for _ in g_fst]
    g_offspring_snd = [0 for _ in g_fst]

    cycles = get_cycles(g_fst, g_snd)

    parent_to_child = True

    for cycle in cycles:
        for position in cycle:
            if parent_to_child:
                g_offspring_fst[position] = g_fst[position]
                g_offspring_snd[position] = g_snd[position]
            else:
                g_offspring_fst[position] = g_snd[position]
                g_offspring_snd[position] = g_fst[position]
        parent_to_child = not parent_to_child

    return g_offspring_fst, g_offspring_snd


def get_cycles(g_fst: List[Any], g_snd: List[Any]) -> List[List[int]]:
    in_cycle: Set[int] = set()
    cycles: List[List[int]] = list()
    for index, elem in enumerate(g_fst):
        if index in in_cycle:
            continue
        cycle: List[int] = list()
        cycle.append(index)
        in_cycle.add(index)

        next_index = g_fst.index(g_snd[index])

        while g_fst[next_index] != elem:
            cycle.append(next_index)
            in_cycle.add(next_index)
            next_index = g_fst.index(g_snd[next_index])

        cycles.append(cycle)

    return cycles


def separate_genome(genome: List) -> Tuple[List, List]:
    counter = 0
    g_categories: List[str] = list()
    g_slots: List[int] = list()
    for chromosome in genome:
        if chromosome == "|":
            g_slots.append(counter)
        else:
            g_categories.append(chromosome)
        counter += 1

    return g_categories, g_slots


def merge_genome(g_categories: List[str], g_slots: List[int]) -> List:
    """
    TODO: Beware of returning the string from input and modifying the input
    :param g_categories:
    :param g_slots:
    :return:
    """
    for slot_position in g_slots:
        g_categories.insert(slot_position, "|")
    return g_categories
