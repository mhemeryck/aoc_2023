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

    # init the counts
    counts = np.zeros(maze.shape, dtype=np.int64)
    # all non-pipe locations are negative
    counts[maze == "."] = -1

    seed_idx = np.where(maze == "S")
    # keep a stack of candidates to check
    candidates = [(seed_idx[0][0], seed_idx[1][0])]
    while candidates:
        can_idx = candidates.pop()
        can = counts[can_idx]
        # north
        north_idx = can_idx[0] - 1, can_idx[1]
        try:
            north = maze[north_idx]
        except IndexError:
            pass
        else:
            if counts[north_idx] == 0 and north in ("7", "F", "|"):
                counts[north_idx] = can + 1
                candidates.append(north_idx)
        # south
        south_idx = can_idx[0] + 1, can_idx[1]
        try:
            south = maze[south_idx]
        except IndexError:
            pass
        else:
            if counts[south_idx] == 0 and south in ("J", "L", "|"):
                counts[south_idx] = can + 1
                candidates.append(south_idx)
        # east
        east_idx = can_idx[0], can_idx[1] + 1
        try:
            east = maze[east_idx]
        except IndexError:
            pass
        else:
            if counts[east_idx] == 0 and east in ("J", "7", "-"):
                counts[east_idx] = can + 1
                candidates.append(east_idx)
        # west
        west_idx = can_idx[0], can_idx[1] + 1
        try:
            west = maze[west_idx]
        except IndexError:
            pass
        else:
            if counts[west_idx] == 0 and west == ("L", "F", "-"):
                counts[west_idx] = can + 1
                candidates.append(west_idx)
        print(counts)

    result = np.max(counts)
    print("part 1: max value", result)


if __name__ == "__main__":
    main()
