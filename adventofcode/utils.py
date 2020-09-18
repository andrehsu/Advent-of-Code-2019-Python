from typing import List


def read_input_lines(filename: str) -> List[str]:
    return open(f'inputs/{filename}.txt').read().splitlines()


def read_input(filename: str) -> str:
    return open(f'inputs/{filename}.txt').read()


def test_case(raw_str: str) -> List[str]:
    return raw_str.strip('\n').splitlines()
