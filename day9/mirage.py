import numpy as np

# FILENAME: str = "example.txt"
FILENAME: str = "input.txt"

with open(FILENAME, "r") as fh:
    LINES = fh.readlines()


def main() -> None:
    # parsing
    lines = np.array([[int(i) for i in line.split(" ")] for line in LINES])

    # part1:  sum all last diffs (last item)
    result = 0
    for line in lines:
        result += line[-1]
        while not np.all(line == 0):
            d = np.diff(line)
            result += d[-1]
            line = d

    print(f"Part 1: {result}")

    # part2:  sum all last diffs (last item)
    result = 0
    for line in lines:
        # orig_line = line[:]
        first = [line[0]]
        while not np.all(line == 0):
            d = np.diff(line)
            # result += d[-1]
            first.append(d[0])
            line = d
        n = 0
        for k in first[::-1][1:]:
            n = k - n
        result += n
        # print(orig_line, first, n)

    print(f"Part 2: {result}")


if __name__ == "__main__":
    main()
