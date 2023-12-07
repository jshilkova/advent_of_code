import argparse
from pathlib import Path


def get_seeds_and_maps():
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()

    with Path(args.path).open() as almanac:
        seeds = list(map(int, almanac.readline().split(':')[1].strip().split(' ')))
        alm_maps = []
        line = almanac.readline()
        for i in range(1, 8):
            for j in range(1, 3):
                line = almanac.readline()
            current_map = []
            while line != '\n' and line:
                current_map.append(list(map(int, line.strip().split(' '))))
                line = almanac.readline()
                current_map = sorted(current_map, key=lambda x: x[1])
            alm_maps.append(current_map)
    return seeds, alm_maps


def get_seed_position(seed, match_ranges):
    if seed < match_ranges[0][0]:
        return -1

    match_r = 0
    for r in match_ranges:
        if seed > r[1]:
            match_r += 1
        else:
            break

    if match_r == len(match_ranges):
        return -2
    else:
        return match_r


def map_range(source_range, match_map):
    match_ranges = [[match_map[0][1], match_map[0][1] + match_map[0][2] - 1]]
    for i in range(1, len(match_map)):
        if match_map[i][1] > match_map[i - 1][1] + match_map[i - 1][2]:
            match_ranges.append([match_map[i - 1][1] + match_map[i - 1][2], match_map[i][1] - 1])
        match_ranges.append([match_map[i][1], match_map[i][1] + match_map[i][2] - 1])

    start_range = get_seed_position(source_range[0], match_ranges)
    end_range = get_seed_position(source_range[1], match_ranges)

    if start_range == -2 or end_range == -1:
        return [source_range]

    result_ranges = []
    if start_range == -1:
        result_ranges.append([source_range[0], match_ranges[0][0] - 1])
        source_range[0] = match_ranges[0][0]
        start_range = 0

    result_ranges.append([source_range[0], min(match_ranges[start_range][1], source_range[1])])
    r = start_range + 1

    while r < len(match_ranges) and result_ranges[-1][1] < source_range[1]:
        result_ranges.append([match_ranges[r][0], min(match_ranges[r][1], source_range[1])])
        r += 1

    if end_range == -2:
        result_ranges.append([match_ranges[-1][1] + 1, source_range[1]])

    return result_ranges


def find_corresponding(source, match_map_r):
    match_map = sorted(match_map_r, key=lambda x: x[0])
    map_line = 0
    while map_line < len(match_map) and source < match_map[map_line][1]:
        map_line += 1
    if (map_line == len(match_map)
            or source > match_map[map_line][1] + match_map[map_line][2] - 1
            or source > match_map[0][1] + match_map[0][2] - 1):

        return source
    else:
        return match_map[map_line][0] + source - match_map[map_line][1]


def find_corresponding_ranges(source_ranges, match_map):
    mapped_ranges = []
    for r in range(0, len(source_ranges)):
        mapped_ranges.append(
            [find_corresponding(source_ranges[r][0], match_map),
             find_corresponding(source_ranges[r][1], match_map)])
    return sorted(mapped_ranges, key=lambda x: x[0])


def main():
    seeds, alm_maps = get_seeds_and_maps()
    seed_ranges = []
    for seed_r in range(0, len(seeds), 2):
        seed_ranges.append([seeds[seed_r], seeds[seed_r] + seeds[seed_r + 1] - 1])

    ranges_to_map = sorted(seed_ranges, key=lambda x: x[0])
    for m in range(0, 7):
        current_ranges_to_map = []
        for r in ranges_to_map:
            current_ranges_to_map.extend(map_range(r, alm_maps[m]))
        ranges_to_map = find_corresponding_ranges(current_ranges_to_map, alm_maps[m])

    print(ranges_to_map[0][0])


if __name__ == "__main__":
    main()
