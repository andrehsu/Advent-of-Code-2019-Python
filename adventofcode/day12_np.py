import re
from typing import List

import numpy as np

from utils import read_input_lines, test_case

INPUT = read_input_lines('day12')


def parse_input(inp: List[str]) -> np.ndarray:
    l = []
    for line in inp:
        x, y, z = map(int, re.findall(r'-?\d+', line))
        l.append(np.array([x, y, z, 0, 0, 0]))
    
    return np.array(l)


def total_energy(moons: np.ndarray) -> int:
    te = 0
    
    for x, y, z, dx, dy, dz in moons:
        pe = abs(x) + abs(y) + abs(z)
        ke = abs(dx) + abs(dy) + abs(dz)
        te += pe * ke
    
    return te


# @numba.njit
def simulate(moons: np.ndarray) -> None:
    for step in range(1000):
        for i in range(len(moons)):
            for j in range(i + 1, len(moons)):
                a = moons[i]
                b = moons[j]
                if a[0] > b[0]:
                    a[3] -= 1
                    b[3] += 1
                elif b[0] > a[0]:
                    b[3] -= 1
                    a[3] += 1
                if a[1] > b[1]:
                    a[4] -= 1
                    b[4] += 1
                elif b[1] > a[1]:
                    b[4] -= 1
                    a[4] += 1
                if a[2] > b[2]:
                    a[5] -= 1
                    b[5] += 1
                elif b[2] > a[2]:
                    b[5] -= 1
                    a[5] += 1
        
        for a in moons:
            a[0] += a[3]
            a[1] += a[4]
            a[2] += a[5]


def part1(inp: List[str]) -> None:
    moons = parse_input(inp)
    
    simulate(moons)
    
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
    part1(INPUT)
