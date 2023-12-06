import argparse
from pathlib import Path


def get_engine_schematic():
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()

    engine = []
    i = 0
    with Path(args.path).open() as lines:
        for line in lines:
            engine.append(list('.' + line.strip() + '.'))
            i += 1
    m = len(engine[0])
    empty_line = ['.'] * m
    engine.insert(0, empty_line)
    engine.append(empty_line)

    return i + 2, m, engine
