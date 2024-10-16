entire_universe = set(range(1, 101))

# Divisor sets
div_by_2 = set(range(2, 101, 2))
div_by_3 = set(range(3, 101, 3))
div_by_5 = set(range(5, 101, 5))
div_by_7 = set(range(7, 101, 7))
divisor_universes = [div_by_2, div_by_3, div_by_5, div_by_7]

possible_current_states = {1}

while True:
    # TODO: get these from the nc. 
    # num_moves is how many pushes or pops were made
    # parity vector is four digits for 2, 3, 5, 7, where 1 means state is divisible by that number
    num_moves = int(input('Input number of moves: ')) 
    parity_vector = input('Input parity vector: ')

    range_sets = [set(range(state - num_moves, state + num_moves + 1)) for state in possible_current_states]
    in_range_set = set.union(*range_sets)

    all_sets = [entire_universe, in_range_set]

    for i, divisor_universe in enumerate(divisor_universes):
        parity_set = divisor_universe if int(parity_vector[i]) else entire_universe.difference(divisor_universe)
        all_sets.append(parity_set)

    possible_current_states = set.intersection(*all_sets)
    print(possible_current_states)
