import enum

import numpy as np

DATA = """.....
.S-7.
.|.|.
.L-J.
....."""

# DATA = """..F7.
# .FJ|.
# SJ.L7
# |F--J
# LJ..."""

# DATA = """F-J
# JS7
# -J|"""

FILENAME: str = "input.txt"
with open(FILENAME, "r") as fh:
    DATA = fh.read()


# DATA = """FF7FSF7F7F7F7F7F---7
# L|LJ||||||||||||F--J
# FL-7LJLJ||||||LJL-77
# F--JF--7||LJLJ7F7FJ-
# L---JF-JLJ.||-FJLJJ7
# |F|F-JF---7F7-L7L|7|
# |FFJF7L7F-JF7|JL---7
# 7-L-JL7||F7|L7F-7F7|
# L.L7LFJ|||||FJL7||LJ
# L7JLJL-JLJLJL--JLJ.L"""


MAZE = np.array([np.array([c for c in line]) for line in DATA.splitlines()])
X_MAX, Y_MAX = MAZE.shape


class Direction(enum.Enum):
    NORTH = 1
    EAST = 2
    WEST = 3
    SOUTH = 4


def bound_check(x: int, y: int) -> bool:
    return 0 <= x < X_MAX and 0 <= y < Y_MAX


def north(idx):
    new = idx[0] - 1, idx[1]
    if bound_check(*new):
        return new


def south(idx):
    new = idx[0] + 1, idx[1]
    if bound_check(*new):
        return new


def east(idx):
    new = idx[0], idx[1] + 1
    if bound_check(*new):
        return new


def west(idx):
    new = idx[0], idx[1] - 1
    if bound_check(*new):
        return new


def find_first(idx):
    north_idx = north(idx)
    if north_idx:
        value = MAZE[north_idx]
        if value in ("7", "F", "|"):
            return north_idx, Direction.NORTH

    south_idx = south(idx)
    if south_idx:
        value = MAZE[south_idx]
        if value in ("J", "L", "|"):
            return south_idx, Direction.SOUTH

    east_idx = east(idx)
    if east_idx:
        value = MAZE[east_idx]
        if value in ("J", "7", "-"):
            return east_idx, Direction.EAST

    west_idx = west(idx)
    if west_idx:
        value = MAZE[west_idx]
        if value in ("L", "F", "-"):
            return west_idx, Direction.WEST

    return None, None


def main() -> None:
    # MAZE = np.array([np.array([c for c in line]) for line in DATA.splitlines()])

    seed_idx = np.where(MAZE == "S")
    seed = MAZE[seed_idx]

    seed_idx = (seed_idx[0][0], seed_idx[1][0])
    # find first neighbor
    current, direction = find_first(seed_idx)
    if current is None:
        return
    path = [current]

    while MAZE[current] != seed:
        match MAZE[current], direction:
            case "S":
                break
            case "7", Direction.EAST:
                current, direction = south(current), Direction.SOUTH
            case "7", Direction.NORTH:
                current, direction = west(current), Direction.WEST
            case "|", Direction.SOUTH:
                current, direction = south(current), Direction.SOUTH
            case "|", Direction.NORTH:
                current, direction = north(current), Direction.NORTH
            case "-", Direction.EAST:
                current, direction = east(current), Direction.EAST
            case "-", Direction.WEST:
                current, direction = west(current), Direction.WEST
            case "J", Direction.SOUTH:
                current, direction = west(current), Direction.WEST
            case "J", Direction.EAST:
                current, direction = north(current), Direction.NORTH
            case "F", Direction.WEST:
                current, direction = south(current), Direction.SOUTH
            case "F", Direction.NORTH:
                current, direction = east(current), Direction.EAST
            case "L", Direction.SOUTH:
                current, direction = east(current), Direction.EAST
            case "L", Direction.WEST:
                current, direction = north(current), Direction.NORTH

        # print(current, direction, MAZE[current])
        if current:
            path.append(current)

    result = len(path) // 2
    print(f"Result part 1: {result}")
    # part 2: area

    # shoelace formula: sum of determinants
    points = np.array(path).T
    area = 0
    for k in range(points.shape[1] - 2):
        area += np.linalg.det(points[:, k : k + 2])
    # last and first point
    area += np.linalg.det(points[:, [points.shape[1] - 1, 0]])
    outer = int(np.abs(area) // 2)

    # pick formula:
    i = outer - result + 1
    print(f"Result part 2: inner number of points: {i}")


if __name__ == "__main__":
    main()
