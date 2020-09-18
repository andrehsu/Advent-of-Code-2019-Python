from typing import List

from adventofcode.utils import read_input_lines

INPUT = read_input_lines('day1')


def fuel_cost(mass) -> int:
    fuel = mass // 3 - 2
    
    if fuel < 0:
        return 0
    else:
        return fuel + fuel_cost(fuel)


def part1(input_: List[str]) -> int:
    fuel = 0
    for line in input_:
        mass = int(line)
        fuel += mass // 3 - 2
    
    return fuel


def part2(input_: List[str]) -> int:
    fuel = 0
    for row in input_:
        mass = int(row)
        fuel += fuel_cost(mass)
    
    return fuel


if __name__ == '__main__':
    print(part1(INPUT))
    print(part2(INPUT))
