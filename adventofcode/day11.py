from collections import defaultdict
from operator import itemgetter
from typing import Tuple, Optional, Dict, Set

from utils import read_input_lines

INPUT = read_input_lines(11)[0]

Pos = Tuple[int, int]


def parse_instruction(instruction: int) -> Tuple[int, int, int, int]:
    return (instruction % 100 // 1,
            instruction % 1000 // 100,
            instruction % 10000 // 1000,
            instruction % 100000 // 10000)


class Bot:
    def __init__(self, code: str):
        self.mem = defaultdict(lambda: 0, ((i, int(value)) for i, value in enumerate(code.split(','))))
        self.hull: Dict[Pos, int] = defaultdict(lambda: 0)
        self.painted: Set[Pos] = set()
        self.direction = 0
        self.x = 0
        self.i = 0
        self.rb = 0
        self.y = 0
    
    @property
    def pos_color(self) -> int:
        return self.hull[self.pos]
    
    @pos_color.setter
    def pos_color(self, value: int) -> None:
        self.hull[self.pos] = value
    
    @property
    def pos(self) -> Pos:
        return self.x, self.y
    
    def run(self) -> None:
        while True:
            ret = self._next_step(self.pos_color)
            if ret is None:
                return
            else:
                if ret != self.pos_color:
                    self.pos_color = ret
                    self.painted.add(self.pos)
                dir_change = self._next_step(self.pos_color)
                if dir_change == 0:
                    self.direction -= 1
                    if self.direction == -1:
                        self.direction += 4
                elif dir_change == 1:
                    self.direction += 1
                    if self.direction == 4:
                        self.direction -= 4
                else:
                    raise RuntimeError('Unexpected dir_change value')
                
                if self.direction == 0:
                    self.y += 1
                elif self.direction == 1:
                    self.x += 1
                elif self.direction == 2:
                    self.y -= 1
                elif self.direction == 3:
                    self.x -= 1
                else:
                    raise RuntimeError('Unexpected self.direction value')
    
    def _next_step(self, inp: int) -> Optional[int]:
        def param(num: int) -> int:
            return self.mem[self.i + num]
        
        def param_read(param_num: int) -> int:
            p = param(param_num)
            mode = modes[param_num - 1]
            if mode == 0:
                return self.mem[p]
            elif mode == 1:
                return p
            elif mode == 2:
                return self.mem[self.rb + p]
            else:
                raise RuntimeError(f'Unexpected mode: {mode}')
        
        def param_write(param_num: int, value: int) -> None:
            mode = modes[param_num - 1]
            p = param(param_num)
            
            if mode == 0:
                self.mem[p] = value
            elif mode == 1:
                raise RuntimeError(f'Cannot write to absolute value')
            elif mode == 2:
                self.mem[p + self.rb] = value
            else:
                raise RuntimeError(f'Unexpected mode: {mode}')
        
        while True:
            opcode, *modes = parse_instruction(self.mem[self.i])
            
            if opcode == 1:
                param_write(3, param_read(1) + param_read(2))
                
                self.i += 4
            elif opcode == 2:
                param_write(3, param_read(1) * param_read(2))
                
                self.i += 4
            elif opcode == 3:
                if inp is None:
                    raise RuntimeError('Input already used')
                param_write(1, inp)
                inp = None
                
                self.i += 2
            elif opcode == 4:
                ret = param_read(1)
                
                self.i += 2
                
                return ret
            elif opcode == 5:
                if param_read(1) != 0:
                    self.i = param_read(2)
                else:
                    self.i += 3
            elif opcode == 6:
                if param_read(1) == 0:
                    self.i = param_read(2)
                else:
                    self.i += 3
            elif opcode == 7:
                if param_read(1) < param_read(2):
                    param_write(3, 1)
                else:
                    param_write(3, 0)
                
                self.i += 4
            elif opcode == 8:
                if param_read(1) == param_read(2):
                    param_write(3, 1)
                else:
                    param_write(3, 0)
                self.i += 4
            elif opcode == 9:
                self.rb += param_read(1)
                
                self.i += 2
            elif opcode == 99:
                return None
            else:
                raise RuntimeError(f"Unexpected opcode: {opcode}")


def part1(inp: str):
    bot = Bot(inp)
    bot.run()
    print(len(bot.painted))


def part2(inp: str):
    bot = Bot(inp)
    bot.pos_color = 1
    bot.run()
    hull = bot.hull
    
    min_x = min(hull, key=itemgetter(0))[0]
    min_y = min(hull, key=itemgetter(1))[1]
    max_x = max(hull, key=itemgetter(0))[0]
    max_y = max(hull, key=itemgetter(1))[1]
    for y in range(max_y, min_y - 1, -1):
        for x in range(min_x, max_x + 1):
            print('#' if hull[x, y] == 1 else ' ', end='')
        print()


if __name__ == '__main__':
    part2(INPUT)
