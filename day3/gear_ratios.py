import typing

FILENAME: str = "input.txt"

OFFSETS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


def is_symbol(el: str) -> bool:
    return el != "." and not el.isdigit()


def neighbor_has_symbol(lines: typing.List[str], i: int, j: int, max_i: int, max_j: int) -> bool:
    indices: typing.List[typing.Tuple[int, int]] = []

    for o_i, o_j in OFFSETS:
        x, y = (i + o_i), (j + o_j)
        if 0 <= x < max_i and 0 <= y < max_j:
            indices.append((x, y))

    return any(is_symbol(lines[i][j]) for i, j in indices)


def find_neighboring_numbers(lines: typing.List[str], i: int, j: int, max_i: int, max_j: int) -> typing.List[int]:
    # coords that hava already been checked
    checked: typing.List[typing.Tuple[int, int]] = []

    indices: typing.List[typing.Tuple[int, int]] = []
    for o_i, o_j in OFFSETS:
        x, y = (i + o_i), (j + o_j)
        if 0 <= x < max_i and 0 <= y < max_j:
            indices.append((x, y))

    numbers = []
    # Check all candidates
    for x, y in indices:
        # Check the candidate itself
        number_str = ""
        if lines[x][y].isdigit() and (x, y) not in checked:
            number_str += lines[x][y]
        else:
            continue
        checked.append((x, y))

        # grow right
        for a in range(y + 1, max_j):
            can = lines[x][a]
            if can.isdigit() and (x, a) not in checked:
                number_str += can
                checked.append((x, a))
            else:
                break
        # grow left
        for a in range(y - 1, -1, -1):
            can = lines[x][a]
            if can.isdigit() and (x, a) not in checked:
                # prepend in case of left grow
                number_str = f"{can}{number_str}"
                checked.append((x, a))
            else:
                break

        if number_str:
            numbers.append(int(number_str))

    return numbers


def part1() -> None:
    with open(FILENAME, "r") as fh:
        lines = fh.read().splitlines()

    max_i = len(lines)
    result = 0
    for i, line in enumerate(lines):
        max_j = len(line)
        # reset for a new line
        number_str, found = "", False
        for j, el in enumerate(line):
            # we're in a number
            if el.isdigit():
                number_str += el
                found |= neighbor_has_symbol(lines, i, j, max_i, max_j)
            else:
                if found:
                    result += int(number_str)
                # # debug
                # if found or number_str:
                #     print(number_str, found, result)

                # reset
                number_str, found = "", False

        # handle end of line number
        if found:
            # print("EOL", number_str, found, result)
            result += int(number_str)

    print(result)


def main() -> None:
    with open(FILENAME, "r") as fh:
        lines = fh.read().splitlines()

    max_i = len(lines)
    result = 0
    for i, line in enumerate(lines):
        max_j = len(line)
        for j, el in enumerate(line):
            if el == "*":
                numbers = find_neighboring_numbers(lines, i, j, max_i, max_j)
                # print(numbers)
                if len(numbers) == 2:
                    prod = 1
                    for number in numbers:
                        prod *= number
                    result += prod
                    print(numbers, prod, result)
    print(result)


if __name__ == "__main__":
    main()
