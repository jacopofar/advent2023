import re

from advent2023.helpers import read_input_as_lines

CharactersPositions = dict[tuple[int, int], str]


def part1(parts_and_numbers: list[tuple[int, CharactersPositions]]) -> int:
    retval = 0
    for part_number, parts in parts_and_numbers:
        if len(parts) > 0:
            retval += part_number
    return retval


def part2(parts_and_numbers: list[tuple[int, CharactersPositions]]) -> int:
    # for each gear coordinate, list the parts adjacent to it
    gears_parts: dict[tuple[int, int], set[int]] = dict()
    for part_number, nearby_parts in parts_and_numbers:
        for part_coord, part_type in nearby_parts.items():
            if part_type == "*":
                if part_coord not in gears_parts:
                    gears_parts[part_coord] = set()
                gears_parts[part_coord].add(part_number)
    retval = 0
    for part_numbers in gears_parts.values():
        if len(part_numbers) == 2:
            retval += part_numbers.pop() * part_numbers.pop()
    return retval


def parse(my_path: str) -> list[tuple[int, CharactersPositions]]:
    lines = read_input_as_lines(my_path)
    number_re = re.compile(r"\d+")
    parts_positions: CharactersPositions = dict()
    for idx, line in enumerate(lines):
        for cidx, c in enumerate(line):
            if not c.isdigit() and c != ".":
                parts_positions[(cidx, idx)] = c
    number_and_parts: list[tuple[int, CharactersPositions]] = []
    for idx, line in enumerate(lines):
        for number in number_re.finditer(line):
            this_number_with_parts: tuple[int, CharactersPositions] = (
                int(number.group()),
                dict(),
            )
            start, end = number.span()
            # row above and below the number
            for x in range(start - 1, end + 1):
                if (x, idx - 1) in parts_positions:
                    this_number_with_parts[1][(x, idx - 1)] = parts_positions[
                        (x, idx - 1)
                    ]
                if (x, idx + 1) in parts_positions:
                    this_number_with_parts[1][(x, idx + 1)] = parts_positions[
                        (x, idx + 1)
                    ]
            # column left and right of the number
            if (start - 1, idx) in parts_positions:
                this_number_with_parts[1][(start - 1, idx)] = parts_positions[
                    (start - 1, idx)
                ]
            if (end, idx) in parts_positions:
                this_number_with_parts[1][(end, idx)] = parts_positions[(end, idx)]
            number_and_parts.append(this_number_with_parts)
    return number_and_parts


if __name__ == "__main__":
    quiz_input = parse(__file__)
    print(part1(quiz_input))
    print(part2(quiz_input))
