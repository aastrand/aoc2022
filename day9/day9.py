#!/usr/bin/env python3

import sys

from utils import io
from utils.grid import BOTTOM, LEFT, RIGHT, TOP, Grid
from utils.math import sign

MOVES = {
    "U": TOP,
    "D": BOTTOM,
    "L": LEFT,
    "R": RIGHT,
}


def move_tail(t, h, offset):
    diff = [abs(t[0] - h[0]), abs(t[1] - h[1])]

    # if touches, do nothing
    if diff[0] <= 1 and diff[1] <= 1:
        return t

    if diff[0] == 1:
        t[0] = h[0]
        t[1] = h[1] - sign(h[1] - t[1])
    elif diff[1] == 1:
        t[0] = h[0] - sign(h[0] - t[0])
        t[1] = h[1]
    else:
        t[0] = h[0] - sign(h[0] - t[0])
        t[1] = h[1] - sign(h[1] - t[1])

    return t


def part1(filename):
    lines = io.get_lines(filename)

    h = [0, 0]
    t = [0, 0]

    visited = set()
    visited.add(tuple(t))

    for move in lines:
        parts = move.split(" ")
        dir = parts[0]
        steps = int(parts[1])

        offset = MOVES[dir]
        for s in range(0, steps):
            h[0] += offset[0]
            h[1] += offset[1]
            t = move_tail(t, h, offset)
            visited.add(tuple(t))

    return len(visited)


def part2(filename):
    lines = io.get_lines(filename)

    knots = [
        [0, 0],
        [0, 0],
        [0, 0],
        [0, 0],
        [0, 0],
        [0, 0],
        [0, 0],
        [0, 0],
        [0, 0],
        [0, 0],
    ]

    visited = set()
    visited.add(tuple(knots[9]))

    for move in lines:
        parts = move.split(" ")
        dir = parts[0]
        steps = int(parts[1])

        offset = MOVES[dir]
        for s in range(0, steps):
            knots[0][0] += offset[0]
            knots[0][1] += offset[1]

            grid = Grid()
            grid.set(tuple(knots[0]), "H")

            for k in range(1, len(knots)):
                knots[k] = move_tail(knots[k], knots[k - 1], offset)
                if tuple(knots[k]) not in grid.data:
                    grid.set(tuple(knots[k]), k)

            # grid.print()

            visited.add(tuple(knots[9]))

    # grid = Grid()
    # for v in visited:
    #     grid.set(v, "#")
    # grid.print()

    return len(visited)


def main():
    assert part1("example.txt") == 13
    print(part1("../input/2022/day9.txt"))

    # ......
    # ......
    # ......
    # ....H.
    # 4321..  (4 covers 5, 6, 7, 8, 9, s)

    # ......
    # ......
    # ....H.
    # .4321.
    # 5.....  (5 covers 6, 7, 8, 9, s)

    assert move_tail([2, 0], [4, -1], (0, -1)) == [3, -1]
    assert move_tail([0, 0], [2, -2], (0, -1)) == [1, -1]

    assert part2("example.txt") == 1
    assert part2("example2.txt") == 36
    print(part2("../input/2022/day9.txt"))


if __name__ == "__main__":
    sys.exit(main())
