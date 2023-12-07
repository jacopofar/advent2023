from collections import Counter

from advent2023.helpers import read_input_as_lines

CARD_VALUES = {
    "2": 1,
    "3": 2,
    "4": 3,
    "5": 4,
    "6": 5,
    "7": 6,
    "8": 7,
    "9": 8,
    "T": 9,
    "J": 10,
    "Q": 11,
    "K": 12,
    "A": 13,
}
# give the card valus combinations a lofty 100M range, easier to troubleshoot
HAND_TYPES = {
    "11111": 0,
    "2111": 100_000_000,
    "221": 200_000_000,
    "311": 300_000_000,
    "32": 400_000_000,
    "41": 500_000_000,
    "5": 600_000_000,
}


def hand_absolute_score(hand: str, joker_twist: bool = False) -> int:
    # first calculate the "variety" of this hand
    value_types: list[int] = [v[1] for v in Counter(hand).most_common()]
    if joker_twist:
        joker_count = hand.count("J")
        remaining_hand = hand.replace("J", "")
        value_types = [v[1] for v in Counter(remaining_hand).most_common()]
        if len(value_types) == 0:
            # special case, ALL jokers, becomes a five of a kind
            value_types = [5]
        else:
            value_types[0] += joker_count
    assert sum(value_types) == 5
    hand_type = "".join([str(v) for v in value_types])
    # now the score of the cards
    pos_mul = 1
    hand_score = 0
    for card in reversed(hand):
        if not (joker_twist and card == "J"):
            hand_score += CARD_VALUES[card] * pos_mul
        pos_mul *= 14
    return HAND_TYPES[hand_type] + hand_score


def sort_and_get_score(hands: list[tuple[str, int]], joker_twist: bool = False) -> int:
    # sort cards by their score
    hands.sort(key=lambda x: hand_absolute_score(x[0], joker_twist=joker_twist))
    # for h, sc in hands:
    #     print(h, hand_absolute_score(h, joker_twist=joker_twist))
    # sum the scores multiplied by the ranks
    retval = 0
    for rank, hand in enumerate(hands):
        retval += (rank + 1) * hand[1]
    return retval


def part1(hands: list[tuple[str, int]]) -> int:
    return sort_and_get_score(hands)


def part2(hands: list[tuple[str, int]]) -> int:
    return sort_and_get_score(hands, joker_twist=True)


def parse(my_path: str, sample: bool = True) -> list[tuple[str, int]]:
    lines = read_input_as_lines(my_path, sample=sample)
    retval = []
    for line in lines:
        cards, bid = line.split()
        retval.append((cards, int(bid)))
    return retval


if __name__ == "__main__":
    assert hand_absolute_score("JKKK2") < hand_absolute_score("QQQQ2")
    quiz_input = parse(__file__, sample=False)
    print(part1(quiz_input))
    print(part2(quiz_input))
