import typing

FILENAME: str = "input.txt"


def is_symbol(el: str) -> bool:
    return el != "." and not el.isdigit()


def neighbor_has_symbol(lines: typing.List[str], i: int, j: int, max_i: int, max_j: int) -> bool:
    indices: typing.List[typing.Tuple[int, int]] = []

    for o_i in [-1, 0, 1]:
        for o_j in [-1, 0, 1]:
            x, y = (i + o_i), (j + o_j)
            if 0 <= x < max_i and 0 <= y < max_j:
                indices.append((x, y))

    return any(is_symbol(lines[i][j]) for i, j in indices)


def main() -> None:
    with open(FILENAME, "r") as fh:
        lines = fh.read().splitlines()

    number = ""
    has_symbol = False
    max_i = len(lines)
    parts = []
    s = 0
    for i, line in enumerate(lines):
        max_j = len(line)
        for j, el in enumerate(line):
            # entering a new number
            if el.isdigit() and not number:
                number = el
                has_symbol |= neighbor_has_symbol(lines, i, j, max_i, max_j)
            # append to the current number
            elif el.isdigit() and number:
                number += el
                has_symbol |= neighbor_has_symbol(lines, i, j, max_i, max_j)
            # at the end of a number
            elif not el.isdigit() and number:
                if has_symbol:
                    n = int(number)
                    if n not in parts:
                        parts.append(n)
                        s += n
                print(has_symbol, number, s)
                # reset everything again
                number = ""
                # reset symbol
                has_symbol = False

    print(f"sum is {s}")


if __name__ == "__main__":
    main()
