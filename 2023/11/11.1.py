import argparse
from functools import reduce
from pathlib import Path


def get_universe():
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()
    universe = []

    with Path(args.path).open() as f:
        for line in f:
            universe.append(line.strip())
    return universe


def expand_universe(universe):
    n = len(universe)
    m = len(universe[0])
    expanded_universe = [''] * n
    for col in range(0, m):
        has_stars = False
        for line in universe:
            if line[col] == '#':
                has_stars = True
                break
        if has_stars:
            for i in range(0, n):
                expanded_universe[i] += universe[i][col]
        else:
            for i in range(0, n):
                expanded_universe[i] += '..'
    i = 0
    for row in universe:
        if '#' not in row:
            expanded_universe.insert(i, '.' * len(expanded_universe[0]))
            i += 1
        i += 1
    return expanded_universe


def collect_stars(expanded_universe):
    stars = []
    for i in range(0, len(expanded_universe)):
        for j in range(0, len(expanded_universe[0])):
            if expanded_universe[i][j] == '#':
                stars.append([i, j])
    return stars


def find_distance(star1, star2):
    return abs(star1[0]-star2[0]) + abs(star1[1]-star2[1])


def main():
    universe = get_universe()
    universe = expand_universe(universe)
    stars = collect_stars(universe)
    distances = [find_distance(star1, star2) for idx, star1 in enumerate(stars) for star2 in stars[idx + 1:]]
    final_number = reduce(lambda a, b: a + b, distances)

    # for line in universe:
    #     print(line)
    # print(stars)
    print(distances)
    print(final_number)


if __name__ == "__main__":
    main()
