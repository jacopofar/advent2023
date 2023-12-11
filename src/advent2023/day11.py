from advent2023.helpers import read_input_as_lines


def expand_space(
    problem: list[tuple[int, int]], factor: int = 2
) -> list[tuple[int, int]]:
    used_x = set(x for x, _ in problem)
    used_y = set(y for _, y in problem)
    retval = []
    for x, y in problem:
        retval.append(
            (
                x + (factor - 1) * (x - sum(1 for a in used_x if a < x)),
                y + (factor - 1) * (y - sum(1 for a in used_y if a < y)),
            )
        )
    return retval


def part1(problem: list[tuple[int, int]]) -> int:
    p = expand_space(problem)
    distance_sum = 0
    for i1 in range(len(p)):
        for i2 in range(i1):
            g1, g2 = p[i1], p[i2]
            distance_sum += abs(g1[0] - g2[0]) + abs(g1[1] - g2[1])
    return distance_sum


def part2(problem: list[tuple[int, int]]) -> int:
    p = expand_space(problem, factor=1_000_000)
    distance_sum = 0
    for i1 in range(len(p)):
        for i2 in range(i1):
            g1, g2 = p[i1], p[i2]
            distance_sum += abs(g1[0] - g2[0]) + abs(g1[1] - g2[1])
    return distance_sum


def parse(my_path: str, sample: bool = True) -> list[tuple[int, int]]:
    # the list is already sorted in reading order
    lines = read_input_as_lines(my_path, sample=sample)
    retval = []
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == "#":
                retval.append((y, x))
    return retval


if __name__ == "__main__":
    quiz_input = parse(__file__, sample=False)
    print(part1(quiz_input))
    print(part2(quiz_input))
