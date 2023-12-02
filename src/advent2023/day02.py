import re

from advent2023.helpers import read_input_as_lines


def is_possible(outcome: dict[str, int], bag: dict[str, int]) -> bool:
    for color, count in outcome.items():
        if color not in bag or bag[color] < count:
            return False
    return True


GameDescription = list[dict[str, int]]
Games = dict[int, list[dict[str, int]]]


def parse_games_description(lines: list[str]) -> Games:
    games: dict[int, list[dict[str, int]]] = {}
    for line in lines:
        gameid_s, _, outcomes = line.partition(":")
        for outcome in outcomes.split(";"):
            one_extraction: dict[str, int] = dict()
            for count_color in outcome.split(","):
                count, _, color = count_color.strip().partition(" ")
                one_extraction[color] = int(count)
            gameid = int(gameid_s[5:])
            if gameid not in games:
                games[gameid] = []
            games[gameid].append(one_extraction)
    return games


def part1(games: Games) -> int:
    retval = 0
    for gameid, extractions in games.items():
        if all(
            is_possible(outcome, dict(red=12, green=13, blue=14))
            for outcome in extractions
        ):
            retval += gameid
    return retval


def minimal_bag(game: GameDescription) -> dict[str, int]:
    minimal_bag = dict()
    for outcome in game:
        for color, count in outcome.items():
            if color not in minimal_bag:
                minimal_bag[color] = count
            else:
                minimal_bag[color] = max(count, minimal_bag[color])
    return minimal_bag


def part2(games: Games) -> int:
    retval = 0
    for game in games.values():
        minbag = minimal_bag(game)
        # get the product of all values in the dict
        power = 1
        for count in minbag.values():
            power *= count
        retval += power
    return retval


if __name__ == "__main__":
    quiz_input = parse_games_description(read_input_as_lines(__file__))
    print(part1(quiz_input))
    print(part2(quiz_input))
