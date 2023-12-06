from math import ceil, floor
from advent2023.helpers import read_input_as_lines


def count_winning_times(t: int, d: int) -> int:
    r: float = (t**2 - d * 4) ** 0.5
    print(f"for {t} and {d} we have:")
    print((t - r) / 2, (t + r) / 2)
    min_press = (t - r) / 2
    if int(min_press) == min_press:
        # not winning, it's a tie, ignore this value
        min_press = int(min_press) + 1
    else:
        min_press = ceil(min_press)
    max_press = (t + r) / 2
    if int(max_press) == max_press:
        # not winning, it's a tie, ignore this value
        max_press = int(max_press) - 1
    else:
        max_press = floor(max_press)
    print(f"press between {min_press} and {max_press}")
    ways_to_win = max_press - min_press + 1
    return ways_to_win


def part1(time_dist: list[tuple[int, int]]) -> int:
    # if the total time is T, pressing the button for a time t
    # means distance will be t(T- t) = tT - t^2
    # so we reach distance d when tT - t^2 = d
    # solving by t = (T +/- sqrt(T^2 - 4d)) / 2
    # then we need to ignore negative and consider only the integers
    retval = 1
    for t, d in time_dist:
        ways_to_win = count_winning_times(t, d)
        print(ways_to_win)
        retval *= ways_to_win
    return retval


def part2(time_dist: list[tuple[int, int]]) -> int:
    total_time = int("".join(str(t) for t, _ in time_dist))
    total_dist = int("".join(str(d) for _, d in time_dist))
    return count_winning_times(total_time, total_dist)


def parse(my_path: str, sample: bool = True) -> list[tuple[int, int]]:
    lines = read_input_as_lines(my_path, sample=sample)
    times = [int(t) for t in lines[0].partition("Time: ")[2].split()]
    distances = [int(t) for t in lines[1].partition("Distance: ")[2].split()]
    return list(zip(times, distances))


if __name__ == "__main__":
    quiz_input = parse(__file__, sample=False)
    print(quiz_input)
    print(part1(quiz_input))
    print(part2(quiz_input))
