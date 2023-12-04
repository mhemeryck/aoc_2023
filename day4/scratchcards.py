with open("input.txt") as fh:
    LINES = fh.readlines()


def main() -> None:
    for line in LINES:
        game_id, payload = line.split(":")
        # parsing
        winning, actual = payload.split("|")
        winning = [int(n) for n in winning.split(" ") if n]
        actual = [int(n) for n in actual.split(" ") if n]

        line_count = 0
        for w in winning:
            if w in actual:
                line_count += 1

        print(game_id, winning, actual, line_count)


if __name__ == "__main__":
    main()
