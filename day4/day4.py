#!/usr/bin/env python3

import sys

from utils import io


def test_pairs(input, test):
    sum = 0

    for p in input:
        pairs = p.split(",")
        p1 = [int(i) for i in pairs[0].split("-")]
        p2 = [int(i) for i in pairs[1].split("-")]

        if test(p1, p2):
            sum += 1

    return sum


def part1(filename):
    return test_pairs(io.get_lines(filename), lambda p1, p2:
                      (p1[0] <= p2[0] and p1[1] >= p2[1]) or
                      (p2[0] <= p1[0] and p2[1] >= p1[1]))


def part2(filename):
    return test_pairs(io.get_lines(filename), lambda p1, p2:
                      (p1[0] <= p2[0] and p1[0] >= p2[1]) or
                      (p1[1] >= p2[0] and p1[1] <= p2[1]) or
                      (p2[0] <= p1[0] and p2[0] >= p1[1]) or
                      (p2[1] >= p1[0] and p2[1] <= p1[1]))


def main():
    assert part1("example.txt") == 2
    print(part1("input.txt"))

    assert part2("example.txt") == 4
    print(part2("input.txt"))


if __name__ == "__main__":
    sys.exit(main())
