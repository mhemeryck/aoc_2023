import numpy as np

FILENAME: str = "example.txt"

with open(FILENAME, "r") as fh:
    LINES = fh.readlines()


def main() -> None:
    # parsing
    lines = np.array([[int(i) for i in line.split(" ")] for line in LINES])

    results = np.zeros(lines.shape[0])
    for k, line in enumerate(lines):
        last = [line[-1]]
        while not np.all(line == 0):
            d = np.diff(line)
            last.append(d[-1])
            line = d
        print(k, line, last)


if __name__ == "__main__":
    main()
