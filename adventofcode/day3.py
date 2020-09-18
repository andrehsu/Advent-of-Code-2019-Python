from typing import Tuple, Dict

from utils import read_input_lines

INPUT = read_input_lines(3)

Point = Tuple[int, int]
WirePoints = Dict[Point, int]


def part1(wire1: WirePoints, wire2: WirePoints) -> int:
    def dist(point: Point) -> int:
        x, y = point
        return abs(x) + abs(y)
    
    return min(map(dist, set(wire1.keys()).intersection(wire2)))


def part2(wire1: WirePoints, wire2: WirePoints) -> int:
    return min(wire1[point] + wire2[point] for point in set(wire1.keys()).intersection(wire2.keys()))


def get_wire_points(wire_str: str) -> WirePoints:
    points = {}
    x = 0
    y = 0
    i_step = 0

    for step in wire_str.split(','):
        direction = step[0]
        dist = int(step[1:])
        for _ in range(dist):
            if direction == 'U':
                y += 1
            elif direction == 'D':
                y -= 1
            elif direction == 'L':
                x -= 1
            elif direction == 'R':
                x += 1
            else:
                raise RuntimeError('Unknown direction')

            i_step += 1

            point = x, y
            if point not in points:
                points[point] = i_step

    return points


if __name__ == '__main__':
    wire1 = get_wire_points(INPUT[0])
    wire2 = get_wire_points(INPUT[1])
    print(part1(wire1, wire2))
    print(part2(wire1, wire2))
