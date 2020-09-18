from itertools import permutations
from typing import Optional, Tuple

from utils import read_input_lines

INPUT = read_input_lines(7)[0]


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
    
            mode = modes[param_num - 1]
            if mode == 0:
                return self.mem[p]
            elif mode == 1:
                return p
            else:
                raise RuntimeError('Unrecognized mode')

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
                ret_val = param_value(1)
                self.i += 2
                return ret_val
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


def day7(input_: str):
    part1(input_)
    part2(input_)


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


def part2(input_):
    signals = []
    
    for a, b, c, d, e in permutations(range(5, 10)):
        amplifiers = {
            'a': Amplifier(input_, a),
            'b': Amplifier(input_, b),
            'c': Amplifier(input_, c),
            'd': Amplifier(input_, d),
            'e': Amplifier(input_, e),
        }
        
        last_output = 0
        
        last_loop = False
        while not last_loop:
            for key, amplifier in amplifiers.items():
                output = amplifier.run(last_output)
                if output is None:
                    last_loop = True
                else:
                    last_output = output
        
        signals.append(last_output)
    
    print(max(signals))


if __name__ == '__main__':
    part1(INPUT)
    part2(INPUT)
