from advent2023.helpers import read_input_as_lines


def diff(values: list[int]) -> list[int]:
    return [values[i + 1] - values[i] for i in range(len(values) - 1)]


def get_pyramid(hist: list[int]) -> list[list[int]]:
    pyramid = [hist]
    new_line = diff(hist)
    # it's not really necessary to calculate all of this
    # but they are so small that it doesn't matter
    while any(n != 0 for n in new_line):
        pyramid.append(new_line)
        new_line = diff(new_line)
    return pyramid


def part1(problem: list[list[int]]) -> int:
    retval = 0
    for hist in problem:
        pyramid = get_pyramid(hist)
        extrapolated = [0]
        for i in range(len(pyramid)):
            extrapolated.append(extrapolated[-1] + pyramid[-i - 1][-1])
        retval += extrapolated[-1]
    return retval


def part2(problem: list[list[int]]) -> int:
    retval = 0
    for hist in problem:
        pyramid = get_pyramid(hist)
        extrapolated = [0]
        for i in range(len(pyramid)):
            extrapolated.append(pyramid[-i - 1][0] - extrapolated[-1])
        retval += extrapolated[-1]
    return retval


def parse(my_path: str, sample: bool = True) -> list[list[int]]:
    lines = read_input_as_lines(my_path, sample=sample)
    return [[int(n) for n in line.split()] for line in lines]


if __name__ == "__main__":
    quiz_input = parse(__file__, sample=False)
    print(part1(quiz_input))
    print(part2(quiz_input))
