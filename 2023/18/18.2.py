import argparse
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))


def get_dig_plan0():
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()
    plan = []
    with Path(args.path).open() as f:
        for line in f:
            d, count, color = line.split()
            plan.append([d, int(count), color[1:-1]])
    return plan


def get_dig_plan():
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()
    plan = []
    with Path(args.path).open() as f:
        for line in f:
            d, count, color = line.split()
            new_steps = int(color[2:-2], 16)
            match color[-2:-1]:
                case '0':
                    plan.append(['R', new_steps])
                case '1':
                    plan.append(['D', new_steps])
                case '2':
                    plan.append(['L', new_steps])
                case '3':
                    plan.append(['U', new_steps])
    return plan


def build_the_grid(dig_plan):
    grid = {0: {0: [0, 0]}}
    current_x = current_y = 0
    for instruction in dig_plan[:-1]:
        d, steps = instruction
        if d == 'R':
            grid[current_x][current_y] = [current_y, current_y + steps]
            current_y += steps
        if d == 'L':
            grid[current_x][current_y - steps] = [current_y - steps, current_y]
            if current_y in grid[current_x]:
                del grid[current_x][current_y]
            current_y -= steps

        if d == 'U':
            for i in range(steps):
                current_x -= 1
                if current_x in grid:
                    grid[current_x][current_y] = [current_y, current_y]
                else:
                    grid[current_x] = {current_y: [current_y, current_y]}
        if d == 'D':
            for i in range(steps):
                current_x += 1
                if current_x in grid:
                    grid[current_x][current_y] = [current_y, current_y]
                else:
                    grid[current_x] = {current_y: [current_y, current_y]}
    d, steps = dig_plan[-1]
    if d == 'U':
        for i in range(steps-1):
            current_x -= 1
            if current_x in grid:
                grid[current_x][current_y] = [current_y, current_y]
            else:
                grid[current_x] = {current_y: [current_y, current_y]}
    return grid


def count_tiles(grid):
    max_x = max(grid.keys())
    min_x = min(grid.keys())

    lava_tiles = 0
    for i in grid:
        s_keys = sorted(grid[i].keys())
        inside = False
        for n, j in enumerate(s_keys):
            v = grid[i][j]
            if v[0] == v[1]:
                if inside:
                    lava_tiles += v[1] - grid[i][s_keys[n - 1]][1]
                else:
                    lava_tiles += 1
                inside = not inside
            else:
                if inside:
                    lava_tiles += v[1] - grid[i][s_keys[n - 1]][1]
                else:
                    lava_tiles += v[1] - v[0] + 1
                if not (i == max_x or i == min_x or
                        (v[0] in grid[i - 1] and v[1] in grid[i - 1]) or
                        (v[0] in grid[i + 1] and v[1] in grid[i + 1])):
                    inside = not inside
    return lava_tiles


def main():
    dig_plan = get_dig_plan()
    grid = build_the_grid(dig_plan)
    print(count_tiles(grid))


if __name__ == "__main__":
    main()
