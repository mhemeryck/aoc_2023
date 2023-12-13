import numpy as np

DATA = """.....
.S-7.
.|.|.
.L-J.
....."""

FILENAME: str = "input.txt"
with open(FILENAME, "r") as fh:
    DATA = fh.read()


def main() -> None:
    maze = np.array([np.array([c for c in line]) for line in DATA.splitlines()])
    print(maze)


if __name__ == "__main__":
    main()
