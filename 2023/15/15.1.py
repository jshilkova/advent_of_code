import argparse
from pathlib import Path


def get_strings():
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()

    with Path(args.path).open() as f:
        strings = f.read().split(',')
    return strings


def get_hash(string):
    val = 0
    for ch in string:
        val += ord(ch)
        val *= 17
        val = val % 256
    return val


def main():
    strings = get_strings()
    final_number = 0
    for line in strings:
        final_number += get_hash(line)
    print(final_number)


if __name__ == "__main__":
    main()
