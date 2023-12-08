from itertools import cycle
from math import lcm

from advent2023.helpers import read_input_as_lines


def part1(problem: tuple[str, dict[str, tuple[str, str]]]) -> int:
    directions, network = problem
    pos = "AAA"
    steps = 0
    for dir in cycle(directions):
        pos = network[pos][0 if dir == "L" else 1]
        steps += 1
        if pos == "ZZZ":
            return steps
    raise ValueError("No solution found")


def find_cycle_sizes(
    start: str, steps: str, network: dict[str, tuple[str, str]]
) -> list[int]:
    position = start
    found_positions: set[tuple[int, str]] = set()
    found_distances: set[int] = set()

    distance = 0
    for idx, dir in cycle(enumerate(steps)):
        position = network[position][0 if dir == "L" else 1]
        distance += 1
        if position.endswith("Z"):
            # we found a value to add to the result
            # if it's already there we are cycling and we found all results
            if (idx, position) in found_positions:
                return sorted(found_distances)
            else:
                found_positions.add((idx, position))
                found_distances.add(distance)
                distance = 0
    raise ValueError("Infinite network???")


def part2(problem: tuple[str, dict[str, tuple[str, str]]]) -> int:
    directions, network = problem
    start_positions = [k for k in network.keys() if k.endswith("A")]
    cycle_sizes: list[int] = []
    for s in start_positions:
        cycles = find_cycle_sizes(s, directions, network)
        for c in cycles:
            cycle_sizes.append(c)

    return lcm(*cycle_sizes)


def parse(my_path: str, sample: bool = True) -> tuple[str, dict[str, tuple[str, str]]]:
    lines = read_input_as_lines(my_path, sample=sample)
    return (
        lines[0],
        {line[:3]: (line[7:10], line[12:15]) for line in lines[2:]},
    )


if __name__ == "__main__":
    quiz_input = parse(__file__, sample=False)
    print(part1(quiz_input))
    print(part2(quiz_input))
