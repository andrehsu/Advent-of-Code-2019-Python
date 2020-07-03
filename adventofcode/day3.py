from utils import read_input

INPUT = read_input(3)


def part1(wire1, wire2):
    def dist(point):
        x, y = point
        return abs(x) + abs(y)

    return min(map(dist, set(wire1.keys()).intersection(wire2)))


def part2(wire1, wire2):
    return min(wire1[point] + wire2[point] for point in set(wire1.keys()).intersection(wire2.keys()))


def get_wire_points(wire_str):
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


def day3(input_):
    wire1 = get_wire_points(input_[0])
    wire2 = get_wire_points(input_[1])

    print(part1(wire1, wire2))
    print(part2(wire1, wire2))


day3(["R8,U5,L5,D3", "U7,R6,D4,L4"])
day3(["R75,D30,R83,U83,L12,D49,R71,U7,L72", "U62,R66,U55,R34,D71,R55,D58,R83"])

day3(INPUT)
