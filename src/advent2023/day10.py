from advent2023.helpers import read_input_as_lines

DIRECTIONS = (1, 1j, -1, -1j)


def find_distances(
    start: complex, map: dict[complex, set[complex]]
) -> dict[complex, int]:
    # graph sarch but with a special case for loops
    # and some rules about how we move in it
    distances: dict[complex, int] = {start: 0}
    to_visit: set[complex] = set((start,))
    while len(to_visit) > 0:
        new_to_visit: set[complex] = set()
        for cell in to_visit:
            for dir in map[cell]:
                candidate_new = map.get(cell + dir)
                # there's nothing (out of bounds or dot)
                if candidate_new is None:
                    continue
                if (cell + dir) in distances:
                    continue
                if -dir in candidate_new:
                    # we found a new cell, mark the distance
                    distances[cell + dir] = distances[cell] + 1
                    new_to_visit.add(cell + dir)
        to_visit = new_to_visit
    return distances


def find_furthest_cell(distances: dict[complex, int]) -> tuple[complex, int]:
    # find the highest distance that also can be
    # reached from 2 different directions
    max_distance_so_far = -1
    corresponding_cell = 0j
    for cell, distance in distances.items():
        if distance > max_distance_so_far:
            incoming_count = 0
            for dir in DIRECTIONS:
                other_dist = distances.get(cell + dir, -1)
                if other_dist == distance - 1:
                    incoming_count += 1
            if incoming_count >= 2:
                max_distance_so_far = distance
                corresponding_cell = cell
    return corresponding_cell, max_distance_so_far


def visualize_map(
    distances: dict[complex, int], marked: dict[complex, str] | None = None
) -> None:
    for x in range(20):
        print(str(x).ljust(2, ".") + "  ", end=" ")
    print()
    for y in range(20):
        for x in range(20):
            val = str(distances.get(complex(x, y), "")).ljust(2, ".")
            print(f"{val}", end=" ")
            if marked is not None and complex(x, y) in marked:
                print(marked[complex(x, y)], end=" ")
            else:
                print(" ", end=" ")
        print(y)


def part1(
    problem: tuple[complex, dict[complex, set[complex]]], visualize: bool = False
) -> int:
    start, map = problem
    distances = find_distances(start, map)
    if visualize:
        visualize_map(distances)
    return find_furthest_cell(distances)[1]


def part2(
    problem: tuple[complex, dict[complex, set[complex]]], visualize: bool = False
) -> int:
    start, map = problem
    distances = find_distances(start, map)
    furthest_cell, max_distance = find_furthest_cell(distances)
    # now I want to find all the cells in the loop
    loop = set([furthest_cell])
    a = None
    b = None
    for dir in DIRECTIONS:
        if distances.get(furthest_cell + dir) == max_distance - 1:
            # we have to match exactly 2
            # the first we found goes into a, the second into b
            if a is None:
                a = furthest_cell + dir
            else:
                b = furthest_cell + dir
    current_distance = max_distance
    assert b is not None
    assert a is not None
    while current_distance > 1:
        current_distance -= 1
        loop.add(a)
        loop.add(b)
        nearby = set()
        # find for a and b what was the precursor in the loop
        for dir in DIRECTIONS:
            if distances.get(a + dir) == current_distance - 1:
                nearby.add(a + dir)
            if distances.get(b + dir) == current_distance - 1:
                nearby.add(b + dir)
        if current_distance > 1:
            assert len(nearby) == 2
            [a, b] = list(nearby)
        else:
            assert len(nearby) == 1
            loop.add(list(nearby)[0])
            break
    if visualize:
        visualize_map(distances, marked={l: "*" for l in loop})
    # check that we found exactly what we expected
    assert len(loop) == (2 * max_distance)
    # now we know the coordinates of the loop
    # we need to count how many "things" are inside
    # so for each row we scan what we find, and if we found an ODD number
    # of loop parts we are inside the loop, otherwise we are out
    # so first let's arrange the loop by real part
    # each scanline is a column in the input
    scanlines: dict[int, list[int]] = dict()
    for cell in loop:
        r, i = int(cell.real), int(cell.imag)
        if i not in scanlines:
            scanlines[i] = []
        # scanlines are "off". Scanline 0 is between line 0 and 1 of tiles
        # because we care about crossings of the pipe
        if complex(r, i - 1) in distances:
            if abs(distances[complex(r, i - 1)] - distances[complex(r, i)]) == 1:
                scanlines[i].append(r)

    if visualize:
        visualize_map(distances, marked={l: "*" for l in loop})
    # now let's scan the lines
    total_inside = 0
    for k in scanlines:
        line = scanlines[k]
        line.sort()
        assert len(line) % 2 == 0
        if len(line) == 0:
            continue
        # are we crossing horizontally, following the loop?
        # the inside is the distance between points
        # between 1st and 2nd is inside
        # between 3rd and 4th is outside
        # and so on
        found_here = 0
        for vi in range(0, len(line), 2):
            f, t = line[vi], line[vi + 1]
            for p in range(f, t):
                if not (complex(p, k) in distances):
                    found_here += 1
        total_inside += found_here
    return total_inside


def parse(
    my_path: str, sample: bool = True
) -> tuple[complex, dict[complex, set[complex]]]:
    map: dict[complex, set[complex]] = dict()
    start: complex = complex(0, 0)
    lines = read_input_as_lines(my_path, sample=sample)
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            # the map represents the coordinate that can be added
            # to the current position from the point of view of the cell
            # a movement is possible only if bofh from and to cell allow it
            if c == "S":
                start = complex(x, y)
                # all directions are valid
                map[complex(x, y)] = set((1j, -1j, 1, -1))
            elif c == "|":
                # vertical only
                map[complex(x, y)] = set((1j, -1j))
            elif c == "-":
                # horizontal only
                map[complex(x, y)] = set((1, -1))
            elif c == "L":
                map[complex(x, y)] = set((1, -1j))
            elif c == "J":
                map[complex(x, y)] = set((-1, -1j))
            elif c == "7":
                map[complex(x, y)] = set((-1, 1j))
            elif c == "F":
                map[complex(x, y)] = set((1, 1j))
            elif c == ".":
                continue
            else:
                raise ValueError(f"Unknown character {c}")
    return start, map


if __name__ == "__main__":
    quiz_input = parse(__file__, sample=False)
    print(part1(quiz_input))
    print(part2(quiz_input, visualize=False))
