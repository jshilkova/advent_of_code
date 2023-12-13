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


def mark_tiles(tiles, pipe, pipe_number, marks_map):
    pipe_direction = pipe[0][0]
    x, y = pipe[1][0], pipe[1][1]

    marks_map[x][y] = 'P'

    match pipe_direction:
        case 'n':
            if tiles[x][y] == '|':
                if y > 0:
                    marks_map[x][y - 1] = 'R' if pipe_number == 0 else 'L'
                if y + 1 < len(tiles[0]):
                    marks_map[x][y + 1] = 'L' if pipe_number == 0 else 'R'
            if tiles[x][y] == 'L':
                if y > 0:
                    marks_map[x][y - 1] = 'R' if pipe_number == 0 else 'L'
                if x + 1 > len(tiles):
                    marks_map[x + 1][y] = 'R' if pipe_number == 0 else 'L'
            if tiles[x][y] == 'J':
                if y + 1 < len(tiles[0]):
                    marks_map[x][y + 1] = 'L' if pipe_number == 0 else 'R'
                if x + 1 < len(tiles):
                    marks_map[x + 1][y] = 'L' if pipe_number == 0 else 'R'
        case 'e':
            if tiles[x][y] == '-':
                if x > 0:
                    marks_map[x - 1][y] = 'R' if pipe_number == 0 else 'L'
                if x + 1 < len(tiles):
                    marks_map[x + 1][y] = 'L' if pipe_number == 0 else 'R'
            if tiles[x][y] == 'L':
                if y > 0:
                    marks_map[x][y - 1] = 'L' if pipe_number == 0 else 'R'
                if x + 1 < len(tiles):
                    marks_map[x + 1][y] = 'L' if pipe_number == 0 else 'R'
            if tiles[x][y] == 'F':
                if x > 0:
                    marks_map[x - 1][y] = 'R' if pipe_number == 0 else 'L'
                if y > 0:
                    marks_map[x][y - 1] = 'R' if pipe_number == 0 else 'L'
        case 's':
            if tiles[x][y] == '|':
                if y > 0:
                    marks_map[x][y - 1] = 'L' if pipe_number == 0 else 'R'
                if y + 1 < len(tiles[0]):
                    marks_map[x][y + 1] = 'R' if pipe_number == 0 else 'L'
            if tiles[x][y] == 'F':
                if y > 0:
                    marks_map[x][y - 1] = 'L' if pipe_number == 0 else 'R'
                if x > 0:
                    marks_map[x - 1][y] = 'L' if pipe_number == 0 else 'R'
            if tiles[x][y] == '7':
                if y + 1 < len(tiles[0]):
                    marks_map[x][y + 1] = 'R' if pipe_number == 0 else 'L'
                if x > 0:
                    marks_map[x - 1][y] = 'R' if pipe_number == 0 else 'L'
        case 'w':
            if tiles[x][y] == '-':
                if x > 0:
                    marks_map[x - 1][y] = 'L' if pipe_number == 0 else 'R'
                if x + 1 < len(tiles):
                    marks_map[x + 1][y] = 'R' if pipe_number == 0 else 'L'
            if tiles[x][y] == '7':
                if y + 1 < len(tiles[0]):
                    marks_map[x][y + 1] = 'L' if pipe_number == 0 else 'R'
                if x > 0:
                    marks_map[x - 1][y] = 'L' if pipe_number == 0 else 'R'
            if tiles[x][y] == 'J':
                if x + 1 < len(tiles):
                    marks_map[x + 1][y] = 'R' if pipe_number == 0 else 'L'
                if y + 1 < len(tiles[0]):
                    marks_map[x][y + 1] = 'R' if pipe_number == 0 else 'L'


def find_inside_tiles_count(loop_map, marks_map):
    outside = define_outside(loop_map, marks_map)
    if not outside:
        return -1
    inside = 'L' if outside == 'R' else 'R'
    inside_tiles = 0
    for i in range(0, len(loop_map)):
        for j in range(0, len(loop_map[0])):
            if loop_map[i][j] == '.' and marks_map[i][j] == '.':
                if j == 0:
                    marks_map[i][j] = outside
                elif loop_map[i][j - 1] == '.':
                    marks_map[i][j] = marks_map[i][j - 1]
    for i in range(0, len(loop_map)):
        for j in range(0, len(loop_map[0])):
            if loop_map[i][j] == '.' and marks_map[i][j] == inside:
                inside_tiles += 1
    return inside_tiles


def build_loop_and_marks_map(tiles):
    loop_map = []
    for i in range(0, len(tiles)):
        loop_map.append([])
        for j in range(0, len(tiles[0])):
            loop_map[i].append('.')

    marks_map = []
    for i in range(0, len(tiles)):
        marks_map.append([])
        for j in range(0, len(tiles[0])):
            marks_map[i].append('.')

    start = find_start(tiles)
    loop_map[start[0]][start[1]] = 'L'
    pipes = find_start_directions(tiles, start)
    for pipe in pipes:
        loop_map[pipe[1][0]][pipe[1][1]] = 'L'
    for p in range(0, 2):
        mark_tiles(tiles, pipes[p], p, marks_map)
    while pipes[0][1] != pipes[1][1]:
        for pipe in pipes:
            go_to_next_connected(tiles, pipe)
            loop_map[pipe[1][0]][pipe[1][1]] = 'L'
        for p in range(0, 2):
            mark_tiles(tiles, pipes[p], p, marks_map)
    loop_map[pipes[0][1][0]][pipes[0][1][1]] = 'L'
    mark_tiles(tiles, pipes[0], 0, marks_map)

    return loop_map, marks_map


def define_outside(loop_map, marks_map):
    n = len(loop_map[0])
    for j in range(0, n):
        if loop_map[0][j] == '.' and marks_map[0][j] != '.':
            return marks_map[0][j]
    for j in range(0, n):
        m = len(loop_map)
        if loop_map[m - 1][j] == '.' and marks_map[m - 1][j] != '.':
            return marks_map[m - 1][j]


def main():
    tiles = get_tiles()
    loop_map, marks_map = build_loop_and_marks_map(tiles)

    inside_tiles = find_inside_tiles_count(loop_map, marks_map)

    print(inside_tiles)


if __name__ == "__main__":
    main()
