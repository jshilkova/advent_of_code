import argparse
import re
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()

    final_number = 0

    with Path(args.path).open() as lines:
        for line in lines:
            temp = re.findall(r'\d', line)
            final_number += int(temp[0] + temp[-1])

    print(final_number)


if __name__ == "__main__":
    main()
