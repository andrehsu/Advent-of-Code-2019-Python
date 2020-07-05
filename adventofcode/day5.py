from typing import Tuple

from utils import read_input

INPUT = read_input(5)[0]


def parse_instruction(instruction: int) -> Tuple[int, int, int, int]:
    return (instruction % 100 // 1,
            instruction % 1000 // 100,
            instruction % 10000 // 1000,
            instruction % 100000 // 10000)


def program(input_, id_: int) -> None:
    mem = list(map(int, input_.split(',')))

    def param(num: int) -> int:
        return mem[i + num]

    def param_value(param_num: int) -> int:
        p = param(param_num)
        return p if modes[param_num - 1] == 1 else mem[p]

    i = 0
    while True:
        opcode, *modes = parse_instruction(mem[i])
    
        if opcode == 1:
            mem[param(3)] = param_value(1) + param_value(2)
        
            assert modes[2] == 0
            
            i += 4
        elif opcode == 2:
            mem[param(3)] = param_value(1) * param_value(2)
            
            assert modes[2] == 0
            
            i += 4
        elif opcode == 3:
            mem[param(1)] = id_
            
            assert modes[0] == 0
            
            i += 2
        elif opcode == 4:
            print(param_value(1), end=' ')
            
            i += 2
        elif opcode == 5:
            if param_value(1) != 0:
                i = param_value(2)
            else:
                i += 3
        elif opcode == 6:
            if param_value(1) == 0:
                i = param_value(2)
            else:
                i += 3
        elif opcode == 7:
            if param_value(1) < param_value(2):
                mem[param(3)] = 1
            else:
                mem[param(3)] = 0
            i += 4
        elif opcode == 8:
            if param_value(1) == param_value(2):
                mem[param(3)] = 1
            else:
                mem[param(3)] = 0
            i += 4
        elif opcode == 99:
            print()
            break
        else:
            raise RuntimeError(f"Unexpected opcode: {opcode}")


def day5(input_: str):
    part1(input_)
    part2(input_)


def part1(input_):
    program(input_, 1)


def part2(input_):
    program(input_, 5)


day5(INPUT)
