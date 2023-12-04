import re

from advent2023.helpers import read_input_as_lines

Card = tuple[set[int], set[int]]


def part1(cards: list[Card]) -> int:
    retval = 0
    for winners, numbers_we_have in cards:
        matches = len(winners & numbers_we_have)
        if matches > 0:
            retval += 2 ** (matches - 1)
    return retval


def part2(cards: list[Card]) -> int:
    retval = 0
    # how many copies do we have for the next cards? Assume 1 by default
    multipliers = [1] * len(cards[0][0])
    for winners, numbers_we_have in cards:
        # multiplier for this card
        multiplier = multipliers.pop(0)
        multipliers.append(1)
        # count the scratches
        retval += multiplier

        matches = len(winners & numbers_we_have)
        if matches > 0:
            for idx in range(matches):
                multipliers[idx] += multiplier
    return retval


def parse(my_path: str, sample: bool = False) -> list[Card]:
    lines = read_input_as_lines(my_path, sample=sample)
    retval = []
    for line in lines:
        numbers = line.partition(": ")[2]
        winners, _, numbers_we_have = numbers.partition("|")
        retval.append(
            (
                set(int(n) for n in winners.split()),
                set(int(n) for n in numbers_we_have.split()),
            )
        )
    return retval


if __name__ == "__main__":
    quiz_input = parse(__file__, sample=False)
    print(part1(quiz_input))
    print(part2(quiz_input))
