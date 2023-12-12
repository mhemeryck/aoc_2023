import numpy as np

# FILENAME: str = "example.txt"
FILENAME: str = "input.txt"

with open(FILENAME, "r") as fh:
    LINES = fh.readlines()


def main() -> None:
    # parsing
    lines = np.array([[int(i) for i in line.split(" ")] for line in LINES])

    # sum all last diffs
    result = 0
    for line in lines:
        result += line[-1]
        while not np.all(line == 0):
            d = np.diff(line)
            result += d[-1]
            line = d

    print(f"Part 1: {result}")


if __name__ == "__main__":
    main()
