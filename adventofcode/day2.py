from utils import read_input

INPUT = read_input(2)[0]


def program(mem, noun, verb):
    mem = mem.copy()

    mem[1] = noun
    mem[2] = verb

    i = 0
    while True:
        opcode = mem[i]
        if opcode == 1:
            read_0 = mem[i + 1]
            read_1 = mem[i + 2]
            write = mem[i + 3]
            mem[write] = mem[read_0] + mem[read_1]

            i += 4
        elif opcode == 2:
            read_0 = mem[i + 1]
            read_1 = mem[i + 2]
            write = mem[i + 3]
            mem[write] = mem[read_0] * mem[read_1]

            i += 4
        elif opcode == 99:
            break
        else:
            raise RuntimeError("Unexpected opcode")

    return mem[0]


def part1(mem):
    return program(mem, 12, 2)


def part2(mem):
    for noun in range(100):
        for verb in range(100):
            if program(mem, noun, verb) == 19690720:
                return noun * 100 + verb


def day2(input_: str):
    mem = list(map(int, input_.split(',')))
    print(part1(mem))
    print(part2(mem))


day2(INPUT)
