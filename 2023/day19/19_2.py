import argparse
import copy
import math
from pathlib import Path


def get_input():
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()

    rules = {}
    with Path(args.path).open() as f:
        for line in f:
            if line == '\n':
                break
            name = line[: line.index('{')]
            rule = line[line.index('{') + 1:line.index('}')].split(',')
            rules[name] = rule
    return rules


xxmas = {'x': 0, 'm': 1, 'a': 2, 's': 3}


def count_combos(rules, current_rule, position, xmas):
    if current_rule == 'A':
        ranges = [v[1] - v[0] + 1 for v in xmas.values()]
        return math.prod(ranges)
    if current_rule == 'R':
        return 0
    count = 0
    if ':' in rules[current_rule][position]:
        cond, next_rule = rules[current_rule][position].split(':')
        if '>' in cond:
            letter, number = cond.split('>')
            number = int(number)
            if xmas[letter][0] <= number:
                greater_xmas = copy.deepcopy(xmas)
                greater_xmas[letter] = [number + 1, xmas[letter][1]]
                count += count_combos(rules, next_rule, 0, greater_xmas)
            if xmas[letter][1] > number:
                smaller_xmas = copy.deepcopy(xmas)
                smaller_xmas[letter] = [xmas[letter][0], number]
                count += count_combos(rules, current_rule, position + 1, smaller_xmas)
        else:
            letter, number = cond.split('<')
            number = int(number)
            if xmas[letter][1] >= number:
                smaller_xmas = copy.deepcopy(xmas)
                smaller_xmas[letter] = [xmas[letter][0], number - 1]
                count += count_combos(rules, next_rule, 0, smaller_xmas)
            if xmas[letter][0] < number:
                greater_xmas = copy.deepcopy(xmas)
                greater_xmas[letter] = [number, xmas[letter][1]]
                count += count_combos(rules, current_rule, position + 1, greater_xmas)
    elif current_rule != 'in':
        count += count_combos(rules, rules[current_rule][position], 0, xmas)
    return count


def main():
    rules = get_input()
    final_count = count_combos(rules, 'in', 0, {key: [1, 4000] for key in 'xmas'})

    print(final_count)


if __name__ == "__main__":
    main()
