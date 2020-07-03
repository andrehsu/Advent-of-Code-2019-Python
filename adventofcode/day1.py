from adventofcode.utils import read_input

INPUT = read_input(1)


def fuel_cost(mass) -> int:
    fuel = mass // 3 - 2

    if fuel < 0:
        return 0
    else:
        return fuel + fuel_cost(fuel)


def part1(input_: list[str]) -> int:
    fuel = 0
    for line in input_:
        mass = int(line)
        fuel += mass // 3 - 2

    return fuel


def part2(input_: list[str]) -> int:
    fuel = 0
    for row in input_:
        mass = int(row)
        fuel += fuel_cost(mass)

    return fuel


def day1(input_: list[str]) -> None:
    print(part1(input_))
    print(part2(input_))


day1(INPUT)
