import re
import typing

with open("input.txt") as fh:
    LINES = fh.readlines()


# LINES = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
# Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
# Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
# Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
# Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
# Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11""".splitlines()


def part1() -> None:
    result = 0
    for line in LINES:
        game_id_str, payload = line.split(":")
        if m := re.match(r"Card\s+(\d+)", game_id_str):
            game_id = int(m.group(1))
        else:
            game_id = -1

        # parsing
        winning, actual = payload.split("|")
        winning = [int(n) for n in winning.split(" ") if n]
        actual = [int(n) for n in actual.split(" ") if n]

        line_count = sum(w in actual for w in winning)
        if line_count:
            result += 1 << (line_count - 1)

        print(game_id, winning, actual, line_count, result)
    print(result)


def main() -> None:
    result = 0
    # map of game id with line count
    line_counts: typing.Dict[int, int] = {}
    for line in LINES:
        game_id_str, payload = line.split(":")
        if m := re.match(r"Card\s+(\d+)", game_id_str):
            game_id = int(m.group(1))
        else:
            game_id = -1

        # parsing
        winning, actual = payload.split("|")
        winning = [int(n) for n in winning.split(" ") if n]
        actual = [int(n) for n in actual.split(" ") if n]

        line_count = sum(w in actual for w in winning)
        line_counts[game_id] = line_count

        print(game_id, winning, actual, line_count, result)
    # print(result)
    # print(line_counts)

    # Counts the number cards for a game card
    # Init with all game ids having one card
    counter: typing.Dict[int, int] = {game_id: 1 for game_id in line_counts.keys()}
    for game_id, line_count in line_counts.items():
        fro = game_id + 1
        to = game_id + line_count + 1

        for next_id in range(fro, to):
            counter[next_id] += counter[game_id]

    print(counter)
    print(sum(counter.values()))


if __name__ == "__main__":
    part1()
    # main()
