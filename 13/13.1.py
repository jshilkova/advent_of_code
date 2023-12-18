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


def find_horizontal_symmetry(field):
    for i, line in enumerate(field[1:], 1):
        if line == field[i - 1]:
            sym = True
            for step in range(0, min(i, len(field) - i)):
                if field[i + step] != field[i - step - 1]:
                    sym = False
            if sym:
                return i
    return -1


def main():
    fields = get_fields()
    final_number = 0
    for field in fields:
        hs = find_horizontal_symmetry(field)
        if hs > 0:
            final_number += 100 * hs
        else:
            vs = find_horizontal_symmetry(transpose_field(field))
            if vs > 0:
                final_number += vs
            else:
                print("No symmetry found")
    print(final_number)


if __name__ == "__main__":
    main()
