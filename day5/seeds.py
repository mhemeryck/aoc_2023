import collections
import typing

FILENAME: str = "input.txt"

with open(FILENAME, "r") as fh:
    LINES = fh.readlines()


# LINES = """seeds: 79 14 55 13

# seed-to-soil map:
# 50 98 2
# 52 50 48

# soil-to-fertilizer map:
# 0 15 37
# 37 52 2
# 39 0 15

# fertilizer-to-water map:
# 49 53 8
# 0 11 42
# 42 0 7
# 57 7 4

# water-to-light map:
# 88 18 7
# 18 25 70

# light-to-temperature map:
# 45 77 23
# 81 45 19
# 68 64 13

# temperature-to-humidity map:
# 0 69 1
# 1 0 69

# humidity-to-location map:
# 60 56 37
# 56 93 4""".splitlines()


Map = collections.namedtuple("Map", ("source", "target", "length"))


def apply(source: int, map: typing.List[Map]) -> int:
    """applies a list of maps to a given source"""
    for m in map:
        if m.source <= source <= m.source + m.length:
            return m.target + (source - m.source)
    return source


def main() -> None:
    # parse seeds
    seed_line = LINES[0].split(":")[1]
    seeds = [int(s) for s in seed_line.split(" ") if s]

    name = ""
    maps: collections.OrderedDict[str, typing.List[Map]] = collections.OrderedDict()
    for line in LINES[1:]:
        line = line.strip("\n")
        if "map" in line:
            # start new map
            name = line.split(" ")[0]
            maps[name] = []
        elif not line:
            # end a map
            name = ""
        elif name:
            # inside of a map
            target, source, length = line.split(" ")
            maps[name].append(Map(source=int(source), target=int(target), length=int(length)))

    # print(maps)

    results = []
    for seed in seeds:
        print(seed)
        for map_name, map in maps.items():
            prev = seed
            seed = apply(seed, map)
            print("\t", prev, "->", map_name, "->", seed)
        results.append(seed)

    print("minimum of all results:", min(results))


if __name__ == "__main__":
    main()
