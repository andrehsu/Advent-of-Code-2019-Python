from typing import List


def read_input(day: int) -> List[str]:
    return open(f'inputs/day{day}.txt').read().splitlines()


def test_case(raw_str: str) -> List[str]:
    return raw_str.strip('\n').splitlines()
