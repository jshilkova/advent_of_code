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


def process_lens(string, boxes, focal_lengths):
    if '-' in string:
        label = string[:-1]
        box_index = get_hash(label)
        if label in boxes[box_index]:
            boxes[box_index].remove(label)
    elif '=' in string:
        label = string[:-2]
        box_index = get_hash(label)
        focal_length = string.split('=')[1]
        if label in boxes[box_index]:
            focal_lengths[label] = int(focal_length)
        else:
            boxes[box_index].append(label)
            focal_lengths[label] = int(focal_length)
    return boxes


def main():
    strings = get_strings()
    boxes = [[] for _x in range(256)]
    focal_lengths = {}

    for line in strings:
        process_lens(line, boxes, focal_lengths)

    final_number = 0
    for i, box in enumerate(boxes, 1):
        for j, label in enumerate(box, 1):
            final_number += i * j * focal_lengths[label]
    print(final_number)


if __name__ == "__main__":
    main()
