from collections import defaultdict
from typing import Tuple

from utils import read_input

INPUT = read_input(9)[0]


def parse_instruction(instruction: int) -> Tuple[int, int, int, int]:
    return (instruction % 100 // 1,
            instruction % 1000 // 100,
            instruction % 10000 // 1000,
            instruction % 100000 // 10000)


def program(code: str, inp: int) -> None:
    mem = defaultdict(lambda: 0, ((i, int(value)) for i, value in enumerate(code.split(','))))
    
    def param(num: int) -> int:
        return mem[i + num]
    
    def param_read(param_num: int) -> int:
        p = param(param_num)
        mode = modes[param_num - 1]
        if mode == 0:
            return mem[p]
        elif mode == 1:
            return p
        elif mode == 2:
            return mem[rb + p]
        else:
            raise RuntimeError(f'Unexpected mode: {mode}')
    
    def param_write(param_num: int, value: int) -> None:
        mode = modes[param_num - 1]
        p = param(param_num)
        
        if mode == 0:
            mem[p] = value
        elif mode == 1:
            raise RuntimeError(f'Cannot write to absolute value')
        elif mode == 2:
            mem[p + rb] = value
        else:
            raise RuntimeError(f'Unexpected mode: {mode}')
    
    rb = 0
    i = 0
    while True:
        opcode, *modes = parse_instruction(mem[i])
        
        if opcode == 1:
            param_write(3, param_read(1) + param_read(2))
            
            i += 4
        elif opcode == 2:
            param_write(3, param_read(1) * param_read(2))
            
            i += 4
        elif opcode == 3:
            param_write(1, inp)
            
            i += 2
        elif opcode == 4:
            print(param_read(1), end=' ')
            
            i += 2
        elif opcode == 5:
            if param_read(1) != 0:
                i = param_read(2)
            else:
                i += 3
        elif opcode == 6:
            if param_read(1) == 0:
                i = param_read(2)
            else:
                i += 3
        elif opcode == 7:
            if param_read(1) < param_read(2):
                param_write(3, 1)
            else:
                param_write(3, 0)
            
            i += 4
        elif opcode == 8:
            if param_read(1) == param_read(2):
                param_write(3, 1)
            else:
                param_write(3, 0)
            i += 4
        elif opcode == 9:
            rb += param_read(1)
            
            i += 2
        elif opcode == 99:
            print()
            break
        else:
            raise RuntimeError(f"Unexpected opcode: {opcode}")


def part1(inp: str):
    program(inp, 1)


def part2(inp: str):
    program(inp, 2)


if __name__ == '__main__':
    part1('109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99')
    part1(INPUT)
    part2(INPUT)
