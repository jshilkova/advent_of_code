import argparse
import regex as re
from pathlib import Path


def word_to_digit(word):
    if len(word) > 1:
        numbers = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
        return str(numbers.index(word) + 1)
    else:
        return word


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()

    final_number = 0

    with Path(args.path).open() as lines:
        for line in lines:
            temp = re.findall(r'(?=(\d|one|two|three|four|five|six|seven|eight|nine))', line)
            final_number += int(word_to_digit(temp[0]) + word_to_digit(temp[-1]))

    print(final_number)


if __name__ == "__main__":
    main()
