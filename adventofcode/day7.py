from itertools import permutations

from utils import read_input

INPUT = read_input(7)[0]


def parse_instruction(instruction: int) -> tuple[int, int, int, int]:
    return (instruction % 100 // 1,
            instruction % 1000 // 100,
            instruction % 10000 // 1000,
            instruction % 100000 // 10000)


def program(code, phase_setting: int, input_signal: int) -> int:
    inputs = [phase_setting, input_signal]
    
    mem = list(map(int, code.split(',')))
    
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
            mem[param(1)] = inputs.pop(0)
            
            assert modes[0] == 0
            
            i += 2
        elif opcode == 4:
            return param_value(1)
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


def part1(input_):
    signals = []
    for a, b, c, d, e in permutations(range(5)):
        a_output = program(input_, a, 0)
        b_output = program(input_, b, a_output)
        c_output = program(input_, c, b_output)
        d_output = program(input_, d, c_output)
        e_output = program(input_, e, d_output)
        signals.append(e_output)
    print(max(signals))


day5(INPUT)
