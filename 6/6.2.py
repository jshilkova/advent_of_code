import argparse
import math
from pathlib import Path


def get_race():
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()

    with Path(args.path).open() as f:
        time = int(f.readline().split(':')[1].replace(' ', ''))
        distance = int(f.readline().split(':')[1].replace(' ', ''))
    return [time, distance]


def get_boundary_times(time, record):
    d = time * time - 4 * record
    sd = math.sqrt(d)
    t1 = (-time + sd)/(-2)
    if isinstance(t1, int):
        t1 = t1 + 1
    else:
        t1 = math.ceil(t1)

    t2 = (-time - sd)/(-2)
    if isinstance(t2, int):
        t2 = t2 - 1
    else:
        t2 = math.floor(t2)

    return t1, t2


def find_number_of_ways_to_win(t1, t2):
    return t2 - t1 + 1

def main():
    race = get_race()
    time = race[0]
    distance = race[1]

    t1, t2 = get_boundary_times(time, distance)
    print(find_number_of_ways_to_win(t1, t2))


if __name__ == "__main__":
    main()