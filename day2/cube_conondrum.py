import collections
import re
import typing

FILENAME: str = "input.txt"

AMOUNT_RED: int = 12
AMOUNT_GREEN: int = 13
AMOUNT_BLUE: int = 14

GAME_ID_REGEX: re.Pattern = re.compile(r"Game (\d+)")
COLOR_REGEX: re.Pattern = re.compile(r"(\d+) (red|green|blue)")


def main() -> None:
    with open(FILENAME, "r") as fh:
        lines = fh.read().splitlines()

    games: typing.Dict[int, typing.List[typing.Dict[str, int]]] = {}
    for line in lines:
        prefix, sets = line.split(":")

        # game id
        game_id = 0
        if (m := GAME_ID_REGEX.match(prefix)) is not None:
            game_id = int(m.group(1))

        # gamesets
        splits = [s.split(",") for s in sets.split(";")]
        game_sets: typing.List[typing.Dict[str, int]] = []
        for splt in splits:
            game_set: typing.Dict[str, int] = {}
            for s in splt:
                s = s.strip()
                if (m := COLOR_REGEX.match(s)) is not None:
                    number = int(m.group(1))
                    color = m.group(2)
                    game_set[color] = number
            game_sets.append(game_set)
        games[game_id] = game_sets

    # print(games)

    ids: typing.List[int] = []
    for game_id, game in games.items():
        if all(
            (gs.get("red", 0) <= AMOUNT_RED and gs.get("blue", 0) <= AMOUNT_BLUE and gs.get("green", 0) <= AMOUNT_GREEN)
            for gs in game
        ):
            ids.append(game_id)

    print(sum(ids))


if __name__ == "__main__":
    main()
