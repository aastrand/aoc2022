#!/usr/bin/env python3

import sys

from utils import io
from utils.parse import ints


def parse(input):
    parts = input.split("\n\n")
    stack_input = parts[0].split("\n")[:-1]
    size = len(stack_input[0])//3
    stacks = []
    for _ in range(0, size):
        stacks.append([])

    for row in stack_input:
        c = 0
        for v in range(1, len(row), 4):
            if row[v] != " ":
                stacks[c].insert(0, row[v])
            c += 1

    instructions = parts[1].strip().split("\n")

    return stacks, instructions


def answer(stacks):
    r = []
    for s in stacks:
        r.append(s[-1] if len(s) > 0 else "")

    return "".join(r)


def part1(filename):
    stacks, instructions = parse(io.get_input(filename))
    for instr in instructions:
        idx = ints(instr)
        for _ in range(0, idx[0]):
            moved = stacks[idx[1] - 1].pop()
            stacks[idx[2] - 1].append(moved)

    return answer(stacks)


def part2(filename):
    stacks, instructions = parse(io.get_input(filename))
    for instr in instructions:
        idx = ints(instr)
        moved = stacks[idx[1] - 1][-idx[0]:]
        stacks[idx[1] - 1] = stacks[idx[1] - 1][:-idx[0]]
        stacks[idx[2] - 1].extend(moved)

    return answer(stacks)


def main():
    assert part1("example.txt") == "CMZ"
    print(part1("input.txt"))

    assert part2("example.txt") == "MCD"
    print(part2("input.txt"))


if __name__ == "__main__":
    sys.exit(main())
