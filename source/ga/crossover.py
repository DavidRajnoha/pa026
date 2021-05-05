from typing import List, Any, Set, Tuple, Iterator

from leap_ec.individual import Individual


def crossover_permutation(next_individual: Iterator) -> Iterator:
    while True:
        parent1: Individual = next(next_individual)
        parent2: Individual = next(next_individual)

        genome_offspring1, genome_offspring2 = order_crossover(parent1.genome, parent2.genome)
        yield Individual(genome_offspring1, decoder=parent1.decoder, problem=parent1.problem)
        yield Individual(genome_offspring2, decoder=parent1.decoder, problem=parent1.problem)


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
