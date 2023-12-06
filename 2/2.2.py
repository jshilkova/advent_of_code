import argparse
from pathlib import Path


def get_minimal_cubes_set_power(line):
    subsets = line[line.index(':') + 2:].split(';')
    min_cubes_set = {"red": 1, "green": 1, "blue": 1}
    for subset in subsets:
        subset_color_numbers = get_color_numbers(subset)
        for color, number in subset_color_numbers.items():
            if subset_color_numbers[color] > min_cubes_set[color]:
                min_cubes_set[color] = number
    return min_cubes_set['red'] * min_cubes_set['green'] * min_cubes_set['blue']


def get_color_numbers(cubes_subset):
    color_number = {"red": 0, "green": 0, "blue": 0}
    colored_cubes = cubes_subset.split(',')
    for colored_pile in colored_cubes:
        number, color = colored_pile.strip().split(' ')
        color_number[color] = int(number)
    return color_number


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()

    final_number = 0

    with Path(args.path).open() as lines:
        for line in lines:
            final_number += get_minimal_cubes_set_power(line)

    print(final_number)


if __name__ == "__main__":
    main()
