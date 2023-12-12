import argparse
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


def follow_instructions(instructions, network, current_element, steps):
    for instruction in instructions:
        steps += 1
        current_element = network[current_element][int(instruction)]
        if current_element == 'ZZZ':
            break

    return steps, current_element


def main():
    instructions, network = get_instructions_and_network()
    current_element = 'AAA'
    steps = 0
    while current_element != 'ZZZ':
        steps, current_element = follow_instructions(instructions, network, current_element, steps)
    print(steps)


if __name__ == "__main__":
    main()
