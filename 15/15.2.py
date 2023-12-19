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


def process_lens(string, boxes, indexes):
    if '-' in string:
        label = string[:-1]
        box = get_hash(label)
        if label in indexes[box]:
            removed_lens_index = indexes[box][label]
            del boxes[box][removed_lens_index]
            del indexes[box][label]
            for k, v in indexes[box].items():
                if v > removed_lens_index:
                    indexes[box][k] = v - 1
    elif '=' in string:
        label = string[:-2]
        box = get_hash(label)
        focal_length = string.split('=')[1]
        if label in indexes[box]:
            boxes[box][indexes[box][label]] = [label, focal_length]
        else:
            boxes[box].append([label, focal_length])
            indexes[box][label] = boxes[box].index([label, focal_length])
    return boxes


def main():
    strings = get_strings()
    boxes = [[] for _x in range(256)]
    indexes = [{} for _x in range(256)]

    for line in strings:
        process_lens(line, boxes, indexes)

    final_number = 0
    for i, box in enumerate(boxes):
        for j, lens in enumerate(box):
            final_number += (i + 1) * (j + 1) * int(lens[1])
    print(final_number)


if __name__ == "__main__":
    main()
