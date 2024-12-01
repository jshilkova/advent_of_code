import argparse
from pathlib import Path


def get_fields():
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()

    with Path(args.path).open() as f:
        fields = []
        for fld in f.read().split('\n\n'):
            fields.append(fld.strip().split('\n'))
    return fields


def transpose_field(field):
    t_field = []
    for col in range(len(field[0])):
        t_field.append([x[col] for x in field])
    return t_field


def has_one_smudge(line1, line2):
    diff = 0
    for i in range(len(line1)):
        if line1[i] != line2[i]:
            diff += 1
            if diff > 1:
                return False
    return True if diff == 1 else False


def find_horizontal_symmetry_with_a_smudge(field):
    for i, line in enumerate(field[1:], 1):
        if line == field[i - 1] or has_one_smudge(line, field[i - 1]):
            smudged_lines = 0
            sym = True
            for step in range(0, min(i, len(field) - i)):
                if has_one_smudge(field[i + step], field[i - step - 1]):
                    smudged_lines += 1

                elif field[i + step] != field[i - step - 1] or smudged_lines > 1:
                    sym = False
                    break

            if sym and smudged_lines == 1:
                return i
    return -1


def main():
    fields = get_fields()
    final_number = 0
    for field in fields:
        hs = find_horizontal_symmetry_with_a_smudge(field)
        if hs > 0:
            final_number += 100 * hs
        else:
            vs = find_horizontal_symmetry_with_a_smudge(transpose_field(field))
            if vs > 0:
                final_number += vs
            else:
                print("No symmetry found")
    print(final_number)


if __name__ == "__main__":
    main()
