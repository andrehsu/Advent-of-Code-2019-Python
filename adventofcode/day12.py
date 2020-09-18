import math
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

    def apply_gravity(self, other):
        if self.x > other.x:
            self.dx -= 1
            other.dx += 1
        elif other.x > self.x:
            other.dx -= 1
            self.dx += 1
        if self.y > other.y:
            self.dy -= 1
            other.dy += 1
        elif other.y > self.y:
            other.dy -= 1
            self.dy += 1
        if self.z > other.z:
            self.dz -= 1
            other.dz += 1
        elif other.z > self.z:
            other.dz -= 1
            self.dz += 1

    def __str__(self):
        return f'pos=<x={self.x:>2}, y={self.y:>2}, z={self.z:>2}>, vel<x={self.dx:>2}, y={self.dy:>2}, z={self.dz:>2}>'


def lcm(a, b):
    return a * b // math.gcd(a, b)


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


def part1(inp: List[str], steps: int = 1000) -> None:
    moons = parse_input(inp)
    for i in range(steps):
        for a, b in combinations(moons, 2):
            a.apply_gravity(b)
        
        for a in moons:
            a.move()
    
    print(total_energy(moons))


def part2(inp: List[str]) -> None:
    moons = parse_input(inp)
    
    xs_loop = ys_loop = zs_loop = -1
    
    x_seen = set()
    y_seen = set()
    z_seen = set()
    
    step = 0
    while True:
        xs = tuple((x.x, x.dx) for x in moons)
        ys = tuple((x.y, x.dy) for x in moons)
        zs = tuple((x.z, x.dz) for x in moons)
        
        if xs_loop != -1 and ys_loop != -1 and zs_loop != -1:
            break
        
        if xs_loop == -1 and xs in x_seen:
            xs_loop = step
        else:
            x_seen.add(xs)
        
        if ys_loop == -1 and ys in y_seen:
            ys_loop = step
        else:
            y_seen.add(ys)
        
        if zs_loop == -1 and zs in z_seen:
            zs_loop = step
        else:
            z_seen.add(zs)
        
        for a, b in combinations(moons, 2):
            a.apply_gravity(b)
        
        for a in moons:
            a.move()
        
        step += 1
    
    print(lcm(lcm(xs_loop, ys_loop), zs_loop))


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
    # part1(test0, 10)
    # part1(test1, 100)
    part1(INPUT)
    part2(test0)
    # part2(test1)
    part2(INPUT)
