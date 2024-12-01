import argparse
from pathlib import Path
import utils


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()

    final_number = 0

    with (Path(args.path).open() as lines):
        for line in lines:
            my_numbers, winning_numbers = utils.get_numbers(line)
            points = 0
            for number in winning_numbers:
                if number in my_numbers:
                    if points:
                        points *= 2
                    else:
                        points = 1
            final_number += points
    print(final_number)


if __name__ == "__main__":
    main()
