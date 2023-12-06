import argparse
import utils
from pathlib import Path


def get_matches(my_numbers, winning_numbers):
    matches = 0
    for number in winning_numbers:
        if number in my_numbers:
            matches += 1
    return matches


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()

    card_count = []
    card_number = 1
    with (Path(args.path).open() as lines):
        for line in lines:
            if len(card_count) < card_number:
                card_count.extend([1])
            my_numbers, winning_numbers = utils.get_numbers(line)
            matches = get_matches(my_numbers, winning_numbers)
            for match in range(1, matches+1):
                if len(card_count) < card_number + match:
                    card_count.extend([1+card_count[card_number-1]])
                else:
                    card_count[card_number + match - 1] += card_count[card_number - 1]

            card_number += 1

        for i in range(len(card_count), card_number-1):
            card_count.extend([1])

        card_count = card_count[:card_number-1]

        final_number = sum(card_count)

    print(final_number)


if __name__ == "__main__":
    main()
