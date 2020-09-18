from collections import defaultdict
from typing import Dict, Tuple, Optional

from utils import read_input

Pos = Tuple[int, int]

INPUT = read_input(13)


class Arcade:
    def __init__(self, code: str):
        self.mem = defaultdict(lambda: 0, ((i, int(value)) for i, value in enumerate(code.split(','))))
        self.screen: Dict[Pos, int] = defaultdict(lambda: 0)
        self.i = 0
        self.rb = 0
        self.score = -1
        self.tilt = 0
    
    @staticmethod
    def parse_instruction(instruction: int) -> Tuple[int, int, int, int]:
        return (instruction % 100 // 1,
                instruction % 1000 // 100,
                instruction % 10000 // 1000,
                instruction % 100000 // 10000)
    
    def run(self) -> None:
        while True:
            ret = self._resume()
            
            if ret is None:
                return

            x = ret
            y = self._resume()
            tile_id = self._resume()

            if x == -1 and y == 0:
                self.score = tile_id
            else:
                self.screen[(x, y)] = tile_id
                try:
                    x_ball, y_ball = self.get_tile_id_pos(4)
                    x_paddle, y_paddle = self.get_tile_id_pos(3)
                    if x_ball == x_paddle:
                        self.tilt = 0
                    elif x_ball > x_paddle:
                        self.tilt = 1
                    else:
                        self.tilt = -1
                except RuntimeError:
                    pass

    def get_tile_id_pos(self, tile_id: int) -> Pos:
        if tile_id not in self.screen.values():
            raise RuntimeError('No tile id')
        else:
            for pos, _tile_id in self.screen.items():
                if _tile_id == tile_id:
                    return pos

    def _resume(self) -> Optional[int]:
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
            opcode, *modes = Arcade.parse_instruction(self.mem[self.i])
            
            if opcode == 1:
                param_write(3, param_read(1) + param_read(2))
                
                self.i += 4
            elif opcode == 2:
                param_write(3, param_read(1) * param_read(2))
                
                self.i += 4
            elif opcode == 3:
                param_write(1, self.tilt)
    
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


def part1(inp: str) -> None:
    arcade = Arcade(inp)
    arcade.run()
    print(sum(i == 2 for i in arcade.screen.values()))


def part2(inp: str) -> None:
    arcade = Arcade(inp)
    arcade.mem[0] = 2
    arcade.run()
    print(arcade.score)


if __name__ == '__main__':
    part1(INPUT)
    part2(INPUT)
