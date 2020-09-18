import math
from collections import Counter
from functools import lru_cache
from operator import itemgetter
from typing import List, Tuple

from utils import read_input_lines, test_case

INPUT = read_input_lines(10)

Pos = Tuple[int, int]


def parse_asteroids(inp: List[str]) -> List[Pos]:
    asteroids = [(x, y) for y, row in enumerate(inp) for x, v in enumerate(row) if v == '#']
    
    return asteroids


@lru_cache(maxsize=None)
def angle_between(a: Pos, b: Pos) -> float:
    ax, ay = a
    bx, by = b
    
    angle = math.atan2(-by - -ay, bx - ax) * 180 / math.pi
    
    angle -= 90
    
    if angle < 0:
        angle += 360
    
    angle = 360 - angle
    if angle == 360:
        angle = 0
    
    return angle


def best_spot(asteroids: List[Pos]) -> Tuple[Pos, int]:
    def is_visible(a: Pos, b: Pos) -> bool:
        if b > a:
            return _is_visible(b, a)
        else:
            return _is_visible(a, b)
    
    # noinspection DuplicatedCode
    @lru_cache(maxsize=None)
    def _is_visible(a: Pos, b: Pos) -> bool:
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
    
    counts = Counter()
    
    for a in asteroids:
        for b in asteroids:
            if is_visible(a, b):
                counts[a] += 1
    
    pos, count = counts.most_common(1)[0]
    
    return pos, count - 1


def part1(inp: List[str]) -> None:
    asteroids = parse_asteroids(inp)
    
    print(best_spot(asteroids)[1])


def part2(inp: List[str]) -> None:
    asteroids = parse_asteroids(inp)
    
    station = best_spot(asteroids)[0]
    
    asteroids.remove(station)
    
    # noinspection DuplicatedCode
    def is_visible(a: Pos, b: Pos) -> bool:
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
    
    last = None
    deg = 0
    for i in range(200):
        angles = [(angle_between(station, a), a) for a in asteroids if is_visible(station, a)]
        angles = filter(lambda x: x[0] >= deg, angles)
        
        if not angles:
            deg = 0
            continue
        
        angle, ast = min(angles, key=itemgetter(0))
        last = ast
        deg = angle + 0.0001
        print(f'{i + 1}th asteroid: {last} at deg {angle:.2f}')
        asteroids.remove(ast)
    
    print(last)
    
    print(last[0] * 100 + last[1])


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
    # part1(INPUT)
    part2(INPUT)
