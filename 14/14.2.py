import argparse
import copy
from pathlib import Path


def get_field():
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()

    with Path(args.path).open() as f:
        field = list(map(lambda x: list(x), f.read().split('\n')))
    return field


def roll_stones_north(field):
    n = len(field)
    m = len(field[0])
    round_stones_count = count_round_stones_vert(field, m, n)

    for j in range(0, m):
        i = 0
        for num in round_stones_count[j]:
            for x in range(num):
                field[i][j] = 'O'
                i += 1

            while i < n and field[i][j] != '#':
                field[i][j] = '.'
                i += 1
            if i < n and field[i][j] == '#':
                i += 1
    return field


def count_round_stones_vert(field, m, n):
    round_stones_count = [[] for _j in range(m)]
    for j in range(0, m):
        r = 0
        for i in range(0, n):
            if field[i][j] == 'O':
                r += 1
            if field[i][j] == '#':
                round_stones_count[j].append(r)
                r = 0
        round_stones_count[j].append(r)
    return round_stones_count


def make_cycle(field):
    for i in range(4):
        roll_stones_north(field)
        field = field[::-1]
        field = [list(x) for x in zip(*field)]
    return field


def main():
    field = get_field()

    seen = [copy.deepcopy(field)]

    i = 1
    while i < 1000000000:
        field = make_cycle(field)
        if field in seen:
            break
        else:
            seen.append(copy.deepcopy(field))
        i += 1
    first_occurance = seen.index(field)
    print(first_occurance, i)
    field = seen[first_occurance + (1000000000 - first_occurance) % (i - first_occurance)]

    final_number = 0
    for i in range(0, len(field)):
        final_number += field[i].count('O') * (len(field) - i)
    print(final_number)


if __name__ == "__main__":
    main()
