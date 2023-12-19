import argparse
from pathlib import Path


def get_field():
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()

    with Path(args.path).open() as f:
        field = f.read().split('\n')
    return field


def roll_stones(field):
    n = len(field)
    m = len(field[0])
    round_stones_count = [[] for j in range(m)]
    print(round_stones_count)
    for j in range(0, m):
        r = 0
        for i in range(0, n):
            if field[i][j] == 'O':
                r += 1
            if field[i][j] == '#':
                round_stones_count[j].append(r)
                r = 0
        round_stones_count[j].append(r)

    res = [['.' for _i in range(m)] for i in range(n)]
    for j in range(0, m):
        i = 0
        for num in round_stones_count[j]:
            for x in range(num):
                res[i][j] = 'O'
                i += 1

            while i < n and field[i][j] != '#':
                i += 1
            i += 1

    return res


def main():
    field = get_field()
    rolled = roll_stones(field)
    for line in rolled:
        print(line)
    final_number = 0
    for i in range(0, len(field)):
        final_number += rolled[i].count('O') * (len(field) - i)
    print(final_number)


if __name__ == "__main__":
    main()
