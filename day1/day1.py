#!/usr/bin/env python3

import sys

from utils import io


def part1(filename):
    lines = io.get_input(filename).strip().split("\n\n")

    return max([sum([int(ln) for ln in line.split("\n")]) for line in lines])


def part2(filename):
    lines = io.get_input(filename).strip().split("\n\n")
    elves = [sum([int(ln) for ln in line.split("\n")]) for line in lines]
    elves.sort()

    return sum(elves[-3:])


def main():
    assert part1("example.txt") == 24000
    print(part1("../input/2022/day1.txt"))

    assert part2("example.txt") == 45000
    print(part2("../input/2022/day1.txt"))


if __name__ == "__main__":
    sys.exit(main())
