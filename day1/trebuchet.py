import typing

FILENAME: str = "input.txt"

NUMBERS: typing.Dict[str, int] = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def part1() -> None:
    with open(FILENAME, "r") as fh:
        lines = fh.readlines()

    digits = [[int(c) for c in line if c.isdigit()] for line in lines]
    answer = sum([d[0] * 10 + d[-1] for d in digits])
    print(answer)


def part2() -> None:
    with open(FILENAME, "r") as fh:
        lines = fh.readlines()

    digits: typing.List[typing.List[int]] = []
    for line in lines:
        ld = []
        for pos, c in enumerate(line):
            if c.isdigit():
                ld.append(int(c))
            else:
                for word, value in NUMBERS.items():
                    if line[pos : pos + len(word)] == word:
                        ld.append(value)

        digits.append(ld)

    answer = sum([d[0] * 10 + d[-1] for d in digits])
    print(answer)


if __name__ == "__main__":
    part2()
