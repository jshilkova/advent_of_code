import argparse
import re
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()

    list_1 = []
    list_2 = []

    with Path(args.path).open() as lines:
        for line in lines:
            a, b = map(int, line.strip().split())
            list_1.append(a)
            list_2.append(b)

    list_1 = sorted(list_1)
    list_2 = sorted(list_2)
    final_number = sum([abs(x-y) for x, y in zip(list_1, list_2)])

    print(final_number)

if __name__ == "__main__":
    main()
