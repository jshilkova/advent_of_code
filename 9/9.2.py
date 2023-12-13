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
    first_values = [history[0]]
    current_differences = history
    while not all(diff == 0 for diff in current_differences):
        new_differences = []
        for i in range(1, len(current_differences)):
            diff = current_differences[i] - current_differences[i-1]
            new_differences.append(diff)
        first_values.append(new_differences[0])
        current_differences = new_differences

    predicted_values = [0]
    values_count = len(first_values)
    for i in range(1, values_count):
        predicted_values.append(first_values[values_count - i - 1] - predicted_values[i-1])
    return predicted_values[-1]


def main():
    report = get_oasis_report()
    final_number = 0
    for history in report:
        final_number += predict_value(history)
    print(final_number)


if __name__ == "__main__":
    main()
