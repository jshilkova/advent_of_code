import argparse
from pathlib import Path


def get_next_tile(current_tile, direction, contraption):
    x, y = list(map(int, current_tile.split(',')))
    match direction:
        case 'r':
            if y + 1 < len(contraption[0]):
                return [x, y + 1]
        case 'l':
            if y > 0:
                return [x, y - 1]
        case 'u':
            if x > 0:
                return [x - 1, y]
        case 'd':
            if x + 1 < len(contraption):
                return [x + 1, y]
    return -1


def get_contraption():
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()

    with Path(args.path).open() as f:
        contraption = f.read().split('\n')
    return contraption


def energize(contraption, beams):
    energized = {}

    while beams:
        beam = beams.pop(0)
        direction = beam[1]
        next_tile = get_next_tile(beam[0], direction, contraption)
        while next_tile != -1:

            tile = contraption[next_tile[0]][next_tile[1]]

            if tile == '-':
                if direction in 'ud':
                    beam[1] = 'r'
                    beams.append([f'{next_tile[0]},{next_tile[1]}', 'l'])

            if tile == '|':
                if direction in 'lr':
                    beam[1] = 'u'
                    beams.append([f'{next_tile[0]},{next_tile[1]}', 'd'])

            if tile == '\\':
                match direction:
                    case 'r':
                        beam[1] = 'd'
                    case 'l':
                        beam[1] = 'u'
                    case 'u':
                        beam[1] = 'l'
                    case 'd':
                        beam[1] = 'r'
            if tile == '/':
                match direction:
                    case 'r':
                        beam[1] = 'u'
                    case 'l':
                        beam[1] = 'd'
                    case 'u':
                        beam[1] = 'r'
                    case 'd':
                        beam[1] = 'l'

            beam[0] = f'{next_tile[0]},{next_tile[1]}'
            direction = beam[1]
            next_tile = get_next_tile(beam[0], direction, contraption)

            if beam[0] in energized:
                if direction in energized[beam[0]]:
                    break
                else:
                    energized[beam[0]] += direction
            else:
                energized[beam[0]] = direction

    return len(energized)

def main():
    en = []
    contraption = get_contraption()
    n = len(contraption)
    m = len(contraption[0])
    for i in range(n):
        en.append(energize(contraption, [[f'{i},-1', 'r']]))
        en.append(energize(contraption, [[f'{i},{m}', 'l']]))
    for j in range(m):
        en.append(energize(contraption, [[f'-1,{j}', 'd']]))
        en.append(energize(contraption, [[f'{n},{j}', 'u']]))
    print(max(en))


if __name__ == "__main__":
    main()
