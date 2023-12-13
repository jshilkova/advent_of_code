import argparse
from functools import reduce
from pathlib import Path

directions = ['north', 'east', 'south', 'west']
connections = {'|': ['n', 's'], '-': ['e', 'w'], 'L': ['n', 'e'], 'J': ['n', 'w'], '7': ['s', 'w'], 'F': ['s', 'e']}
opposites = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}


def get_tiles():
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()
    tiles = []

    with Path(args.path).open() as f:
        for line in f:
            tiles.append(line.strip())
    return tiles


def find_start(tiles):
    x = 0
    y = 0
    for line in tiles:
        if 'S' in line:
            y = line.index('S')
            break
        x += 1

    return x, y


def connected(side, start_tile, tiles):
    x, y = start_tile
    match side:
        case "north":
            tile = tiles[x - 1][y]
            if tile in '|7F':
                return ['s', [x - 1, y]]
        case "east":
            tile = tiles[x][y + 1]
            if tile in '-J7':
                return ['w', [x, y + 1]]
        case "south":
            tile = tiles[x + 1][y]
            if tile in '|LJ':
                return ['n', [x + 1, y]]
        case "west":
            tile = tiles[x][y - 1]
            if tile in '-LF':
                return ['e', [x, y - 1]]
    return False


def go_to_next_connected(tiles, pipe):
    x, y = pipe[1]
    prev_direction = pipe[0]
    conn = connections[tiles[x][y]]
    # print('current conn ', conn)
    next_direction = conn[abs(conn.index(prev_direction) - 1)]
    pipe[0] = opposites[next_direction]
    match next_direction:
        case 'n':
            pipe[1] = [x - 1, y]
        case 'e':
            pipe[1] = [x, y + 1]
        case 's':
            pipe[1] = [x + 1, y]
        case 'w':
            pipe[1] = [x, y - 1]
    return pipe


def find_start_directions(tiles, start):
    pipes = []
    for direction in directions:
        pipe = connected(direction, start, tiles)
        if pipe:
            pipes.append(pipe)
    return pipes


def main():
    tiles = get_tiles()
    start = find_start(tiles)
    pipes = find_start_directions(tiles, start)
    steps = 1
    while pipes[0][1] != pipes[1][1]:
        for pipe in pipes:
            go_to_next_connected(tiles, pipe)
        steps += 1
        # print(pipes)
    print(steps)


if __name__ == "__main__":
    main()
