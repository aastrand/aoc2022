#!/usr/bin/env python3

import sys

from utils import io


SHAPE_TO_POS = {
    "A": 0,
    "B": 1,
    "C": 2,
    "X": 0,
    "Y": 1,
    "Z": 2,
}


def part1(filename):
    lines = io.get_lines(filename)
    pairs = [(SHAPE_TO_POS[p[0]], SHAPE_TO_POS[p[1]])
             for p in [line.split(" ") for line in lines]]

    outcomes = [
        [3, 0, 6],  # rr, rp, rs
        [6, 3, 0],  # pr, pp, ps
        [0, 6, 3],  # sr, sp, ss
    ]

    return sum([p[1] + 1 + outcomes[p[1]][p[0]] for p in pairs])


def part2(filename):
    lines = io.get_lines(filename)
    pairs = [(SHAPE_TO_POS[p[0]], SHAPE_TO_POS[p[1]])
             for p in [line.split(" ") for line in lines]]

    inverse = [
        [2, 0, 1],  # lose
        [0, 1, 2],  # draw
        [1, 2, 0],  # win,
    ]
    return sum([p[1] * 3 + inverse[p[1]][p[0]] + 1 for p in pairs])


def main():
    assert part1("example.txt") == 15
    print(part1("input.txt"))

    assert part2("example.txt") == 12
    print(part2("input.txt"))


if __name__ == "__main__":
    sys.exit(main())
