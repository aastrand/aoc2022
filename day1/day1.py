#!/usr/bin/env python3

import sys

from utils import io


def part1(filename):
    lines = io.get_input(filename).split("\n\n")

    return max([sum([int(l) for l in line.split("\n")]) for line in lines])


def part2(filename):
    lines = io.get_input(filename).split("\n\n")
    elves = [sum([int(l) for l in line.split("\n")]) for line in lines]
    elves.sort()

    return sum(elves[-3:])


def main():
    assert part1("example.txt") == 240
    print(part1("input.txt"))

    assert part2("example.txt") == 45000
    print(part2("input.txt"))


if __name__ == "__main__":
    sys.exit(main())
