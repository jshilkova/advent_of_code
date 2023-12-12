import argparse
import math
from pathlib import Path


def get_instructions_and_network():
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()

    with Path(args.path).open() as f:
        instructions = f.readline().strip().replace('L', '0').replace('R', '1')
        f.readline()
        network = {}
        for line in f:
            key, value = line.split('=')
            node1, node2 = value.strip()[1:-1].split(',')
            network[key.strip()] = [node1, node2.strip()]
    return instructions, network


def get_starting_points(network):
    starting_points = []
    for node in network:
        if node[2] == 'A':
            starting_points.append(node)
    return starting_points


def follow_instructions(instructions, network, current_points, steps, total_steps):
    for instruction in instructions:
        steps += 1
        new_points = []
        for i in range(0, len(current_points)):
            current_points[i] = network[current_points[i]][int(instruction)]
            if current_points[i][2] == 'Z':
                total_steps.append(steps)
            else:
                new_points.append(current_points[i])
        current_points = new_points
        if not current_points:
            break

    return steps, current_points, total_steps


def find_steps_count(total_steps):
    x = total_steps[0]
    lcm = 0
    for steps in total_steps[1:]:
        y = steps
        lcm = (x * y) / math.gcd(x, y)
        x = int(lcm)
    return int(lcm)


def main():
    instructions, network = get_instructions_and_network()
    current_points = get_starting_points(network)
    steps = 0
    total_steps = []
    while current_points:
        steps, current_points, total_steps = (
            follow_instructions(instructions, network, current_points, steps, total_steps))

    print(find_steps_count(total_steps))


if __name__ == "__main__":
    main()
