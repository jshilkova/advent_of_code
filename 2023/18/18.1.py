import argparse
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from day10 import aoc10_2


def get_dig_plan():
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()
    plan = []
    with Path(args.path).open() as f:
        for line in f:
            d, count, color = line.split()
            plan.append([d, int(count), color[1:-1]])
    return plan


def build_the_maze(dig_plan):
    prev_d = "U"
    current_x = 0
    current_y = 0
    grid = {0: {0: '-'}}
    for instruction in dig_plan:
        d, steps, colour = instruction
        if d == 'R':
            if prev_d == 'U':
                grid[current_x][current_y] = 'F'
            if prev_d == 'D':
                grid[current_x][current_y] = 'L'
            for i in range(steps):
                current_y += 1
                grid[current_x][current_y] = '-'
        if d == 'L':
            if prev_d == 'U':
                grid[current_x][current_y] = '7'
            if prev_d == 'D':
                grid[current_x][current_y] = 'J'
            for i in range(steps):
                current_y -= 1
                grid[current_x][current_y] = '-'
        if d == 'U':
            if prev_d == 'L':
                grid[current_x][current_y] = 'L'
            if prev_d == 'R':
                grid[current_x][current_y] = 'J'
            for i in range(steps):
                current_x -= 1
                if current_x in grid:
                    grid[current_x][current_y] = '|'
                else:
                    grid[current_x] = {current_y: '|'}
        if d == 'D':
            if prev_d == 'L':
                grid[current_x][current_y] = 'F'
            if prev_d == 'R':
                grid[current_x][current_y] = '7'
            for i in range(steps):
                current_x += 1
                if current_x in grid:
                    grid[current_x][current_y] = '|'
                else:
                    grid[current_x] = {current_y: '|'}
        prev_d = d
    grid[current_x][current_y] = 'S'
    return grid


def draw_the_maze(grid):
    max_x = 0
    min_x = 0
    max_y = 0
    min_y = 0
    for i in grid:
        if i < min_y:
            min_y = i
        for j in grid[i]:
            if j < min_x:
                min_x = j
            if j > max_x:
                max_x = j
    n = len(grid)
    m = max_x - min_x + 1
    maze = [['.' for _j in range(m)] for _i in range(n)]
    for i in grid:
        for j in grid[i]:
            maze[i - min_y][j - min_x] = grid[i][j]
    maze_tiles = 0
    for i in grid:
        maze_tiles += len(grid[i])
    return maze, maze_tiles


def main():
    dig_plan = get_dig_plan()
    grid = build_the_maze(dig_plan)
    maze, maze_tiles = draw_the_maze(grid)

    loop_map, marks_map = aoc10_2.build_loop_and_marks_map(maze)
    inside_tiles = aoc10_2.find_inside_tiles_count(loop_map, marks_map)
    print(maze_tiles + inside_tiles)


if __name__ == "__main__":
    main()
