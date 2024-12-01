import argparse
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
        parts = []
        for line in f:
            part = line[1:-2].split(',')

            parts.append({p[:1]: int(p[2:]) for p in part})
    return rules, parts


def process_part(rules, part):
    current_wf = 'in'
    while current_wf not in 'AR':
        for rule in rules[current_wf]:
            if ':' in rule:
                cond, next_rule = rule.split(':')
                if cond[1] == '>':
                    if part[cond[0]] > int(cond[2:]):
                        current_wf = next_rule
                        break
                else:
                    if part[cond[0]] < int(cond[2:]):
                        current_wf = next_rule
                        break
            else:
                current_wf = rule
    return sum(part.values()) if current_wf == 'A' else 0


def main():
    rules, parts = get_input()
    final_number = 0
    for part in parts:
        final_number += process_part(rules, part)
    print(final_number)


if __name__ == "__main__":
    main()
