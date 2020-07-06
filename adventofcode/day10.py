from typing import List, Tuple

from utils import read_input, test_case

INPUT = read_input(10)

Map = List[List[bool]]
Pos = Tuple[int, int]


def parse_map(inp: List[str]) -> Map:
    return [[i == '#' for i in row] for row in inp]


def print_map(space_map: Map) -> None:
    for row in space_map:
        for i in row:
            if i:
                print('#', end='')
            else:
                print('.', end='')
        print()


def is_visible(asteroids: List[Pos], a: Pos, b: Pos) -> bool:
    ax, ay = a
    bx, by = b
    for c in asteroids:
        cx, cy = c
        if ((cy - ay) * (bx - ax) - (cx - ax) * (by - ay) == 0 and
                (ax <= cx <= bx or ax >= cx >= bx) and
                (ay <= cy <= by or ay >= cy >= by) and
                len({a, b, c}) == 3):
            return False
    return True


def part1(inp: List[str]) -> None:
    space_map = parse_map(inp)

    asteroids = [(r, c) for r, row in enumerate(space_map) for c, v in enumerate(row) if v]
    
    visible = {}
    
    for a in asteroids:
        for b in asteroids:
            if a != b and (a, b) not in visible and (b, a) not in visible:
                visibility = is_visible(asteroids, a, b)
                visible[(a, b)] = visibility
                visible[(b, a)] = visibility
    
    counts = {}
    
    for a in asteroids:
        counts[a] = 0
        for b in asteroids:
            if a != b and visible[(a, b)]:
                counts[a] += 1
    
    print(max(counts.values()))


test0 = test_case('''
.#..#
.....
#####
....#
...##
''')

test1 = test_case('''
.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##
''')

if __name__ == '__main__':
    # part1(test0)
    # part1(test1)
    part1(INPUT)
