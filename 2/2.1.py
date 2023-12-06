import argparse
from pathlib import Path

initial_cubes_set = {"red": 12, "green": 13, "blue": 14}


def possible_game(line):
    colon_index = line.index(':')
    game_number = line[5:line.index(':')]
    game = line[colon_index + 2:]
    subsets = game.split(';')
    possible = True
    for subset in subsets:
        if not is_possible_set(subset.strip(), initial_cubes_set):
            possible = False
            return 0
    return int(game_number)


def is_possible_set(cubes_subset, cubes):
    possible = True
    colored_cubes = cubes_subset.split(',')
    for colored_pile in colored_cubes:
        number, color = colored_pile.strip().split(' ')
        if int(number) > cubes[color]:
            possible = False
    return possible


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()

    final_number = 0

    with Path(args.path).open() as lines:
        for line in lines:
            final_number += possible_game(line)

    print(final_number)


if __name__ == "__main__":
    main()
