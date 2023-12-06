from advent2023.helpers import read_input_as_lines

AlmanacMap = list[tuple[int, int, int]]
ProblemDescription = tuple[list[int], list[tuple[str, AlmanacMap]]]


def map_seed(seed: int, map: AlmanacMap) -> int:
    for dest, source, length in map:
        if seed >= source and seed < source + length:
            return dest + seed - source
    return seed


def map_range(
    seed_start: int,
    seed_end: int,
    map: AlmanacMap,
) -> list[tuple[int, int]]:
    """Given a seed range X..Y and a mapping, return a list of mapped
    ranges. Mapping can break the topology of a range, so we return many.
    """
    result = []
    consume_start = seed_start
    # NOTE: mapping is sorted by source, so we see the mapping in increasing
    # order. They cannot overlap or the result would be ambiguous
    for dest, source, length in map:
        # we process in a greedy way the mappings, producing the corresponding
        # remapped ranges and moving the consume_start to mark what we processed
        # so far
        # the mapping source is completely before the range
        if seed_end < source:
            # we are done, all next mappings are after the range
            result.append((consume_start, seed_end))
            return result
        # the range starts before the mapping source, consume it
        if consume_start < source:
            # we have a range from consume_start to source - 1
            result.append((consume_start, source - 1))
            consume_start = source
        # now we are consuming the inside of the overlap
        # add the overlap range, if any
        if source + length >= consume_start:
            result.append(
                (
                    max(consume_start, source) + (dest - source),
                    min(seed_end, source + length) + (dest - source),
                )
            )
            # move to the end of this mapping
            consume_start = source + length + 1
        # did we reach the end? stop
        if consume_start >= seed_end:
            return result
    # we are done with the mappings, add the remaining range
    result.append((consume_start, seed_end))

    return result


def part1(almanac: ProblemDescription) -> int:
    current_seeds = almanac[0]
    for _map_name, map in almanac[1]:
        new_seeds = []
        for seed in current_seeds:
            mapped_seed = map_seed(seed, map)
            new_seeds.append(mapped_seed)
        current_seeds = new_seeds
    return min(current_seeds)


def part2(almanac: ProblemDescription) -> int:
    current_seed_ranges: list[tuple[int, int]] = []
    for idx in range(len(almanac[0])):
        if idx % 2 == 0:
            current_seed_ranges.append(
                (
                    almanac[0][idx],
                    # the range is inclusive
                    almanac[0][idx] + almanac[0][idx + 1] - 1,
                )
            )
    # print('seed ranges:', current_seed_ranges)

    for map_name, map in almanac[1]:
        # print(map_name, map)
        new_seed_ranges = []
        # print('before mapping', current_seed_ranges)
        for start, end in current_seed_ranges:
            mapped_ranges = map_range(start, end, map)
            new_seed_ranges += mapped_ranges
        # print('remapped ranges:', new_seed_ranges)
        current_seed_ranges = new_seed_ranges
    return min(n[0] for n in new_seed_ranges) - 1


def parse(my_path: str, sample: bool = True) -> ProblemDescription:
    """Return a tuple of (seed_numbers, found_maps).
    seed_numbers is a list of integers
    found_maps is a list of tuples of (map_name, map_entries)
    map_entries is a list of tuples of (dest, source, length)
    map_entries is sorted by source
    """
    lines = read_input_as_lines(my_path, sample=sample)
    seed_numbers = [int(n) for n in lines[0].partition(": ")[2].split()]
    found_maps: list[tuple[str, AlmanacMap]] = []
    current_map_name = None
    current_map_entries: AlmanacMap = []
    for l in lines[1:]:
        if l.endswith(" map:"):
            if current_map_name is not None:
                current_map_entries.sort(key=lambda e: e[1])
                found_maps.append((current_map_name, current_map_entries))
                current_map_entries = []
            current_map_name = l.replace(" map:", "")
        elif l == "":
            continue
        else:
            parts = l.split()
            assert len(parts) == 3
            # NOTE mypy cannot detect that the assert above makes sure that
            # this is a tuple of 3 ints
            current_map_entries.append(tuple(int(p) for p in parts))  # type: ignore
    # add the last map to be seen
    current_map_entries.sort(key=lambda e: e[1])
    assert current_map_name is not None
    found_maps.append((current_map_name, current_map_entries))

    return seed_numbers, found_maps


if __name__ == "__main__":
    # some checks, I don't want to implement tests for this :)
    # assert map_range(100, 200, [(30, 20, 15)]) == [(100, 200)]
    # assert map_range(3, 200, [(30, 20, 15)]) == [(3, 19), (30, 45), (36, 200)]
    # assert map_range(3, 25, [(30, 20, 15)]) == [(3, 19), (30, 35)]
    # assert map_range(3, 25, [(30, 60, 15)]) == [(3, 25)]
    # assert map_range(25, 30, [(1000, 20, 16)]) == [(1005, 1010)]
    # assert map_range(25, 30, [(1000, 20, 100)]) == [(1005, 1010)]
    quiz_input = parse(__file__, sample=False)
    print(part1(quiz_input))
    print(part2(quiz_input))
