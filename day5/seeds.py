import collections
import multiprocessing
import sys
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
SeedRange = collections.namedtuple("SeedRange", ("offset", "length"))


def location_for_seed(seed: int, maps: collections.OrderedDict[str, typing.List[Map]], debug: bool = False) -> int:
    """apply all maps for a given seed"""
    for map_name, map in maps.items():
        prev = seed
        seed = apply(seed, map)
        if debug:
            print("\t", prev, "->", map_name, "->", seed)
    return seed


def apply(source: int, map: typing.List[Map]) -> int:
    """applies a list of maps to a given source"""
    for m in map:
        if m.source <= source <= m.source + m.length:
            return m.target + (source - m.source)
    return source


def remap_seeds(seeds: typing.List[int]) -> typing.List[SeedRange]:
    result = []
    offset, length = 0, 0
    for n, seed in enumerate(seeds):
        if n % 2 == 0:
            offset = seed
        else:
            length = seed
            result.append(SeedRange(offset=offset, length=length))

    return result


def producer(
    q: multiprocessing.Queue,
    seed_range: SeedRange,
) -> None:
    for seed in range(seed_range.offset, seed_range.offset + seed_range.length):
        # print(f"putting seed {seed}")
        q.put(seed)


def consumer(
    q: multiprocessing.Queue,
    maps: collections.OrderedDict[str, typing.List[Map]],
    minimum,
) -> None:
    print("starting consumer")
    while True:
        seed = q.get()
        if seed is None:
            break

        location = location_for_seed(seed, maps)
        minimum.value = min(minimum.value, location)
        if location == minimum.value:
            print(f"new minimum: {location}")


def main() -> None:
    # parse seeds
    seed_line = LINES[0].split(":")[1]
    seeds = [int(s) for s in seed_line.split(" ") if s]

    # Parse the maps
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

    # part 1
    results = []
    for seed in seeds:
        location = location_for_seed(seed, maps)
        results.append(location)

    print("minimum of all results:", min(results))

    # part 2: rewrap seeds to ranges
    seed_ranges = remap_seeds(seeds)

    with multiprocessing.Manager() as manager:
        minimum = manager.Value("i", sys.maxsize)
        q = multiprocessing.Queue()

        producers = [multiprocessing.Process(target=producer, args=(q, seed_range)) for seed_range in seed_ranges]
        consumers = [multiprocessing.Process(target=consumer, args=(q, maps, minimum)) for _ in range(8)]

        for p in producers:
            p.start()

        for c in consumers:
            c.start()

        for p in producers:
            p.join()

        for _ in range(len(consumers)):
            q.put(None)

        for c in consumers:
            c.join()

        print(minimum.value)

    # # part 2: process per seed range
    # for i, seed_range in enumerate(seed_ranges):
    #     print(f"Processing range {i}")
    #     for seed in range(seed_range.offset, seed_range.offset + seed_range.length):
    #         location = location_for_seed(seed, maps)
    #         minimum = min(minimum, location)
    #         if location == minimum:
    #             print(seed, location, minimum)
    # print(minimum)


if __name__ == "__main__":
    main()
