import typing
import numpy as np

DATA = """.....
.S-7.
.|.|.
.L-J.
....."""

DATA = """..F7.
.FJ|.
SJ.L7
|F--J
LJ..."""

DATA = """F-J
JS7
-J|"""

FILENAME: str = "input.txt"
with open(FILENAME, "r") as fh:
    DATA = fh.read()


def bound_check(x: int, y: int, x_max: int, y_max: int) -> bool:
    return 0 <= x < x_max and 0 <= y < y_max


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
        if bound_check(north_idx[0], north_idx[1], maze.shape[0], maze.shape[1]):
            north = maze[north_idx]
            if (counts[north_idx] == 0 or counts[north_idx] > can) and north in ("7", "F", "|"):
                counts[north_idx] = can + 1
                candidates.append(north_idx)
        # south
        south_idx = can_idx[0] + 1, can_idx[1]
        if bound_check(south_idx[0], south_idx[1], maze.shape[0], maze.shape[1]):
            south = maze[south_idx]
            if (counts[south_idx] == 0 or counts[south_idx] > can) and south in ("J", "L", "|"):
                counts[south_idx] = can + 1
                candidates.append(south_idx)
        # east
        east_idx = can_idx[0], can_idx[1] + 1
        if bound_check(east_idx[0], east_idx[1], maze.shape[0], maze.shape[1]):
            east = maze[east_idx]
            if (counts[east_idx] == 0 or counts[east_idx] > can) and east in ("J", "7", "-"):
                counts[east_idx] = can + 1
                candidates.append(east_idx)
        # west
        west_idx = can_idx[0], can_idx[1] - 1
        if bound_check(west_idx[0], west_idx[1], maze.shape[0], maze.shape[1]):
            west = maze[west_idx]
            if (counts[west_idx] == 0 or counts[west_idx] > can) and west in ("L", "F", "-"):
                counts[west_idx] = can + 1
                candidates.append(west_idx)
        # breakpoint()
        # print(
        #     counts[
        #         np.max([can_idx[0] - 10, 0]) : np.min([can_idx[0] + 11, counts.shape[0]]),
        #         np.max([can_idx[1] - 10, 0]) : np.min([can_idx[1] + 11, counts.shape[1]]),
        #     ]
        # )
        # print(counts)

    result = np.max(counts)
    print("part 1: max value", result)


if __name__ == "__main__":
    main()
