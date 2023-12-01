import re

from advent2023.helpers import read_input_as_lines


def part1(lines: list[str]) -> int:
    digit_re = re.compile(r"\d")
    retval = 0
    for line in lines:
        digits = digit_re.findall(line)
        retval += int(digits[0] + digits[-1])
    return retval


def part2(lines: list[str]) -> int:
    digits_names_english = dict(
        one=1,
        two=2,
        three=3,
        four=4,
        five=5,
        six=6,
        seven=7,
        eight=8,
        nine=9,
    )
    digit_re = re.compile(r"\d|" + "|".join(digits_names_english.keys()))
    retval = 0
    for line in lines:
        # this time is easier to use integers directly
        digits: list[int] = []
        # consume left to right until we find a digit
        start_pos = 0
        while start_pos < len(line):
            match = digit_re.search(line, start_pos)
            if match is None:
                break
            else:
                # I use start + 1 because digits may overlap
                # e.g. "eightwo" has to become 82
                start_pos = match.start() + 1
                if match.group().isdigit():
                    digits.append(int(match.group()))
                else:
                    digits.append(digits_names_english[match.group()])
        retval += digits[0] * 10 + digits[-1]
    return retval


if __name__ == "__main__":
    quiz_input = read_input_as_lines(__file__)
    print(part1(quiz_input))
    print(part2(quiz_input))
