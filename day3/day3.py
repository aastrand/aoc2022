#!/usr/bin/env python3

import sys

from utils import io


def to_priority(item):
    offset = 96 if item.islower() else 38
    return ord(item) - offset


def part1(filename):
    lines = io.get_lines(filename)
    sum = 0

    for line in lines:
        p1 = set(line[:len(line)//2])
        p2 = set(line[len(line)//2:])
        item = (p1 & p2).pop()

        sum += to_priority(item)

    return sum


def part2(filename):
    lines = io.get_lines(filename)

    sum = 0

    for i in range(0, len(lines), 3):
        sacks = lines[i:i+3]
        p1 = set(sacks[0])
        p2 = set(sacks[1])
        p3 = set(sacks[2])
        item = (p1 & p2 & p3).pop()

        sum += to_priority(item)

    return sum


def main():
    assert part1("example.txt") == 157
    print(part1("input.txt"))

    assert part2("example.txt") == 70
    print(part2("input.txt"))


if __name__ == "__main__":
    sys.exit(main())
