import argparse
from pathlib import Path
from queue import PriorityQueue


def get_city_block():
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()

    with Path(args.path).open() as f:
        city_block = [list(map(int, line.strip())) for line in f]
    return city_block


def find_path(city_block):
    n = len(city_block)
    m = len(city_block[0])

    seen = {}
    pq = PriorityQueue()
    pq.put((0, 0, 0, 0, 1, 0))
    pq.put((0, 0, 0, 1, 0, 0))

    while not pq.empty():
        hl, r, c, dr, dc, steps = pq.get()
        if r == n - 1 and c == m - 1:
            return hl

        directions = [(-dc, dr), (dc, -dr)]
        if steps < 3:
            directions.append((dr, dc))

        for ndr, ndc in directions:
            nr = r + ndr
            nc = c + ndc
            if 0 <= nr < n and 0 <= nc < m:
                key = (nr, nc, ndr, ndc, steps + 1 if (ndr, ndc) == (dr, dc) else 1)
                nhl = hl + city_block[nr][nc]
                if key not in seen or nhl < seen[key]:
                    seen[key] = nhl
                    pq.put((nhl, *key))



def main():
    city_block = get_city_block()

    print(find_path(city_block))


if __name__ == "__main__":
    main()
