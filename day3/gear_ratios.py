import typing

FILENAME: str = "input.txt"


def is_symbol(el: str) -> bool:
    return el != "." and not el.isdigit()


def neighbor_has_symbol(lines: typing.List[str], i: int, j: int, max_i: int, max_j: int) -> bool:
    indices: typing.List[typing.Tuple[int, int]] = []
    # top row
    if i > 1:
        if j > 1:
            indices.append((i - 1, j - 1))
        indices.append((i - 1, j))
        if j < max_j - 1:
            indices.append((i - 1, j + 1))
    # current row
    if j > 1:
        indices.append((i, j - 1))
    if j < max_j - 1:
        indices.append((i, j + 1))
    # below row
    if i < max_i - 1:
        if j > 1:
            indices.append((i + 1, j - 1))
        indices.append((i + 1, j))
        if j < max_j - 1:
            indices.append((i + 1, j + 1))

    return any(is_symbol(lines[i][j]) for i, j in indices)


def main() -> None:
    with open(FILENAME, "r") as fh:
        lines = fh.read().splitlines()

    number = ""
    has_symbol = False
    max_i = len(lines)
    valid = []
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
                    # print(number)
                    n = int(number)
                    if n not in valid:
                        valid.append(n)
                        s += n
                print(has_symbol, number, s)
                # reset everything again
                number = ""
                # reset symbol
                has_symbol = False

    print(f"sum is {s}")


if __name__ == "__main__":
    main()
