import utils


def is_adjacent_to_symbol(engine, row, column, size):
    for i in range(row - 1, row + 2):
        for j in range(column - 1, column + size + 1):
            if engine[i][j] != '.' and not engine[i][j].isdigit():
                return True
    return False


def main():
    n, m, engine = utils.get_engine_schematic()
    final_number = 0
    for i in range(1, n - 1):
        j = 1
        while j < m - 1:
            if engine[i][j].isdigit():
                current_digit = ''
                while engine[i][j].isdigit():
                    current_digit += engine[i][j]
                    j += 1
                digit_size = len(current_digit)
                if is_adjacent_to_symbol(engine, i, j - digit_size, digit_size):
                    final_number += int(current_digit)
            j += 1
    print(final_number)


if __name__ == "__main__":
    main()
