from itertools import permutations
from typing import Optional, Tuple

from utils import read_input

INPUT = read_input(7)[0]


def parse_instruction(instruction: int) -> Tuple[int, int, int, int]:
    return (instruction % 100 // 1,
            instruction % 1000 // 100,
            instruction % 10000 // 1000,
            instruction % 100000 // 10000)


class Amplifier:
    def __init__(self, code: str, phase_setting: int):
        self.i = 0
        self.mem = list(map(int, code.split(',')))
        
        self.inputs = [phase_setting]
    
    def run(self, input_signal: int) -> Optional[int]:
        self.inputs.append(input_signal)

        def param(num: int) -> int:
            return self.mem[self.i + num]
        
        def param_value(param_num: int) -> int:
            p = param(param_num)
            return p if modes[param_num - 1] == 1 else self.mem[p]

        while True:
            opcode, *modes = parse_instruction(self.mem[self.i])
            
            if opcode == 1:
                self.mem[param(3)] = param_value(1) + param_value(2)
                
                assert modes[2] == 0

                self.i += 4
            elif opcode == 2:
                self.mem[param(3)] = param_value(1) * param_value(2)
                
                assert modes[2] == 0

                self.i += 4
            elif opcode == 3:
                self.mem[param(1)] = self.inputs.pop(0)
                
                assert modes[0] == 0

                self.i += 2
            elif opcode == 4:
                return param_value(1)
            elif opcode == 5:
                if param_value(1) != 0:
                    self.i = param_value(2)
                else:
                    self.i += 3
            elif opcode == 6:
                if param_value(1) == 0:
                    self.i = param_value(2)
                else:
                    self.i += 3
            elif opcode == 7:
                if param_value(1) < param_value(2):
                    self.mem[param(3)] = 1
                else:
                    self.mem[param(3)] = 0
                self.i += 4
            elif opcode == 8:
                if param_value(1) == param_value(2):
                    self.mem[param(3)] = 1
                else:
                    self.mem[param(3)] = 0
                self.i += 4
            elif opcode == 99:
                return None
            else:
                raise RuntimeError(f"Unexpected opcode: {opcode}")


def day5(input_: str):
    part1(input_)


def part1(input_):
    signals = []
    for a, b, c, d, e in permutations(range(5)):
        a_output = Amplifier(input_, a).run(0)
        b_output = Amplifier(input_, b).run(a_output)
        c_output = Amplifier(input_, c).run(b_output)
        d_output = Amplifier(input_, d).run(c_output)
        e_output = Amplifier(input_, e).run(d_output)
        signals.append(e_output)
    print(max(signals))


day5(INPUT)
