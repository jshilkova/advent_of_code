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
            universe.append([*line.strip()])
    return universe


def expand_universe(universe, times):
    n = len(universe)
    m = len(universe[0])
    for col in range(0, m):
        has_stars = False
        for line in universe:
            if line[col] == '#':
                has_stars = True
                break
        if not has_stars:
            for i in range(0, n):
                universe[i][col] = times
    for i in range(0, n):
        if '#' not in universe[i]:
            universe[i] = [times]*m
    return universe


def collect_stars(expanded_universe):
    stars = []
    for i in range(0, len(expanded_universe)):
        for j in range(0, len(expanded_universe[0])):
            if expanded_universe[i][j] == '#':
                stars.append([i, j])
    return stars


def find_distance(universe, star1, star2, times):
    distance = 0
    start_i = min(star1[0]+1, star2[0]+1)
    end_i = start_i + abs(star1[0] - star2[0])
    for i in range(start_i, end_i):
        if universe[i][star1[1]] == times:
            distance += times
        else:
            distance += 1
    start_j = min(star1[1]+1, star2[1]+1)
    end_j = start_j + abs(star1[1] - star2[1])
    for j in range(start_j, end_j):
        if universe[star1[0]][j] == times:
            distance += times
        else:
            distance += 1
    return distance


def main():
    universe = get_universe()
    times = 1000000
    universe = expand_universe(universe, times)

    stars = collect_stars(universe)
    distances = [find_distance(universe, star1, star2, times) for idx, star1 in enumerate(stars) for star2 in stars[idx + 1:]]
    final_number = reduce(lambda a, b: a + b, distances)

    print(final_number)


if __name__ == "__main__":
    main()
