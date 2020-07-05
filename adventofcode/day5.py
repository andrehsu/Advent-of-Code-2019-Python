from typing import List, Tuple

from utils import read_input

INPUT = read_input(5)[0]

Memory = List[int]


def parse_instruction(instruction: int) -> Tuple[int, int, int, int]:
    return (instruction % 100 // 1,
            instruction % 1000 // 100,
            instruction % 10000 // 1000,
            instruction % 100000 // 10000)


def program(mem: Memory, id_: int) -> None:
    mem = mem.copy()
    
    def param(num: int) -> int:
        return mem[i + num]
    
    i = 0
    while True:
        opcode, *modes = parse_instruction(mem[i])
        
        def read_mem_at_param(param_num: int) -> int:
            param_value = param(param_num)
            return param_value if modes[param_num - 1] == 1 else mem[param_value]
        
        if opcode == 1:
            mem[param(3)] = read_mem_at_param(1) + read_mem_at_param(2)
            
            assert modes[2] == 0
            
            i += 4
        elif opcode == 2:
            mem[param(3)] = read_mem_at_param(1) * read_mem_at_param(2)
            
            assert modes[2] == 0
            
            i += 4
        elif opcode == 3:
            mem[param(1)] = id_
            
            assert modes[0] == 0
            
            i += 2
        elif opcode == 4:
            print(read_mem_at_param(1), end=' ')
            
            i += 2
        elif opcode == 99:
            break
        else:
            raise RuntimeError(f"Unexpected opcode: {opcode}")


def day5(input_: str):
    mem = list(map(int, input_.split(',')))
    part1(mem)


def part1(mem: Memory):
    program(mem, 1)


day5(INPUT)
