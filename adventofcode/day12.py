import re
from dataclasses import dataclass
from itertools import combinations
from typing import List

from utils import read_input, test_case

INPUT = read_input(12)


@dataclass
class Moon:
    x: int
    y: int
    z: int
    dx: int = 0
    dy: int = 0
    dz: int = 0
    
    @staticmethod
    def from_str(s: str) -> 'Moon':
        x, y, z = map(int, re.findall(r'-?\d+', s))
        return Moon(x, y, z)
    
    def move(self):
        self.x += self.dx
        self.y += self.dy
        self.z += self.dz
    
    def __str__(self):
        return f'pos=<x={self.x:>2}, y={self.y:>2}, z={self.z:>2}>, vel<x={self.dx:>2}, y={self.dy:>2}, z={self.dz:>2}>'


def parse_input(inp: List[str]) -> List[Moon]:
    l = []
    for line in inp:
        l.append(Moon.from_str(line))
    
    return l


def total_energy(moons: List[Moon]) -> int:
    te = 0
    
    for moon in moons:
        pe = abs(moon.x) + abs(moon.y) + abs(moon.z)
        ke = abs(moon.dx) + abs(moon.dy) + abs(moon.dz)
        te += pe * ke
    
    return te


def simulate(moons: List[Moon], steps: int) -> List[Moon]:
    for i in range(steps):
        # print(f'After {i} steps:')
        # for moon in moons:
        #     print(moon)
        # print()
        for a, b in combinations(moons, 2):
            if a.x > b.x:
                a.dx -= 1
                b.dx += 1
            elif b.x > a.x:
                b.dx -= 1
                a.dx += 1
            if a.y > b.y:
                a.dy -= 1
                b.dy += 1
            elif b.y > a.y:
                b.dy -= 1
                a.dy += 1
            if a.z > b.z:
                a.dz -= 1
                b.dz += 1
            elif b.z > a.z:
                b.dz -= 1
                a.dz += 1
        
        for a in moons:
            a.move()
    
    return moons


def part1(inp: List[str], steps=1000) -> None:
    moons = parse_input(inp)
    
    moons = simulate(moons, steps)
    
    print(total_energy(moons))


test0 = test_case("""
<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>
""")

test1 = test_case("""
<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>
""")

if __name__ == '__main__':
    part1(test0, 10)
    part1(test1, 100)
    part1(INPUT)
