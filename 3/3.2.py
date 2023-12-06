import utils


def is_a_gear(engine, row, column):
    digits = []
    for i in range(row - 1, row + 2):
        j = column - 1
        while j < column + 2:
            current_number = ''
            if engine[i][j].isdigit():
                backward_steps = 1
                current_number = ''
                while engine[i][j - backward_steps].isdigit():
                    current_number = engine[i][j - backward_steps] + current_number
                    backward_steps += 1
                while engine[i][j].isdigit():
                    current_number += engine[i][j]
                    j += 1
                digits.append(current_number)
            j += 1
    if len(digits) == 2:
        return digits
    else:
        return False


def main():
    n, m, engine = utils.get_engine_schematic()
    final_number = 0
    for i in range(1, n - 1):
        for j in range(1, m - 1):
            if engine[i][j] == '*':
                digits = is_a_gear(engine, i, j)
                if digits:
                    final_number += int(digits[0]) * int(digits[1])

    print(final_number)


if __name__ == "__main__":
    main()
