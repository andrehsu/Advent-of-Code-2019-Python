from dataclasses import dataclass
from typing import List, Dict

from utils import read_input

INPUT = read_input(6)


@dataclass(frozen=True)
class Planet:
    _planets: Dict[str, 'Planet']
    _parent_name: str
    name: str

    @property
    def parent(self):
        if self._parent_name == 'COM':
            return None
        else:
            return self._planets[self._parent_name]

    def level(self):
        if self.parent is not None:
            return 1 + self.parent.level()
        else:
            return 1


def part1(input_: List[str]) -> int:
    planets = parse_planets(input_)
    
    return sum(planet.level() for planet in planets.values())


def part2(input_: List[str]) -> int:
    planets = parse_planets(input_)
    
    steps = 0
    
    you_parent = planets['YOU'].parent
    san_parent = planets['SAN'].parent
    
    while you_parent != san_parent:
        while you_parent.level() > san_parent.level():
            you_parent = you_parent.parent
            steps += 1
        while san_parent.level() > you_parent.level():
            san_parent = san_parent.parent
            steps += 1

        san_parent = san_parent.parent
        you_parent = you_parent.parent
        steps += 2

    return steps


def parse_planets(input_: List[str]) -> Dict[str, Planet]:
    planets = {}
    
    for row in input_:
        parent, child = row.split(')')
        planets[child] = Planet(planets, parent, child)
    
    return planets


if __name__ == '__main__':
    print(part1(INPUT))

    print(part2(INPUT))
