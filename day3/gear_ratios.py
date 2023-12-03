import typing

FILENAME: str = "input.txt"


def is_symbol(el: str) -> bool:
    return el != "." and not el.isdigit()


def neighbor_has_symbol(lines: typing.List[str], i: int, j: int, max_i: int, max_j: int) -> bool:
    indices: typing.List[typing.Tuple[int, int]] = []

    offsets = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for o_i, o_j in offsets:
        x, y = (i + o_i), (j + o_j)
        if 0 <= x < max_i and 0 <= y < max_j:
            indices.append((x, y))

    return any(is_symbol(lines[i][j]) for i, j in indices)


def main() -> None:
    with open(FILENAME, "r") as fh:
        lines = fh.read().splitlines()

    number_str, found = "", False
    max_i = len(lines)
    result = 0
    for i, line in enumerate(lines):
        max_j = len(line)
        for j, el in enumerate(line):
            # we're in a number
            if el.isdigit():
                number_str += el
                found = found or neighbor_has_symbol(lines, i, j, max_i, max_j)
            else:
                if found:
                    result += int(number_str)
                if found or number_str:
                    print(number_str, found, result)
                # reset
                number_str, found = "", False

        # reset for a new line
        number_str, found = "", False

    print(result)


if __name__ == "__main__":
    main()
