import collections
import logging
import logging.config
import multiprocessing
import sys
import typing


LOG_LEVEL = logging.INFO
LOG_CONFIG = dict(
    version=1,
    formatters={"default": {"format": "%(asctime)s - %(levelname)s -  %(message)s"}},
    handlers={
        "stream": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "level": LOG_LEVEL,
        }
    },
    root={"handlers": ["stream"], "level": LOG_LEVEL},
)
logging.config.dictConfig(LOG_CONFIG)
logger = logging.getLogger(__name__)


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
        # prev = seed
        seed = apply(seed, map)
        # if debug:
        #     logger.debug("\t", prev, "->", map_name, "->", seed)
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
    nseeds,
) -> None:
    for seed in range(seed_range.offset, seed_range.offset + seed_range.length):
        # logger.debug(f"putting seed {seed}")
        q.put(seed)
        nseeds.value += 1

        if nseeds.value % 1000 == 0:
            logger.debug(f"produced {nseeds.value}")


def consumer(
    q: multiprocessing.Queue, maps: collections.OrderedDict[str, typing.List[Map]], minimum, nseeds, max_nseeds
) -> None:
    logger.debug("starting consumer")
    while True:
        seed = q.get()
        nseeds.value += 1
        if seed is None:
            break

        location = location_for_seed(seed, maps)
        minimum.value = min(minimum.value, location)
        if location == minimum.value:
            logger.info(f"new minimum: {location}")

        if nseeds.value % 1000 == 0:
            logger.debug(f"consumed {nseeds.value} / {max_nseeds} ({nseeds.value / max_nseeds * 100.0:0.2f} %)")


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

    logger.debug("minimum of all results: %d", min(results))

    # part 2: rewrap seeds to ranges
    seed_ranges = remap_seeds(seeds)

    max_nseeds = sum(sr.length for sr in seed_ranges)

    with multiprocessing.Manager() as manager:
        minimum = manager.Value("i", sys.maxsize)
        nseeds_produced = manager.Value("i", 0)
        nseeds_consumed = manager.Value("i", 0)

        q = multiprocessing.Queue()

        producers = [
            multiprocessing.Process(target=producer, args=(q, seed_range, nseeds_produced))
            for seed_range in seed_ranges
        ]
        consumers = [
            multiprocessing.Process(target=consumer, args=(q, maps, minimum, nseeds_consumed, max_nseeds))
            for _ in range(8)
        ]

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

        logger.info(minimum.value)

    # # part 2: process per seed range
    # for i, seed_range in enumerate(seed_ranges):
    #     logger.debug(f"Processing range {i}")
    #     for seed in range(seed_range.offset, seed_range.offset + seed_range.length):
    #         location = location_for_seed(seed, maps)
    #         minimum = min(minimum, location)
    #         if location == minimum:
    #             logger.debug(seed, location, minimum)
    # logger.debug(minimum)


if __name__ == "__main__":
    main()
