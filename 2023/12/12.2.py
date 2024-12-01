import argparse
from pathlib import Path


def get_springs_working_map():
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()
    springs = []
    damaged = []

    with Path(args.path).open() as f:
        for line in f:
            s, w = line.split(' ')
            springs.append('?'.join([s] * 5))
            damaged.append(tuple(map(int, w.strip().split(','))) * 5)
    return springs, damaged


known = {}


def count(springs, damaged):
    key = (springs, damaged)

    if key in known:
        return known[key]

    if len(springs) == 0:
        return 1 if len(damaged) == 0 else 0

    if len(damaged) == 0:
        return 0 if '#' in springs else 1

    result = 0

    if springs[0] in '.?':
        result += count(springs[1:], damaged)
    if (springs[0] in '#?' and '.' not in springs[:damaged[0]]
               and (len(springs) == damaged[0] or (len(springs) > damaged[0] and springs[damaged[0]] != '#'))):
        result += count(springs[damaged[0] + 1:], damaged[1:])

    known[key] = result
    return result


def main():
    springs, damaged = get_springs_working_map()
    final_number = 0

    for i in range(0, len(springs)):
        final_number += count(springs[i], damaged[i])
        print(i, final_number)

    print(final_number)


if __name__ == "__main__":
    main()
