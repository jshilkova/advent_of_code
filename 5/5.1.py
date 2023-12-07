import argparse
from pathlib import Path


def get_seeds_and_maps():
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()

    with Path(args.path).open() as almanac:
        seeds = list(map(int, almanac.readline().split(':')[1].strip().split(' ')))
        alm_maps =[]
        line = almanac.readline()
        for i in range(1, 8):
            for j in range(1, 3):
                line = almanac.readline()
            current_map = []
            while line != '\n' and line:
                current_map.append(list(map(int, line.strip().split(' '))))
                line = almanac.readline()
                current_map = sorted(current_map, key=lambda x: x[1], reverse=True)
            alm_maps.append(current_map)
    return seeds, alm_maps


def find_corresponding(source, match_map):
    map_line = 0
    while map_line < len(match_map) and source < match_map[map_line][1]:
        map_line += 1
    if (map_line == len(match_map)
            or source > match_map[map_line][1] + match_map[map_line][2] - 1
            or source > match_map[0][1] + match_map[0][2] - 1):

        return source
    else:
        return match_map[map_line][0] + source - match_map[map_line][1]


def map_seed_to_location(seed, alm_maps):
    mapped = seed
    for i in range(0, 7):
        mapped = find_corresponding(mapped, alm_maps[i])
    return mapped

def main():
    seeds, alm_maps = get_seeds_and_maps()
    locations = []
    for seed in seeds:
        mapped = map_seed_to_location(seed,alm_maps)
        locations.append(mapped)

    print(min(locations))


if __name__ == "__main__":
    main()
