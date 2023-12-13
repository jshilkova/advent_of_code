import argparse
from functools import reduce
from pathlib import Path


def get_oasis_report():
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()
    report = []

    with Path(args.path).open() as f:
        for line in f:
            history = list(map(int, line.split(' ')))
            report.append(history)
    return report


def predict_value(history):
    last_values = [history[-1]]
    current_differences = history
    while not all(diff == 0 for diff in current_differences):
        new_differences = []
        for i in range(1, len(current_differences)):
            diff = current_differences[i] - current_differences[i-1]
            new_differences.append(diff)
        last_values.append(new_differences[-1])
        current_differences = new_differences
    return reduce(lambda a, b: a+b, last_values)


def main():
    report = get_oasis_report()
    final_number = 0
    for history in report:
        final_number += predict_value(history)
    print(final_number)


if __name__ == "__main__":
    main()
