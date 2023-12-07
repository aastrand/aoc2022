#!/usr/bin/env python3

import sys
from collections import defaultdict

from utils import io
from utils.grid import (BOTTOM, BOTTOM_LEFT, BOTTOM_RIGHT, LEFT, RIGHT, TOP,
                        TOP_LEFT, TOP_RIGHT, Grid)

N = TOP
S = BOTTOM
W = LEFT
E = RIGHT
NW = TOP_LEFT
NE = TOP_RIGHT
SW = BOTTOM_LEFT
SE = BOTTOM_RIGHT


def parse(lines):
    grid = Grid.from_lines(lines)

    offsets = [
        [N, NE, NW],
        [S, SE, SW],
        [W, NW, SW],
        [E, NE, SE]
    ]

    return grid, offsets


def move(grid, offsets):
    moved = False
    proposals = defaultdict(list)
    new_grid = Grid()

    for pos, val in grid.items():
        if val == "#":

            surrounding = defaultdict(list)
            for stride in offsets:
                for o in stride:
                    neigh = (pos[0] + o[0], pos[1] + o[1])
                    if grid.get(neigh) == "#":
                        surrounding[stride[0]].append(neigh)

            if len(surrounding) > 0:
                for stride in offsets:
                    o = stride[0]

                    if len(surrounding[o]) == 0:
                        new_pos = (pos[0] + o[0], pos[1] + o[1])

                        if grid.get(new_pos) != "#":
                            proposals[new_pos].append(pos)
                            break

                else:
                    new_grid.set((pos), "#")
            else:
                new_grid.set((pos), "#")

    for pos, movers in proposals.items():
        if len(movers) == 1:
            new_grid.set(pos, "#")
            moved = True
        else:
            for pos in movers:
                new_grid.set(pos, "#")

    offsets.append(offsets.pop(0))

    return new_grid, offsets, moved


def part1(filename, rounds=10):
    grid, offsets = parse(io.get_lines(filename))

    # print("== Initial State ==")
    # grid.print()

    for _ in range(1, rounds+1):
        grid, offsets, _ = move(grid, offsets)

        # print("== End of Round", r, "==")
        # grid.print()

    sum = 0
    for y in range(grid.minY, grid.maxY+1):
        for x in range(grid.minX, grid.maxX+1):
            if grid.data.get((x, y)) != "#":
                sum += 1

    return sum


def part2(filename):
    grid, offsets = parse(io.get_lines(filename))

    r = 0
    moved = True
    while moved:
        grid, offsets, moved = move(grid, offsets)
        r += 1

    return r


def main():
    assert part1("example.txt") == 25
    assert part1("example2.txt") == 110
    print(part1("../input/2022/day23.txt"))

    assert part2("example2.txt") == 20
    print(part2("../input/2022/day23.txt"))


if __name__ == "__main__":
    sys.exit(main())
