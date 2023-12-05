import typing
import collections

FILENAME: str = "input.txt"

with open(FILENAME, "r") as fh:
    LINES = fh.readlines()


Map = collections.namedtuple("Map", ("source", "target", "length"))


def main() -> None:
    # parse seeds
    seed_line = LINES[0].split(":")[1]
    seeds = [int(s) for s in seed_line.split(" ") if s]

    name = ""
    maps: typing.Dict[str, typing.List[map]] = {}
    for line in LINES[1:]:
        line = line.strip("\n")
        if "map" in line:
            name = line.split(" ")[0]
            maps[name] = []
        elif not line:
            name = ""
        elif name:
            source, target, length = line.split(" ")
            source = int(source)
            target = int(target)
            length = int(length)
            maps[name].append(Map(source=source, target=target, length=length))

    print(maps)


if __name__ == "__main__":
    main()
