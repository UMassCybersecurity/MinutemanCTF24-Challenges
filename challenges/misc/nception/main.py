import sys
import numpy as np
from random import shuffle
from story import *
from flag import FLAG

testing = True

if not testing:
    print(description)

    if input('Are you ready to start? [y/N]\n') != 'y':
        sys.exit(0)
    print('\n')

# Game setup
shuffle(floors)
current_floor = 1  # What floor are they currently on
num_failures = 0   # How many times as the player guessed incorrectly
max_failures = 5   # What is the max number of wrong guesses before users is kicked
passed_check = 0   # Did they get their previous guess correct?
num_floors = 100   # How many floors are there?

def check_tops(floor_num: int):
    tops = np.array([floor_num % 2, floor_num % 3, floor_num % 5, floor_num % 7]) == 0

    top_numbers = {0: "2", 1: "3", 2: "5", 3: "7"}
    true_tops = [top_numbers[i] for i, value in enumerate(tops) if value]
    false_tops = [top_numbers[i] for i, value in enumerate(tops) if not value]

    def format_tops(tops_list, status):
        if not tops_list:
            return f"No top is {status}"
        elif len(tops_list) == 1:
            return f"Top {tops_list[0]} is {status}"
        else:
            return f"Tops {', '.join(tops_list[:-1])} and {tops_list[-1]} are {status}"

    print(format_tops(true_tops, "spinning indefinitely"))
    print(format_tops(false_tops, "stationary"))
    

def push_or_pop(floor_num: int):
    if floor_num == 1:
        return (1, 'push')
    if floor_num == num_floors:
        return (-1, 'pop')
    
    k = floor_num / num_floors
    prob = 0.7 * (1 - k) + 0.3 * k
    change = np.random.choice([1, -1], p=[prob, 1 - prob])
    outcome = 'push' if change == 1 else 'pop'

    return change, outcome


def get_description(floor_num: int):
    if floor_num == 1: 
        return first_floor
    if floor_num == num_floors:
        return last_floor
    return floors[floor_num-2]
    

while num_failures < max_failures:
    num_events = np.random.randint(5, 7)
    for _ in range(num_events):
        num_moves = np.random.choice([1, 2, 3, 4, 5], p=[0.50, 0.25, 0.15, 0.05, 0.05])

        for _ in range(num_moves):
            change, outcome = push_or_pop(current_floor)
            current_floor += change

            if testing:
                print(change, outcome)

        person = np.random.choice(['Achilles', 'the Tortoise'])
        if num_moves == 1:
            print(f'Inception: {person} picked out one {outcome}')
        else:
            print(f'Inception: {person} picked out {num_moves} pushes and tops')
        print(get_description(current_floor))
        check_tops(current_floor)
        print()

    if testing:
        print(current_floor)

    guess = int(input(f'Hofstadter booms down: what is the current floor? [1-{num_floors}]\n'))
    if guess < 1 or guess > num_floors:
        print('That guess is invalid. Try again next time')
        sys.exit(0)

    wrong = guess != current_floor

    if wrong:
        num_failures += 1
        passed_check = 0
        print(f'Your guess was wrong, the correct floor was {current_floor}. You have {max_failures - num_failures} guesses left.')
    elif passed_check:
        print(f"\n\nYou win, here's your flag: {FLAG}")
        break
    else:
        print('Your guess was correct.\n')
        passed_check = 1

print('Hofstadter declares with finality: you are out of guesses. Achilles and the Tortoise are mine for eternity! (reconnect to play again)')