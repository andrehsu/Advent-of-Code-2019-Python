from collections import Counter, deque

from utils import read_input_lines

INPUT = read_input_lines(8)[0]


def part1(inp: str) -> None:
    digits = list(map(int, inp))
    
    layers = []
    
    size = 25 * 6
    for i in range(len(digits) // size):
        layer = digits[i * size: (i + 1) * size]
        layers.append(Counter(layer))
    
    layer_min_0 = min(layers, key=lambda c: c[0])
    
    print(layer_min_0[1] * layer_min_0[2])


def part2(inp: str) -> None:
    digits = deque(map(int, inp))
    
    img = [[deque() for _ in range(25)] for _ in range(6)]
    
    size = 25 * 6
    for layer in range(len(digits) // size):
        for r in range(6):
            for c in range(25):
                img[r][c].append(digits.popleft())
    
    for r in range(6):
        for c in range(25):
            pixel = img[r][c]
            while pixel[0] == 2:
                pixel.popleft()
            if pixel[0] != 0:
                print('#', end=' ')
            else:
                print(' ', end=' ')
        print()


if __name__ == '__main__':
    part1(INPUT)
    part2(INPUT)
